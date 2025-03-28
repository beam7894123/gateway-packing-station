import { forwardRef, HttpException, HttpStatus, Inject, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { Request } from 'express';
import { PickingStationService } from 'src/pickingStation/pickingStation.service';
import { getBaseUrl } from 'src/utils';
import { MailingService } from 'src/service/mailing.service';

@Injectable()
export class PackingOrderService {
    constructor(private prisma: PrismaService,
        @Inject(forwardRef(() => PickingStationService))
        private readonly pickingStationService: PickingStationService,
        private readonly mailingService: MailingService,
    ) {} 
    

    async getAllOrders(req: Request, { status, createdAt, startDate, endDate }: { status?: string, createdAt?: string, startDate?: string, endDate?: string }) {
        const baseUrl = getBaseUrl(req);
    
        const whereClause: any = { isDeleted: 0 };
    
        if (status) {
            whereClause.status = parseInt(status);
        }
    
        if (createdAt) {
            const date = new Date(createdAt);
            whereClause.createdAt = {
                gte: new Date(date.setHours(0, 0, 0, 0)),
                lt: new Date(date.setHours(23, 59, 59, 999)),
            };
        }        
    
        if (startDate && endDate) {
            const start = new Date(startDate);
            const end = new Date(endDate);
            whereClause.createdAt = {
                gte: new Date(start.setHours(0, 0, 0, 0)),
                lte: new Date(end.setHours(23, 59, 59, 999)),
            };
        }
    
        // Fetch data with filters applied directly in the query
        const packing = await this.prisma.packing_proofs.findMany({
            where: whereClause,
            include: {
                order: true,
            },
        });
    
        // Map the results to include the full video URL
        return packing.map(proof => ({
            ...proof,
            video: proof.video ? `${baseUrl}${proof.video}` : null,
        }));
    }    

    async getOrderById(id: number, req: Request) {
        const baseUrl = getBaseUrl(req);
        const packing =  await this.prisma.packing_proofs.findUnique({
            where: { id, isDeleted: 0 },
            include: { order: true }
        });

        if (!packing) {
            throw new NotFoundException(`Packing proof with id ${id} not found xwx`);
        }

        return {
            ...packing,
            video: packing.video ? `${baseUrl}${packing.video}` : null
        };
    }

    async softDeletePackingProof(id: number) {
        const packing_proofs = await this.prisma.packing_proofs.findUnique({
            where: { id, isDeleted: 0 }
        });

        if (!packing_proofs) {
            throw new NotFoundException(`Packing proof with id ${id} not found xwx`);
        }

        await this.prisma.orders.update({
            where: { id: packing_proofs.orderId },
            data: { status: 2 } // Set the order back to Paid
        });


        return await this.pickingStationService.softDeletePackingProof(id);
    }

    async sendProofToMailById(id: number, req: Request) {
        const baseUrl = getBaseUrl(req);
        const packing = await this.prisma.packing_proofs.findUnique({
            where: { id, isDeleted: 0 },
            include: { order: true }
        });

        if (!packing) {
            throw new HttpException(`Packing proof with id ${id} not found xwx`, HttpStatus.NOT_FOUND);
        }

        if (!packing.video) {
            throw new HttpException(`Proof video not found for order ${packing.order.id}! xwx`, HttpStatus.BAD_REQUEST);
        }

        const packingFinal = {
            ...packing,
            video: packing.video ? `${baseUrl}${packing.video}` : null
        };

        if (!packingFinal.order.customerEmail) {
            throw new HttpException(`Customer email not found for order ${packing.order.id} xwx`, HttpStatus.BAD_REQUEST);
        }
        
        // If the proof video is not found, throw an error and brick the process XD
        if (!packingFinal.video) { 
             throw new HttpException(`Proof video not found for order ${packing.order.id} xwx`, HttpStatus.BAD_REQUEST);
        }

        try {
            await this.mailingService.sendPackingProofEmail(packingFinal.order.customerEmail, packingFinal.order.customer, packingFinal.order.id, packingFinal.video);
            await this.prisma.packing_proofs.update({
                where: { id },
                data: { status: 3 }
            });
            return { message: `Proof sent to ${packing.order.customerEmail} successfully ^w^` };
        }
        catch (error) {
            console.error(`Failed to send proof to ${packing.order.customerEmail}:`, error);
            throw new HttpException(`Failed to send proof to ${packing.order.customerEmail} xwx`, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}