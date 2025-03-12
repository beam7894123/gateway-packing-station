import { Body, Controller, Delete, Get, Param, Post, Req, UploadedFile, UseInterceptors } from '@nestjs/common';
import { Request } from 'express';
import { PickingStationService } from './pickingStation.service';
import { StationDto } from './dto/station.dto';
import { videoUploadInterceptor } from 'src/utils';

@Controller('packing-station')
export class PickingStationController {
  constructor(
    private readonly pickingStationService: PickingStationService,
  ) {}

  @Get('/heartbeat')
  checkHeartbeat() {
    return { 
      status: 'OK',
      statusCode: 200,
      message: "Yeah I'm good bro :3",
      timestamp: new Date().toISOString() };
  }

  @Post('/start')
  async startScan(@Body() data: StationDto, @Req() req: Request) {
    // return this.pickingStationService.startScan(data, req);
    return this.pickingStationService.restartScan(data, req); // So the old order can be scanned again
  }

  @Post('/item')
  async addScannedItem(@Body() data: StationDto, @Req() req: Request) {
    return this.pickingStationService.scannedItem(data, req);
  }

  @Post('/finish')
  @UseInterceptors(videoUploadInterceptor('video'))
  async finishScan(@Body() data: StationDto, @UploadedFile() video?: Express.Multer.File) {
    if (!video) {
      return this.pickingStationService.finishScan(data); // No video uploaded :<
    }

    const videoPath = `/assets/uploads/videos/${video.filename}`;

    return await this.pickingStationService.finishScan({
      ...data,
      video: videoPath,
    });
  }

  @Post('/restart')
  async restartScan(@Body() data: StationDto, @Req() req: Request) {
    return this.pickingStationService.restartScan(data, req);
  }

  @Delete('/delete/:id')
  async deleteScan(@Param('id') id: number,) {
    return this.pickingStationService.softDeletePackingProof(id);
  }

  @Get('/check/order/:id')
  async checkPackingProof(@Param('id') id: number, @Req() req: Request) {
    return this.pickingStationService.checkOrderPackingProof(id, req);
  }

  @Get('/check/items/:id')
  async checkScan(@Param('id') id: number, @Req() req: Request) {
    return this.pickingStationService.checkScannedAndUnscannedItems(id, req);
  }

  @Get('/')
      async getAllItems(@Req() req: Request) {
        // return await this.pickingStationService.getAllwaiting(req);
        return 'Meow :3';
      }

  @Post('/TEST')
  async test(@Body() data: any, @Req() req: Request) {
    return this.pickingStationService.getScannedAndUnscannedItems(data, req);
  }
}
