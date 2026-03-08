# Guía de desarrollo — finanzas_gastos

Documentación técnica para desarrolladores. Cubre la instalación desde cero en un equipo nuevo, la arquitectura del proyecto y la descripción de cada componente.

Para el uso diario del importador, ver [INSTRUCCIONES.md](INSTRUCCIONES.md).

---

## Índice

1. [Requisitos del sistema](#1-requisitos-del-sistema)
2. [Instalación desde cero](#2-instalación-desde-cero)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Componente ETL — Importador](#4-componente-etl--importador)
5. [Componente API — FastAPI](#5-componente-api--fastapi)
6. [Base de datos](#6-base-de-datos)
7. [Variables de entorno](#7-variables-de-entorno)
8. [Cómo correr el proyecto](#8-cómo-correr-el-proyecto)
9. [Solución de problemas](#9-solución-de-problemas)
10. [Roadmap técnico](#10-roadmap-técnico)

---

## 1. Requisitos del sistema

Antes de instalar, asegurate de tener lo siguiente:

| Herramienta | Versión mínima      | Cómo verificar     |
| ----------- | ------------------- | ------------------ |
| Python      | 3.10+               | `python --version` |
| MySQL       | 8.0+                | `mysql --version`  |
| pip         | incluido con Python | `pip --version`    |

**Nota para distribuciones Linux:** El módulo `tkinter` para el selector gráfico de archivos no siempre viene incluido con Python. Instalarlo según el sistema:

```bash
# Fedora / RHEL / CentOS
sudo dnf install python3-tkinter

# Ubuntu / Debian
sudo apt install python3-tk
```

---

## 2. Instalación desde cero

### 2.1 Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd finanzas_gastos
```

### 2.2 Crear el entorno virtual del ETL

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 2.3 Instalar dependencias del ETL

```bash
pip install -r requirements.txt
```

### 2.4 Crear el entorno virtual de la API

```bash
python -m venv api/venv
source api/venv/bin/activate
pip install -r api/requirements.txt
deactivate
```

### 2.5 Configurar las credenciales

Copiá el archivo de ejemplo y completá los valores:

```bash
cp .env.example .env
```

Editá `.env` con tus datos reales (ver sección [Variables de entorno](#7-variables-de-entorno)).

### 2.6 Crear la base de datos

Con MySQL corriendo, ejecutá:

```bash
mysql -u root -p < db/schemas.sql
```

Esto crea la base de datos `finanzas_gastos` y la tabla `movimientos`.

### 2.7 Verificar la instalación

```bash
source venv/bin/activate
python main.py
```

Debería abrirse la ventana para seleccionar un archivo del banco.

---

## 3. Estructura del proyecto

```
finanzas_gastos/
│
├── main.py                  ← punto de entrada del importador
├── requirements.txt         ← dependencias del ETL
├── .env                     ← credenciales (no se sube a Git)
├── .env.example             ← plantilla de credenciales
│
├── scripts/
│   ├── parse_excel.py       ← parser de archivos Excel del BROU
│   └── save_mysql.py        ← guarda los datos en MySQL
│
├── db/
│   ├── schemas.sql          ← crea la DB y la tabla
│   └── reset.sql            ← vacía la tabla (uso en desarrollo)
│
├── data/
│   ├── raw/                 ← archivos originales del banco (excluidos de Git)
│   └── processed/
│       └── movimientos.csv  ← CSV intermedio generado por los parsers
│
├── api/
│   ├── main.py              ← aplicación FastAPI
│   ├── auth.py              ← autenticación JWT
│   ├── db.py                ← conexión a MySQL
│   ├── requirements.txt     ← dependencias de la API
│   ├── venv/                ← entorno virtual de la API (excluido de Git)
│   └── routes/
│       └── movimientos.py   ← endpoints de movimientos
│
├── venv/                    ← entorno virtual del ETL (excluido de Git)
│
├── README.MD
├── INSTRUCCIONES.md         ← guía del usuario final
└── DESARROLLO.md            ← esta guía
```

---

## 4. Componente ETL — Importador

El flujo del importador sigue el patrón **ETL (Extract → Transform → Load)**:

```
Archivo del banco (.xls / .xlsx)
            ↓
       main.py detecta la extensión
            ↓
        parse_excel.py
            ↓
    CSV temporal en data/processed/
            ↓
       save_mysql.py inserta en MySQL
            ↓
      ✓ Proceso completado
```

### `main.py`

Punto de entrada único. Acepta la ruta del archivo como argumento CLI o abre un selector gráfico con `tkinter`. Si `tkinter` no está disponible, cae a entrada por terminal.

```bash
python main.py                                         # selector gráfico
python main.py /ruta/al/archivo/movimientos.xls        # argumento directo
```

---

### `scripts/parse_excel.py`

**Función:** `parse(input_path: str, output_path: str)`

Los extractos del BROU contienen ~35 filas de metadata de cabecera antes de los datos reales. El parser detecta dinámicamente la fila de encabezado buscando la celda con el texto `"Fecha"`.

Columnas exportadas: `fecha`, `descripcion`, `documento`, `dependencia`, `debito`, `credito`

Decisiones técnicas:

- `_encontrar_fila_header()` escanea fila por fila hasta encontrar la celda `"Fecha"`
- Filas de pie de página se eliminan filtrando con `pd.to_datetime(errors='coerce')`
- `NaN` se convierte a `None` con `df.astype(object).where(pd.notnull(df), None)` para que MySQL los registre como `NULL`

---

### `scripts/save_mysql.py`

**Función:** `save(csv_path: str)`

Lee el CSV generado por el parser e inserta cada fila en la tabla `movimientos`. Las credenciales se leen desde `.env` con `python-dotenv`.

---

## 5. Componente API — FastAPI

La API expone los datos de MySQL con autenticación JWT. Es opcional — el importador funciona sin necesidad de correr la API.

### Endpoints

| Método | Ruta                   | Descripción                                          | Auth |
| ------ | ---------------------- | ---------------------------------------------------- | ---- |
| `POST` | `/auth/login`          | Obtiene token JWT                                    | No   |
| `GET`  | `/health`              | Estado de la API                                     | No   |
| `GET`  | `/movimientos`         | Lista movimientos (filtrable por mes `?mes=YYYY-MM`) | Sí   |
| `GET`  | `/movimientos/meses`   | Meses disponibles en la base de datos                | Sí   |
| `GET`  | `/movimientos/resumen` | Totales de débito y crédito por mes                  | Sí   |

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=admin&password=tu_password" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

Devuelve: `{"access_token": "eyJ...", "token_type": "bearer"}`

### Correr la API

```bash
source api/venv/bin/activate
uvicorn api.main:app --port 8000 --reload
```

O sin activar el venv:

```bash
./api/venv/bin/uvicorn api.main:app --port 8000 --reload
```

La API queda disponible en `http://localhost:8000`. Documentación interactiva en `http://localhost:8000/docs`.

---

## 6. Base de datos

### Esquema

```sql
CREATE DATABASE IF NOT EXISTS finanzas_gastos;

USE finanzas_gastos;

CREATE TABLE IF NOT EXISTS movimientos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    fecha       DATE,
    descripcion TEXT,
    documento   VARCHAR(50),
    dependencia VARCHAR(100),
    debito      DECIMAL(12,2),
    credito     DECIMAL(12,2),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Resetear datos (solo en desarrollo)

```bash
mysql -u root -p finanzas_gastos < db/reset.sql
```

Esto ejecuta `TRUNCATE TABLE movimientos` — borra todos los registros pero mantiene la estructura.

### Consultas útiles

```sql
-- Ver todos los movimientos
SELECT fecha, descripcion, debito, credito
FROM movimientos
ORDER BY fecha DESC;

-- Resumen por mes
SELECT DATE_FORMAT(fecha, '%Y-%m') AS mes,
       SUM(debito) AS total_debito,
       SUM(credito) AS total_credito
FROM movimientos
GROUP BY mes
ORDER BY mes DESC;
```

---

## 7. Variables de entorno

Todas las credenciales se configuran en el archivo `.env` en la raíz del proyecto. Nunca se sube a Git.

```ini
# Base de datos MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
DB_NAME=finanzas_gastos

# Credenciales de la API REST
API_USER=admin
API_PASSWORD=tu_password_aqui

# JWT — cambiar por una clave larga y aleatoria en producción
JWT_SECRET=una_clave_larga_y_aleatoria_minimo_32_caracteres
JWT_EXPIRE_MINUTES=480
```

Generar un `JWT_SECRET` seguro:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 8. Cómo correr el proyecto

### Solo el importador ETL

```bash
source venv/bin/activate
python main.py
```

### API

```bash
./api/venv/bin/uvicorn api.main:app --port 8000 --reload
```

---

## 9. Solución de problemas

| Error                                               | Causa probable                                 | Solución                                                                             |
| --------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------ |
| `ModuleNotFoundError: tkinter`                      | tkinter no instalado                           | `sudo dnf install python3-tkinter` (Fedora) o `sudo apt install python3-tk` (Ubuntu) |
| `ModuleNotFoundError: xlrd`                         | Dependencia faltante                           | `pip install xlrd` dentro del venv del ETL                                           |
| `KeyError: 'fecha'`                                 | El Excel no tiene el formato esperado del BROU | Verificar que el archivo sea el exportado directamente del homebanking BROU          |
| `Unknown column 'nan'` en MySQL                     | Valores vacíos no convertidos                  | Ya corregido en `save_mysql.py` con `df.astype(object).where(pd.notnull(df), None)`  |
| `Access denied for user` en MySQL                   | Credenciales incorrectas                       | Revisar `DB_USER` y `DB_PASSWORD` en `.env`                                          |
| `RuntimeError: Form data requires python-multipart` | Dependencia faltante en API                    | `pip install python-multipart` dentro de `api/venv`                                  |
| `401 Unauthorized` en la API                        | Token expirado o credenciales incorrectas      | Re-autenticarse en `/auth/login`; verificar `API_USER`/`API_PASSWORD` en `.env`      |

---

## 10. Roadmap técnico

### Clasificación automática de gastos

Mapear descripciones conocidas a categorías usando una tabla `categorias` en MySQL:

```
DISCO       → supermercado
ANTEL       → telecomunicaciones
DISA        → combustible
```

### Soporte para múltiples bancos

Agregar parsers específicos por banco en `scripts/`:

- `parse_excel_brou.py` (actual)
- `parse_excel_itau.py`
- `parse_excel_santander.py`

### Dashboard web con gráficos

Extender el frontend existente en `web/` con:

- Gráfico de barras por mes (recharts o chart.js)
- Torta de distribución por categoría
- Buscador / filtro por descripción
