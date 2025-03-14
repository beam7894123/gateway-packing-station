import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { join } from 'path';
import { NestExpressApplication } from '@nestjs/platform-express';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);
  app.useGlobalPipes(
    new ValidationPipe({
      transform: true,
      whitelist: true,
    }),
  );

  app.useStaticAssets(join(__dirname, '..', 'assets'), {
    prefix: '/assets', // Serve static files from /uploads
  });

  app.enableCors({
    origin: process.env.FRONTEND_URL ?? 'http://localhost:8080',
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    allowedHeaders: 'Content-Type,Authorization',
    credentials: false, // If using cookies or authentication change to true!
  });

  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
