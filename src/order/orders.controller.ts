import { Body, Controller, Get, Param, Patch, Post, Req, UploadedFile, UseInterceptors, Delete, Res } from '@nestjs/common';
import { Request, Response } from 'express';
import { OrdersService } from './orders.service';
import { OrderDto as OrderDto } from './dto/order.dto';

@Controller('orders')
export class OrdersController {
  constructor(private readonly ordersService: OrdersService) {}

    @Get('/')
    async getAllItems(@Req() req: Request) {
      return await this.ordersService.getAllOrders(req);
    }  

    @Get(':id')
    async getItemById(@Param('id') id: number,@Req() req: Request) {
        return await this.ordersService.getOrderById(id, req);
        }
    
    @Post('create')
  async createOrder(@Body() orderDto: OrderDto) {
    return await this.ordersService.createOrder(orderDto);
  }

    @Delete('/:id/delete')
    async softDeleteItem(@Param('id') id: number) {
      return await this.ordersService.softDeleteOrders(id);
  }

  @Get('/:id/picking-list')
    async getPickingListPdf(@Param('id') id: number, @Res() res: Response, @Req() req: Request) {
        return this.ordersService.generatePickingListPdf(id, res, req);
    }
}
