import { Body, Controller, Get, Param, Patch, Post, Req, UploadedFile, UseInterceptors, Delete } from '@nestjs/common';
import { Request } from 'express';
import { ItemsService } from './items.service';
import { ItemDto as ItemDto } from './dto/item.dto';
import { imageUploadInterceptor } from 'src/utils';

@Controller('items')
export class ItemsController {
  constructor(private readonly itemsService: ItemsService) {}

    @Get('/')
    async getAllItems(@Req() req: Request) {
      return await this.itemsService.getAllItems(req);
    }  

    @Get(':id')
    async getItemById(@Param('id') id: number,@Req() req: Request) {
        return await this.itemsService.getItemById(id, req);
        }
    
    @Post('/create')
    @UseInterceptors(imageUploadInterceptor('image'))
      async createItem(@UploadedFile() file: Express.Multer.File, @Body() data: ItemDto) {
        const imageUrl = file ? `/assets/uploads/image/${file.filename}` : null;
        return await this.itemsService.createItem({ ...data, image: imageUrl });
      }

    @Patch(':id/update')
    @UseInterceptors(imageUploadInterceptor('image'))
    async updateItem(
      @Param('id') id: number,
      @Body() data: ItemDto,
      @UploadedFile() file: Express.Multer.File,
      @Req() req: Request
    ) {
      return await this.itemsService.updateItem(Number(id), data, file, req);
    }

    @Delete('/:id/delete')
    async softDeleteItem(@Param('id') id: number) {
      return await this.itemsService.softDeleteItem(id);
  }
}
