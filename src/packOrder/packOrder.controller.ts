import { Body, Controller, Delete, Get, Param, Post, Req, UploadedFile, UseInterceptors } from '@nestjs/common';
import { Request } from 'express';
import { PackingOrderService } from './packOrder.service';

@Controller('packing')
export class PackingOrderController {
  constructor(
    private readonly packingOrderService: PackingOrderService,
  ) {}
    @Get('/')
    async getAllItems(@Req() req: Request) {
      return await this.packingOrderService.getAllOrders(req);
    }  

    @Get(':id')
    async getItemById(@Param('id') id: number,@Req() req: Request) {
        return await this.packingOrderService.getOrderById(id, req);
    }

    @Delete(':id/delete')
    async deleteScan(@Param('id') id: number) {
        return this.packingOrderService.softDeletePackingProof(id);
    }

    @Post(':id/mail/send')
    async sendProofToMailById(@Param('id') id: number, @Req() req: Request) {
        return await this.packingOrderService.sendProofToMailById(id, req);
    }
}