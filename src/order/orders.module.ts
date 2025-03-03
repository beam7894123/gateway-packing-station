import { Module } from '@nestjs/common';
import { OrdersService } from './orders.service';
import { PrismaService } from 'src/prisma/prisma.service';
import { OrdersController } from './orders.controller';

@Module({
  providers: [OrdersService, PrismaService],
  exports: [OrdersService],
  controllers: [OrdersController],
})
export class OrdersModule {}
