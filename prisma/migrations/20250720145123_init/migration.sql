-- CreateTable
CREATE TABLE "TickerData" (
    "id" TEXT NOT NULL,
    "datetime" TIMESTAMP(3) NOT NULL,
    "open" DECIMAL(65,30) NOT NULL,
    "high" DECIMAL(65,30) NOT NULL,
    "low" DECIMAL(65,30) NOT NULL,
    "close" DECIMAL(65,30) NOT NULL,
    "volume" INTEGER NOT NULL,

    CONSTRAINT "TickerData_pkey" PRIMARY KEY ("id")
);
