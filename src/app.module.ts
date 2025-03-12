import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { ItemsModule } from './items/items.module';
import { OrdersModule } from './order/orders.module';
import { PickingStationModule } from './pickingStation/pickingStation.module';

@Module({
  imports: [AuthModule, UsersModule, ItemsModule, OrdersModule, PickingStationModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
