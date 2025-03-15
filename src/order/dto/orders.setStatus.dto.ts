import { IsNumber } from 'class-validator';

export class OrderSetStatusDto {
  @IsNumber()
  status: number;
}