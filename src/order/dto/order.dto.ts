import { IsArray, IsInt, IsNotEmpty, IsOptional, IsString } from 'class-validator';

export class OrderDto {
  @IsString()
  @IsNotEmpty()
  customer: string;

  @IsString()
  @IsOptional()
  trackingNumber: string;

  @IsArray()
  @IsNotEmpty()
  items: { itemId: number; quantity: number }[];
}