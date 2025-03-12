/*
  Warnings:

  - You are about to drop the column `startTime` on the `packing_proofs` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "packing_proofs" DROP COLUMN "startTime",
ALTER COLUMN "video" DROP NOT NULL;
