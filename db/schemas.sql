CREATE DATABASE IF NOT EXISTS finanzas_gastos;

USE finanzas_gastos;

CREATE TABLE IF NOT EXISTS movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    descripcion TEXT,
    documento VARCHAR(50),
    asunto TEXT,
    dependencia VARCHAR(100),
    debito DECIMAL(12,2),
    credito DECIMAL(12,2),
    categoria_manual VARCHAR(50) NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categoria_reglas (
    descripcion VARCHAR(500) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (descripcion(255))
);

