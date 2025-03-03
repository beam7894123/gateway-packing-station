import { IsString, IsOptional, IsInt, IsNumberString, IsPositive, IsNumber } from 'class-validator';
import { Transform } from 'class-transformer';

export class ItemDto {
  @IsOptional()
  @IsString()
  itemCode: string;

  @IsOptional()
  @IsString()
  name: string;

  @IsOptional()
  @IsString()
  description?: string;

  @IsOptional()
  @IsNumber()
  @IsPositive()
  @Transform(({ value }) => parseFloat(value))
  price?: number;

  @IsOptional()
  @IsNumber()
  @IsPositive()
  @Transform(({ value }) => parseInt(value))
  quantity?: number;

  @IsOptional()
  @IsString()
  image?: string | null; // This will store the image URL after file upload

  @IsOptional()
  @IsNumber()
  @IsPositive()
  @Transform(({ value }) => parseInt(value))
  createdUser: number;
}