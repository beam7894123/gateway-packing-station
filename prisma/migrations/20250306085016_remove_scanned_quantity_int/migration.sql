/*
  Warnings:

  - You are about to drop the column `firstscannedAt` on the `packing_scans_list` table. All the data in the column will be lost.
  - You are about to drop the column `lastscannedAt` on the `packing_scans_list` table. All the data in the column will be lost.
  - You are about to drop the column `scannedQuantity` on the `packing_scans_list` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "packing_scans_list" DROP COLUMN "firstscannedAt",
DROP COLUMN "lastscannedAt",
DROP COLUMN "scannedQuantity",
ADD COLUMN     "scannedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- CreateIndex
CREATE INDEX "packing_scans_list_orderId_idx" ON "packing_scans_list"("orderId");

-- CreateIndex
CREATE INDEX "packing_scans_list_itemId_idx" ON "packing_scans_list"("itemId");
