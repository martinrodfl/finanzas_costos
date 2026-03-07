CREATE DATABASE IF NOT EXISTS finanzas_gastos;

USE finanzas_gastos;

CREATE TABLE IF NOT EXISTS movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    descripcion TEXT,
    documento VARCHAR(50),
    dependencia VARCHAR(100),
    debito DECIMAL(12,2),
    credito DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);