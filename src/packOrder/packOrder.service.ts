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
    

    async getAllOrders(req: Request, { status, createdAt }: { status?: string, createdAt?: string }) {
        const baseUrl = getBaseUrl(req);
        let packing = await this.prisma.packing_proofs.findMany({
            where: { isDeleted: 0 },
            include: {
                order: true,
            }
        });

        if (status) {
            packing = packing.filter(proof => proof.status === parseInt(status));
        }

        if (createdAt) {
            packing = packing.filter(proof => proof.createdAt.toISOString().includes(createdAt));
        }

        return packing.map(proof => ({
            ...proof,
            video: proof.video ? `${baseUrl}${proof.video}` : null
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
            throw new HttpException(`Failed to send proof to ${packing.order.customerEmail} xwx`, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}