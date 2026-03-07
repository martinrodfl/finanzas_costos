-- ============================================================
-- RESET de base de datos — solo para uso en desarrollo
-- Borra todos los registros y reinicia el auto_increment
--
-- Uso:
--   mysql -u root -p finanzas_gastos < db/reset.sql
-- ============================================================

USE finanzas_gastos;

TRUNCATE TABLE movimientos;
