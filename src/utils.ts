import { BadRequestException } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { randomBytes } from 'crypto';
import { Request } from 'express';
import { diskStorage } from 'multer';
import { extname } from 'path';

export function getBaseUrl(req: Request): string {
  const protocol = req.headers['x-forwarded-proto'] || req.protocol;
  return process.env.BASE_URL || `${protocol}://${req.get('host')}`;
}

export const imageUploadInterceptor = (fieldName: string) =>
  FileInterceptor(fieldName, {
    fileFilter: (req, file, callback) => {
      const allowedMimeTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!allowedMimeTypes.includes(file.mimetype)) {
        return callback(new BadRequestException('Only image files (JPG, PNG, GIF) are allowed! >:<'), false); // PLZ ADD WEBP SUPPORT!!! >m< <--------------------------
      }
      callback(null, true);
    },
    storage: diskStorage({
      destination: './assets/uploads/image',
      filename: (req, file, callback) => {
        const randomId = randomBytes(8).toString('hex');
        const ext = extname(file.originalname);
        callback(null, `${randomId}_${file.originalname}`);
      },
    }),
  });