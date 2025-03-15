import { IsArray, IsInt, IsNotEmpty, IsNumber, IsOptional, IsString } from 'class-validator';
import { Transform } from 'class-transformer';

export class OrderDto {
  @IsString()
  @IsNotEmpty()
  customer: string;

  @IsString()
  @IsNotEmpty()
  customerEmail: string;

  @IsString()
  @IsOptional()
  trackingNumber: string;

  @IsNumber()
  @IsOptional()
  @Transform(({ value }) => parseInt(value))
  status: number;

  @IsArray()
  @IsNotEmpty()
  items: { itemId: number; quantity: number }[];
}