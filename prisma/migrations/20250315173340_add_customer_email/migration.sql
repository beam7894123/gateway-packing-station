-- AlterTable
ALTER TABLE "orders" ADD COLUMN     "customerEmail" TEXT,
ALTER COLUMN "customer" SET DEFAULT 'Guest';
