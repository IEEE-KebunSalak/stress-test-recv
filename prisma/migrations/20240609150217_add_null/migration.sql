-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_SensorReading" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "nodeId" INTEGER,
    "temperature" REAL,
    "humidity" REAL,
    "lux" REAL,
    "tips" INTEGER,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);
INSERT INTO "new_SensorReading" ("createdAt", "humidity", "id", "lux", "nodeId", "temperature", "tips", "updatedAt") SELECT "createdAt", "humidity", "id", "lux", "nodeId", "temperature", "tips", "updatedAt" FROM "SensorReading";
DROP TABLE "SensorReading";
ALTER TABLE "new_SensorReading" RENAME TO "SensorReading";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
