import { Module } from '@nestjs/common';
import { PickingStationService } from './pickingStation.service';
import { PrismaService } from 'src/prisma/prisma.service';
import { PickingStationController } from './pickingStation.controller';
import { PackingOrderService } from 'src/packOrder/packOrder.service';
import { MailingService } from 'src/service/mailing.service';

@Module({
  providers: [PickingStationService, PackingOrderService, PrismaService, MailingService],
  exports: [PickingStationService],
  controllers: [PickingStationController],
})
export class PickingStationModule {}
