-- Migration: Initial schema for Dealcross

CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL PRIMARY KEY,
    "email" VARCHAR(255) UNIQUE NOT NULL,
    "username" VARCHAR(100) UNIQUE,
    "full_name" VARCHAR(255),
    "hashed_password" TEXT NOT NULL,
    "is_active" BOOLEAN NOT NULL DEFAULT TRUE,
    "is_superuser" BOOLEAN NOT NULL DEFAULT FALSE,
    "is_2fa_enabled" BOOLEAN DEFAULT FALSE,
    "totp_secret" VARCHAR(255),
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "transaction" (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "amount" DECIMAL(12, 2) NOT NULL,
    "currency" VARCHAR(10) DEFAULT 'USD',
    "status" VARCHAR(50) DEFAULT 'pending',
    "reference" VARCHAR(255) UNIQUE,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Required for Aerich migration tracking
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB
);