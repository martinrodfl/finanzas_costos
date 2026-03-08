@echo off
title Instalacion - Importador de Movimientos BROU
cd /d "%~dp0"

echo =================================================
echo   Instalacion - Importador de Movimientos BROU
echo =================================================
echo.

:: --- Verificar Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python 3.10+ desde https://www.python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo [OK] %%v

:: --- Verificar Node/npm ---
where npm >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm no encontrado. Instala Node.js desde https://nodejs.org
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('npm --version') do echo [OK] npm %%v

:: --- Verificar MySQL ---
set PATH=%PATH%;C:\Program Files\MySQL\MySQL Server 8.0\bin
where mysql
if errorlevel 1 (
    echo [ERROR] mysql no encontrado en el PATH.
    echo         Agrega MySQL al PATH o ejecuta desde MySQL Shell.
    pause
    exit /b 1
)
echo [OK] MySQL encontrado

:: --- Credenciales ---
echo.
echo --- Ingresa las credenciales ---
echo.
set /p DB_USER=Usuario MySQL [default: root]: 
if "%DB_USER%"=="" set DB_USER=root
set /p DB_PASSWORD=Contrasena MySQL: 
set /p DB_HOST=Host MySQL [default: localhost]: 
if "%DB_HOST%"=="" set DB_HOST=localhost
set /p API_PASSWORD=Contrasena para la API REST: 

for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do set JWT_SECRET=%%i

:: --- Entorno virtual ETL ---
echo.
echo --- Entorno virtual ETL ---
if exist venv\Scripts\python.exe (
    echo [SKIP] venv ETL ya existe
) else (
    echo Creando venv ETL...
    python -m venv venv
    if errorlevel 1 ( echo [ERROR] No se pudo crear venv ETL & pause & exit /b 1 )
    echo [OK] venv ETL creado
)
echo Instalando dependencias ETL...
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\pip install -r requirements.txt
if errorlevel 1 ( echo [ERROR] Fallo pip install requirements.txt & pause & exit /b 1 )
echo [OK] Dependencias ETL instaladas

:: --- Entorno virtual API ---
echo.
echo --- Entorno virtual API ---
if exist api\venv\Scripts\python.exe (
    echo [SKIP] venv API ya existe
) else (
    echo Creando venv API...
    python -m venv api\venv
    if errorlevel 1 ( echo [ERROR] No se pudo crear venv API & pause & exit /b 1 )
    echo [OK] venv API creado
)
echo Instalando dependencias API...
api\venv\Scripts\python -m pip install --upgrade pip
api\venv\Scripts\pip install -r api\requirements.txt
if errorlevel 1 ( echo [ERROR] Fallo pip install api\requirements.txt & pause & exit /b 1 )
echo [OK] Dependencias API instaladas

:: --- Frontend ---
echo.
echo --- Frontend (npm install) ---
cd web
npm install
if errorlevel 1 ( echo [ERROR] Fallo npm install & cd .. & pause & exit /b 1 )
cd ..
echo [OK] Frontend instalado

:: --- Archivo .env ---
echo.
echo --- Archivo .env ---
if exist .env (
    echo [SKIP] .env ya existe, no se sobreescribe
) else (
    (
        echo DB_HOST=%DB_HOST%
        echo DB_USER=%DB_USER%
        echo DB_PASSWORD=%DB_PASSWORD%
        echo DB_NAME=finanzas_gastos
        echo.
        echo API_USER=admin
        echo API_PASSWORD=%API_PASSWORD%
        echo.
        echo JWT_SECRET=%JWT_SECRET%
        echo JWT_EXPIRE_MINUTES=480
    ) > .env
    echo [OK] .env creado
)

:: --- Base de datos MySQL ---
echo.
echo --- Base de datos MySQL ---
mysql -u %DB_USER% -p%DB_PASSWORD% -h %DB_HOST% < db\schemas.sql
if errorlevel 1 (
    echo [AVISO] No se pudo crear la DB automaticamente.
    echo         Ejecuta manualmente: mysql -u root -p ^< db\schemas.sql
) else (
    echo [OK] Base de datos creada
)

:: --- Carpetas necesarias ---
if not exist data\processed mkdir data\processed
if not exist data
aw mkdir data
aw
if not exist logs mkdir logs
echo [OK] Carpetas creadas

:: --- Listo ---
echo.
echo =================================================
echo   Instalacion completada exitosamente!
echo =================================================
echo.
echo Para usar el sistema ejecuta:   run.bat
echo.
pause