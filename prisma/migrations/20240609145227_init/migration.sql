-- CreateTable
CREATE TABLE "SensorReading" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nodeId" INTEGER NOT NULL,
    "temperature" REAL NOT NULL,
    "humidity" REAL NOT NULL,
    "lux" REAL NOT NULL,
    "tips" INTEGER NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);
