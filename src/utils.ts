import { BadRequestException } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { randomBytes } from 'crypto';
import { Request } from 'express';
import { diskStorage } from 'multer';
import { extname } from 'path';
import * as path from 'path';

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

// I already try to add progress bar for video upload but it's not working properly and I just wasted my 5hr on it. :<
// Maybe this might be helpful of anyone try to make it : https://mikelopster.dev/posts/upload-basic/#%E0%B9%80%E0%B8%A3%E0%B8%B4%E0%B9%88%E0%B8%A1%E0%B8%97%E0%B8%B3-api-upload-%E0%B9%81%E0%B8%A5%E0%B8%B0-upload-%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B8%9B%E0%B8%81%E0%B8%95%E0%B8%B4
export const videoUploadInterceptor = (fieldName: string) =>
  FileInterceptor(fieldName, {
    fileFilter: (req, file, callback) => {
       const allowedMimeTypes = ['video/mp4', 'video/mov', 'video/avi', 'video/webm'];
       if (!allowedMimeTypes.includes(file.mimetype)) {
         return callback(new BadRequestException('Only video files (MP4, MOV, AVI, WEBM) are allowed! >:<'), false);
       }
       callback(null, true);
     },
     storage: diskStorage({
       destination: './assets/uploads/videos',
        filename: (req, file, callback) => {
         const randomId = randomBytes(8).toString('hex');
         const ext = path.extname(file.originalname);
         callback(null, `${randomId}_${file.originalname}`);
       },
     }),
   });