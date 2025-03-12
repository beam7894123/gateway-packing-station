/*
  Warnings:

  - A unique constraint covering the columns `[itemCode]` on the table `items` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "items_itemCode_key" ON "items"("itemCode");
