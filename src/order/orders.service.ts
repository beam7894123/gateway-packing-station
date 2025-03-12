import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { NotFoundException } from '@nestjs/common';
import { OrderDto } from './dto/order.dto';
import { Request } from 'express';
import { getBaseUrl } from 'src/utils';
import { Response } from 'express';
import { pdfPickingList } from './pdfPickingList';
import * as path from 'path';
import * as fs from 'fs';

@Injectable()
export class OrdersService {
    constructor(private prisma: PrismaService) {}
    
    async getAllOrders (req: Request) {
        const orders = await this.prisma.orders.findMany({
          where: { isDeleted: 0 }
        });
      
        return orders
      }
      

    async getOrderById(id: number, req: Request) {
        const baseUrl = getBaseUrl(req);
        const order = await this.prisma.orders.findUnique({
            where: {
                id: id,
                isDeleted: 0,
            },
            include: {
                orderItems: {
                    include: {
                        item: true, // Include detailed information about each item
                    },
                },
            },
        });
    
        if (!order) {
            throw new NotFoundException(`Orders with id ${id} not found xwx`);
        }
    
        // Add full image URL to each item
        return {
            ...order,
            orderItems: order.orderItems.map(orderItem => ({
                ...orderItem,
                item: {
                    ...orderItem.item,
                    image: orderItem.item.image ? `${baseUrl}${orderItem.item.image}` : null
                }
            }))
        };
    }    

    async getRecordVideo(id: number, res: Response, req: Request) {
      const baseUrl = getBaseUrl(req);
      
      const packingProof = await this.prisma.packing_proofs.findFirst({
          where: {
              orderId: id,
              isDeleted: 0,
          },
          select: {
              video: true,
          },
      });
  
      if (!packingProof || !packingProof.video) {
          return res.status(404).json({ error: 'No video found for this order >m<' });
      }
  
      return res.json({ url: `${baseUrl}${packingProof.video}` });
    }
  

    async createOrder(data: OrderDto) {
        const items = data.items;
      
        // Start a transaction to ensure order creation and item stock update are both atomic
        const order = await this.prisma.$transaction(async (prisma) => {
          // Create the order
          const order = await prisma.orders.create({
            data: {
              customer: data.customer,
              status: 1, // Default status (received)
              trackingNumber: data.trackingNumber || null,
              createdAt: new Date(),
              updatedAt: null,
              isDeleted: 0,
              orderItems: {
                create: items.map(item => ({
                  itemId: item.itemId,
                  quantity: item.quantity,
                })),
              },
            },
            include: {
              orderItems: true, // Include order items in the response
            },
          });
      
          // Update the item quantities
          await Promise.all(
            items.map(async (item) => {
              const updatedItem = await prisma.items.update({
                where: { id: item.itemId },
                data: {
                  quantity: {
                    decrement: item.quantity, // Decrease item quantity
                  },
                },
              });
            })
          );
      
          return order;
        });
      
        return order;
      }      

    async softDeleteOrders(id: number) {
        const orders = await this.prisma.orders.findUnique({
          where: { id, isDeleted: 0 },
        });
      
        // Check if the item exists
        if (!orders) {
          throw new NotFoundException(`Orders with id ${id} not found xwx`);
        }
      
        // Proceed to update the item and mark it as deleted
        await this.prisma.orders.update({
          where: { id },
          data: {
            isDeleted: 1, // Set isDeleted to 1 for soft delete
            updatedUser: 0, // <---------- Not use yet :>
            updatedAt: new Date(),
          },
        });
      
        return {
          message: `Orders with id ${id} has been deleted successfully! ^w^`,
          statusCode: 200,
        };
    }

    async generatePickingListPdf(id: number, res: Response, req: Request) {
        const order = await this.getOrderById(id, req);
        const pdfBuffer = await pdfPickingList(order);
        const pdfDir = path.join(__dirname, '../../assets/uploads/pdfs');
        const timestamp = new Date().toISOString().replace(/[-:.]/g, '_');
        const baseUrl = getBaseUrl(req);

        if (!fs.existsSync(pdfDir)) {
            fs.mkdirSync(pdfDir, { recursive: true });
        }
        const pdfFilePath = path.join(pdfDir, `order-${order.id}-${timestamp}.pdf`);
        try {
            fs.writeFileSync(pdfFilePath, pdfBuffer);
        } catch (error) {
            console.error('Error Writing PickingList PDF File:', error);
            return res.status(500).json({ error: 'Failed to generate PickingList PDF >m<' });
        }

        const fileUrl = `${baseUrl}/assets/uploads/pdfs/order-${order.id}-${timestamp}.pdf`;
        return res.json({ url: fileUrl });
    }

    // async generatePickingListPdf(id: number, res: Response, req: Request) {
    //     const order = await this.getOrderById(id, req);

    //     const doc = new PDFDocument();
    //     res.setHeader('Content-Disposition', `attachment; filename="picking-list-${order.id}.pdf"`);
    //     res.setHeader('Content-Type', 'application/pdf');
    //     doc.pipe(res);

    //     // Title
    //     doc.fontSize(20).text(`Picking List - Order #${order.id}`, { align: 'center' });
    //     doc.moveDown();
    //     doc.fontSize(12).text(`Customer: ${order.customer}`);
    //     doc.text(`Tracking Number: ${order.trackingNumber || 'N/A'}`);
    //     doc.moveDown();

    //     // Items table title
    //     doc.fontSize(14).text('Items:', { underline: true });
    //     doc.moveDown();

    //     // Create folder if missing
    //     const barcodeDir = path.join(__dirname, '../../assets/barcodes');
    //     if (!fs.existsSync(barcodeDir)) {
    //         fs.mkdirSync(barcodeDir, { recursive: true });
    //     }

    //     // Start the table
    //     let tableTop = doc.y;

    //     for (const item of order.orderItems) {
    //         const barcodePath = path.join(barcodeDir, `${item.item.id}.png`);

    //         try {
    //             // Generate barcode
    //             const pngBuffer = await bwipjs.toBuffer({
    //                 bcid: 'code128',
    //                 text: item.item.itemCode,
    //                 scale: 3,
    //                 height: 10,
    //                 includetext: true,
    //                 textxalign: 'center',
    //             });

    //             // Save barcode image
    //             fs.writeFileSync(barcodePath, pngBuffer);

    //             // Table row: Image on the left and barcode on the right
    //             const xLeft = 50;
    //             const xRight = 300;
    //             const rowHeight = 80;

    //             // Draw the item image (assumes the item has an image URL)
    //             if (item.item.image) {
    //                 const imagePath = path.join(__dirname, `../../${item.item.image}`);
    //                 doc.image(imagePath, xLeft, tableTop, { width: 80, height: 80 });
    //             }

    //             // Draw the barcode
    //             doc.image(barcodePath, xRight, tableTop, { width: 150, height: 50 });

    //             // Item description and quantity on the left side
    //             doc.fontSize(12).text(`Item: ${item.item.name}`, xLeft + 90, tableTop + 10);
    //             doc.text(`Quantity: ${item.quantity}`, xLeft + 90, tableTop + 30);

    //             // Move to the next row
    //             tableTop += rowHeight;
    //         } catch (error) {
    //             console.error(`Failed to generate barcode for ${item.item.name}`, error);
    //             // doc.text(`[Barcode not available]`);
    //         }
    //     }

    //     doc.end();
    // }
}