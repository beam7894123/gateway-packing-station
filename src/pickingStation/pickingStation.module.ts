import { Module } from '@nestjs/common';
import { PickingStationService } from './pickingStation.service';
import { PrismaService } from 'src/prisma/prisma.service';
import { PickingStationController } from './pickingStation.controller';

@Module({
  providers: [PickingStationService, PrismaService],
  exports: [PickingStationService],
  controllers: [PickingStationController],
})
export class PickingStationModule {}
