import { HttpException, HttpStatus, Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { Request } from 'express';
import { PickingStationService } from 'src/pickingStation/pickingStation.service';
import { getBaseUrl } from 'src/utils';

@Injectable()
export class PackingOrderService {
    constructor(private prisma: PrismaService,
        private readonly pickingStationService: PickingStationService
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
}