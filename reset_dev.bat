@echo off
title Reset desarrollo - Importador BROU
cd /d "%~dp0"

echo =================================================
echo   Reset desarrollo - Importador BROU
echo =================================================
echo.
echo Esto borrara:
echo   - venv\
echo   - api\venv\
echo   - web\node_modules\
echo   - data\
echo   - logs\
echo   - .env
echo.
echo El codigo fuente NO se toca.
echo.
set /p CONFIRM=Confirmas? (s/N): 
if /i not "%CONFIRM%"=="s" (
    echo Cancelado.
    pause & exit /b 0
)

echo.
if exist venv (
    rmdir /s /q venv
    echo [OK] venv\ eliminado
) else (
    echo [SKIP] venv\ no existe
)

if exist api\venv (
    rmdir /s /q api\venv
    echo [OK] api\venv\ eliminado
) else (
    echo [SKIP] api\venv\ no existe
)

if exist web\node_modules (
    rmdir /s /q web\node_modules
    echo [OK] web\node_modules\ eliminado
) else (
    echo [SKIP] web\node_modules\ no existe
)

if exist data (
    rmdir /s /q data
    echo [OK] data\ eliminado
) else (
    echo [SKIP] data\ no existe
)

if exist logs (
    rmdir /s /q logs
    echo [OK] logs\ eliminado
) else (
    echo [SKIP] logs\ no existe
)

if exist .env (
    del .env
    echo [OK] .env eliminado
) else (
    echo [SKIP] .env no existe
)

echo.
echo =================================================
echo   Reset completado. Corre install.bat para reinstalar.
echo =================================================
echo.
pause
