import * as fs from 'fs';
import * as path from 'path';
import { env } from 'process';
import { Injectable } from '@nestjs/common';
import * as nodemailer from 'nodemailer';
import * as handlebars from 'handlebars';

@Injectable()
export class MailingService {
  private transporter: nodemailer.Transporter;
  private confirmationTemplate: handlebars.TemplateDelegate;
  private packingProofTemplate: handlebars.TemplateDelegate;

  constructor() {
    this.transporter = nodemailer.createTransport({
      host: env.MAIL_HOST,
      port: Number(env.MAIL_PORT),
      secure: env.MAILER_SECURE === 'true',
      auth: {
        user: env.MAIL_USER,
        pass: env.MAIL_PASSWORD,
      },
    });

    // Load Handlebars templates
    const confirmationTemplatePath = path.join(__dirname, '../../src/service/mailTemplates', 'confirmation.hbs');
    const packingProofTemplatePath = path.join(__dirname, '../../src/service/mailTemplates', 'proofOfPacking.hbs');

    this.confirmationTemplate = handlebars.compile(fs.readFileSync(confirmationTemplatePath, 'utf8'));
    this.packingProofTemplate = handlebars.compile(fs.readFileSync(packingProofTemplatePath, 'utf8'));

  }

  async sendTestEmail(to: string, name: string, confirmationLink: string) {
    const htmlContent = this.confirmationTemplate({ name, confirmationLink });
  
    const mailOptions = {
      from: env.MAIL_USER, // Sender
      to, // Recipient
      subject: 'Confirm Your Email',
      html: htmlContent, // Rendered Handlebars template
    };
  
    try {
      const info = await this.transporter.sendMail(mailOptions);
      console.log('Email sent:', info.messageId);
      return { success: true, message: 'Email sent successfully!' };
    } catch (error) {
      console.error('Error sending email:', error);
      return { success: false, message: 'Failed to send email.' };
    }
  }  

  async sendPackingProofEmail(to: string, customerName: string, orderId: number, proofVideoUrl: string) {
    const emailHtml = this.packingProofTemplate({
        customerName,
        orderId,
        proofVideoUrl,
        year: new Date().getFullYear(),
    });

    await this.transporter.sendMail({
        from: env.MAIL_USER,
        to,
        subject: `Proof of Packing for Order #${orderId}`,
        html: emailHtml,
    });
  }
}