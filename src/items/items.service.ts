import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { NotFoundException } from '@nestjs/common';
import { randomBytes } from 'crypto';
import { ItemDto } from './dto/item.dto';
import { Request } from 'express';
import { getBaseUrl } from 'src/utils';

@Injectable()
export class ItemsService {
    constructor(private prisma: PrismaService) {}
    
    async getAllItems(req: Request) {
        const baseUrl = getBaseUrl(req);
        const items = await this.prisma.items.findMany({
          where: { isDeleted: 0 }
        });
      
        return items.map(item => ({
          ...item,
          image: item.image ? `${baseUrl}${item.image}` : null
        }));
      }
      

    async getItemById(id: number, req: Request) {
        const baseUrl = getBaseUrl(req);
        const item = await this.prisma.items.findUnique({
            where: {
                id: id,
                isDeleted: 0,
            }
        });

        if (!item) {
            throw new NotFoundException(`Item with id ${id} not found xwx`);
        }

        return {
            ...item,
            image: item.image ? `${baseUrl}${item.image}` : null
          };
    }

    async createItem(data: ItemDto) {
        return await this.prisma.items.create({
            data: {
                itemCode: data.itemCode || randomBytes(6).toString('base64').replace(/[^a-zA-Z0-9]/g, '').substring(0, 8),
                name: data.name,
                description: data.description || null,
                price: data.price || 0,
                quantity: data.quantity || 0,
                image: data.image || null,
                createdUser: 0, // <---------- Not use yet :>
                createdAt: new Date(),
                isDeleted: 0,
            },
        });
    }    

    async updateItem(id: number, data: any, image: Express.Multer.File, req: Request) {
        const item = await this.prisma.items.findUnique({
          where: { id, isDeleted: 0 },
        });
    
        if (!item) {
          throw new NotFoundException(`Item with id ${id} not found xwx`);
        }
    
        // If a new image is uploaded, update the image URL
        if (image) {
          data.image = `/assets/uploads/image/${image.filename}`;
        }
    
        return await this.prisma.items.update({
          where: { id },
          data: {
            ...data,
            updatedUser: 0, // <---------- Not use yet :>
            updatedAt: new Date(),
        }
        });
    }

    async softDeleteItem(id: number) {
        const item = await this.prisma.items.findUnique({
          where: { id, isDeleted: 0 },
        });
      
        // Check if the item exists
        if (!item) {
          throw new NotFoundException(`Item with id ${id} not found xwx`);
        }
      
        // Proceed to update the item and mark it as deleted
        await this.prisma.items.update({
          where: { id },
          data: {
            isDeleted: 1, // Set isDeleted to 1 for soft delete
            updatedUser: 0, // <---------- Not use yet :>
            updatedAt: new Date(),
          },
        });
      
        return {
          message: `Item with id ${id} has been deleted successfully! ^w^`,
          statusCode: 200,
        };
    }
}