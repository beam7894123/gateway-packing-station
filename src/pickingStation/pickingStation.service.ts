import { HttpException, HttpStatus, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { Request } from 'express';
import { StationDto } from './dto/station.dto';
import { getBaseUrl } from 'src/utils';

@Injectable()
export class PickingStationService {
    constructor(private prisma: PrismaService) {}

    async checkOrderPackingProof(orderId: number, req: Request) {
        const packing_proof = await this.prisma.packing_proofs.findFirst({
            where: { orderId: orderId, isDeleted: 0 },
        });

        if (packing_proof?.status === 0) {
            throw new HttpException('Found but this order packing failed!', HttpStatus.OK);
        }
        if (packing_proof?.status === 1) {
            throw new HttpException('Order is in used!', HttpStatus.FORBIDDEN);
        }
        if (!packing_proof) {
            throw new HttpException('Order not found! xwx', HttpStatus.NOT_FOUND);
        }
        else {
            return this.getScannedAndUnscannedItems(packing_proof.id, req);
        }
    }
    
    async startScan(data: StationDto, req: Request) {

        // Check if order exists
        const orderExists = await this.prisma.orders.findUnique({
            where: { id: data.orderId, isDeleted: 0 }, // Ensure it's not deleted
        });

        if (!orderExists) {
            throw new HttpException(`Order with id ${data.orderId} not found or deleted >m<`, HttpStatus.NOT_FOUND);
        }
        
        const existingProofs = await this.prisma.packing_proofs.findMany({
            where: { orderId: data.orderId, isDeleted: 0 },
        });

        if (existingProofs.length > 0) {
            throw new HttpException('Look like this order is already scanned! :<', HttpStatus.FORBIDDEN);
        }

        const newProof = await this.prisma.packing_proofs.create({
            data: {
                orderId: data.orderId,
                station: data.station,
                status: 1, // 1 means scan started
                video: data.video || null,
                createdAt: new Date(),
                isDeleted: 0,
            },
        });

        return this.getScannedAndUnscannedItems(newProof.id, req);;
    }

    async scannedItem(data: StationDto, req: Request) {
        const packingProof = await this.prisma.packing_proofs.findFirst({
            where: {
                orderId: data.orderId,
                status: 1,
                isDeleted: 0,
            },
        });

        if (!packingProof) {
            throw new HttpException('Scan start barcode first!', HttpStatus.FORBIDDEN);
        }

        const item = await this.prisma.items.findUnique({
            where: { itemCode: data.itemCode, isDeleted: 0 },
        });

        if (!item) {
            throw new HttpException('Item not found xwx', HttpStatus.NOT_FOUND);
        }

        // Check if the item has already been fully scanned
        const scannedItemCount = await this.prisma.packing_scans_list.count({
            where: {
            orderId: data.orderId,
            itemId: item.id,
            packingProofId: packingProof.id,
            isDeleted: 0,
            },
        });
        const orderItem = await this.prisma.order_items.findFirst({
            where: { 
                orderId: data.orderId, 
                itemId: item.id 
            },
        });
        let orderItemQuantity = 0;
        if (orderItem) {
            orderItemQuantity = orderItem.quantity;
        }
        if ((scannedItemCount + 1) > orderItemQuantity) {
            throw new HttpException('This item has already been scanned! >:<', HttpStatus.FORBIDDEN);
        }

        // Add the scanned item to the list
        await this.prisma.packing_scans_list.create({
            data: {
            packingProofId: packingProof.id,
            orderId: data.orderId,
            itemId: item.id,
            scannedAt: new Date(),
            isDeleted: 0,
            },
        });

        return this.getScannedAndUnscannedItems(packingProof.id, req);
    }

    async getScannedAndUnscannedItems(packingProofId: number, req: Request) {
        const baseUrl = getBaseUrl(req);
        
        // Get the orderId from packing_proofs
        const packingProof = await this.prisma.packing_proofs.findUnique({
            where: { id: packingProofId, isDeleted: 0 },
            select: { orderId: true },
        });
    
        if (!packingProof) {
            throw new HttpException('Packing proof not found xwx??', HttpStatus.NOT_FOUND);
        }
    
        // Get all items in the order with their quantities and details
        const orderItems = await this.prisma.order_items.findMany({
            where: { orderId: packingProof.orderId },
            select: {
                itemId: true,
                quantity: true,
                item: true,
            },
        });
    
        // Get all scanned items in the order with their quantities
        const scannedItems = await this.prisma.packing_scans_list.groupBy({
            by: ['itemId'],
            where: { orderId: packingProof.orderId, packingProofId: packingProofId, isDeleted: 0 },
            _count: { itemId: true },
        });
    
        const scannedItemMap = new Map(scannedItems.map(item => [item.itemId, item._count.itemId]));
    
        const scanned: { itemId: number; name: string; description: string | null; image: string | null; price: number | null; scannedQuantity: number }[] = [];
        const unscanned: { itemId: number; name: string; description: string | null; image: string | null; price: number | null; unscannedQuantity: number }[] = [];
    
        // Categorize scanned and unscanned items with details
        for (const orderItem of orderItems) {
            const scannedQuantity = scannedItemMap.get(orderItem.itemId) || 0;
            const unscannedQuantity = orderItem.quantity - scannedQuantity;
    
            const itemDetails = {
                itemId: orderItem.itemId,
                name: orderItem.item.name,
                description: orderItem.item.description,
                image: orderItem.item.image ? `${baseUrl}${orderItem.item.image}` : null,
                price: orderItem.item.price,
            };
    
            if (scannedQuantity > 0) {
                scanned.push({
                    ...itemDetails,
                    scannedQuantity,
                });
            }
    
            if (unscannedQuantity > 0) {
                unscanned.push({
                    ...itemDetails,
                    unscannedQuantity,
                });
            }
        }
    
        return { scanned, unscanned };
    }

    async checkScannedAndUnscannedItems(packingProofId: number, req: Request) {
        return this.getScannedAndUnscannedItems(packingProofId, req);
    }

    async finishScan(data: StationDto) {
        const packingProof = await this.prisma.packing_proofs.findFirst({
            where: {
                orderId: data.orderId,
                status: 1,
                isDeleted: 0,
            },
        });
    
        if (!packingProof) {
            throw new HttpException('No active scan found for this order! xwx', HttpStatus.NOT_FOUND);
        }



        if (data.video) {
            return await this.prisma.packing_proofs.update({
                where: { id: packingProof.id },
                data: { 
                    status: 2, // 2 means scan finished with video
                    finishTime: new Date(),
                    updatedAt: new Date(),
                    video: data.video,
    
                 },
            });
        }

        if (!data.video) {
            // throw new HttpException('Please upload a video! xwx', HttpStatus.BAD_REQUEST);
            return await this.prisma.packing_proofs.update({
                where: { id: packingProof.id },
                data: { 
                    status: 0, // 0 means Error
                 },
            });
        }
    
        throw new HttpException('uhhhhhhhhhh what? @w@', HttpStatus.INTERNAL_SERVER_ERROR);
    }

    async restartScan(data: StationDto, req: Request) {

        const packingProofsId = await this.prisma.packing_proofs.findFirst({
            where: { orderId: data.orderId, status: { in: [0, 1] }, isDeleted: 0 },
            select: { id: true },
        });
        if (packingProofsId && packingProofsId.id) {
            await this.softDeletePackingProof(packingProofsId.id);
        }

        return await this.startScan(data, req);
    }

    async softDeletePackingProof(packingProofId: number) {
        // Check if the packing proof exists
        const packingProof = await this.prisma.packing_proofs.findUnique({
            where: { id: packingProofId, isDeleted: 0 }, // Ensure it's not already deleted
        });
    
        if (!packingProof) {
            throw new NotFoundException(`Packing proof with ID ${packingProofId} not found! xwx`);
        }
    
        // Soft delete the packing proof
        await this.prisma.packing_proofs.update({
            where: { id: packingProofId },
            data: { isDeleted: 1 },
        });
    
        // Soft delete all scanned items related to this packing proof
        await this.prisma.packing_scans_list.updateMany({
            where: { packingProofId: packingProofId },
            data: { isDeleted: 1 },
        });
    
        return {
            message: `Packing proof and related scanned items have been deleted! owo`,
            statusCode: 200,
        };
    }
    
    async getAllwaiting(req: Request) {
        // const result = await this.prisma.pickingStation.findMany();
        // return result;
        return 'Meow :3';
    }

}