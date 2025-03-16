import { HttpException, HttpStatus, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { Request } from 'express';
import { PickingStationService } from 'src/pickingStation/pickingStation.service';
import { getBaseUrl } from 'src/utils';
import { MailingService } from 'src/service/mailing.service';

@Injectable()
export class PackingOrderService {
    constructor(private prisma: PrismaService,
        private readonly pickingStationService: PickingStationService,
        private readonly mailingService: MailingService,
    ) {} 
    

    async getAllOrders(req: Request) {
        const baseUrl = getBaseUrl(req);
        const packing = await this.prisma.packing_proofs.findMany({
            where: { isDeleted: 0 },
            include: {
                order: true,
            }
        });

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

    async sendMail(body: any) {
        await this.mailingService.sendTestEmail(body.to, body.name, body.confirmationLink);
        return { message: `Mail sent to ${body.to} successfully ^w^` };
    }    
}