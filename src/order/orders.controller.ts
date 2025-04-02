import { Body, Controller, Get, Param, Patch, Post, Req, UploadedFile, UseInterceptors, Delete, Res, Query } from '@nestjs/common';
import { Request, Response } from 'express';
import { OrdersService } from './orders.service';
import { OrderDto as OrderDto } from './dto/order.dto';
import { OrderSetStatusDto } from './dto/orders.setStatus.dto';

@Controller('orders')
export class OrdersController {
  constructor(private readonly ordersService: OrdersService) {}

  @Get('/')
    async getAllItems(@Req() req: Request,
      @Query('status') status?: string,
      @Query('createdAt') createdAt?: string,
      @Query('startDate') startDate?: string,
      @Query('endDate') endDate?: string,
    ) {
      return await this.ordersService.getAllOrders(req, { status, createdAt, startDate, endDate });
    }  

  @Get(':id')
    async getItemById(@Param('id') id: number,@Req() req: Request) {
        return await this.ordersService.getOrderById(id, req);
        }
    
  @Post('create')
    async createOrder(@Body() orderDto: OrderDto) {
      return await this.ordersService.createOrder(orderDto);
  }

  @Patch('/:id/update')
    async updateOrder(@Param('id') id: number, @Body() orderDto: OrderDto) {
      return await this.ordersService.updateOrder(id, orderDto);
  }

  @Patch('/:id/set/status')
    async setStatusOrder(@Param('id') id: number, @Body() setStatusDto: OrderSetStatusDto) {
      return await this.ordersService.setStatusOrder(id, setStatusDto);
  }

  @Delete('/:id/delete')
    async softDeleteItem(@Param('id') id: number) {
      return await this.ordersService.softDeleteOrders(id);
  }

  @Get('/:id/picking-list')
    async getPickingListPdf(@Param('id') id: number, @Res() res: Response, @Req() req: Request) {
        return this.ordersService.generatePickingListPdf(id, res, req);
    }

  @Get('/:id/record-video')
    async getRecordVideo(@Param('id') id: number, @Res() res: Response, @Req() req: Request) {
        return this.ordersService.getRecordVideo(id, res, req);
    }
}
