/*
  Warnings:

  - You are about to drop the column `isSuccessfully` on the `packing_proofs` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "packing_proofs" DROP COLUMN "isSuccessfully",
ADD COLUMN     "status" INTEGER NOT NULL DEFAULT 0;
