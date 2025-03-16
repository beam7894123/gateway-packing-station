import { Module } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { PackingOrderService } from './packOrder.service';
import { PackingOrderController } from './packOrder.controller';
import { PickingStationService } from 'src/pickingStation/pickingStation.service';
import { MailingService } from 'src/service/mailing.service';


@Module({
  providers: [PackingOrderService, PickingStationService, MailingService ,PrismaService],
  exports: [PackingOrderService],
  controllers: [PackingOrderController],
})
export class PackingOrderModule {}
