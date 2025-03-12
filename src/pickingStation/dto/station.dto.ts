import { IsInt, IsNotEmpty, IsOptional, IsPositive, IsString } from 'class-validator';
import { Transform } from 'class-transformer';

export class StationDto {
    @IsInt()
    @IsPositive()
    @Transform(({ value }) => parseInt(value))
    orderId: number;

    @IsString()
    @IsNotEmpty()
    station: string;

    @IsInt()
    @IsPositive()
    @IsOptional()
    @Transform(({ value }) => parseInt(value))
    status?: number;

    @IsOptional()
    @IsString()
    video?: string;

    @IsOptional()
    @IsString()
    itemCode?: string;
}
