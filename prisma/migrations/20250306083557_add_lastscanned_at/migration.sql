/*
  Warnings:

  - You are about to drop the column `scannedAt` on the `packing_scans_list` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "packing_scans_list" DROP COLUMN "scannedAt",
ADD COLUMN     "firstscannedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "lastscannedAt" TIMESTAMP(3);
