import { Module } from '@nestjs/common';
import { ItemsService } from './items.service';
import { PrismaService } from 'src/prisma/prisma.service';
import { ItemsController } from './items.controller';

@Module({
  providers: [ItemsService, PrismaService],
  exports: [ItemsService],
  controllers: [ItemsController],
})
export class ItemsModule {}
