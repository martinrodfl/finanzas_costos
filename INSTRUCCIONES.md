# Guía de uso — Importador de Movimientos Bancarios

> Esta guía es para el **uso diario** del sistema, asumiendo que ya fue instalado y configurado correctamente.  
> Si es la primera vez que instalás el proyecto en un equipo nuevo, consultá [DESARROLLO.md](DESARROLLO.md) primero.

---

## Cómo usar el sistema

### Paso 1 — Descargá el archivo del banco

1. Ingresá al **homebanking del BROU**
2. Andá a **Movimientos** → **Exportar / Descargar**
3. Elegí el formato **Excel (.xls)**
4. Guardalo donde quieras (Descargas, Escritorio, o cualquier carpeta)

---

### Paso 2 — Ejecutá el sistema

Desde la carpeta del proyecto, un solo comando hace todo:

```bash
./main.py
```

Eso es todo. El script se encarga de:

1. Abrir una **ventana para seleccionar el archivo** del banco
2. **Parsear** el archivo y guardar los movimientos en la base de datos
3. **Levantar el backend** (API en `http://localhost:8000`) si no estaba corriendo
4. **Levantar el frontend** (web en `http://localhost:5173`) si no estaba corriendo
5. **Abrir el navegador** automáticamente con la aplicación lista

> **No necesitás activar el entorno virtual, ni levantar servidores manualmente.** Todo se hace solo.

---

### Resultado esperado en la terminal

```
=== Importador de Movimientos Bancarios ===

Archivo detectado: Detalle_Movimiento_Cuenta.xls
Excel procesado: 39 registros → data/processed/movimientos.csv
39 registros nuevos guardados en MySQL. (0 ya existían, omitidos)

✓ Proceso completado exitosamente.

— Levantando servicios —
  Backend iniciado en http://localhost:8000
  Frontend iniciado en http://localhost:5173
  Navegador abierto. ¡Listo!
```

Si ejecutás el script una segunda vez (para importar otro mes), los servicios ya están corriendo y no se duplican.

---

## Uso avanzado

Si preferís pasar la ruta del archivo directamente sin que se abra la ventana:

```bash
./main.py /ruta/al/archivo/movimientos.xls
```

---

## Solución de problemas

| Problema                          | Qué hacer                                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| No se abre la ventana de archivos | Instalá tkinter: `sudo dnf install python3-tkinter` (Fedora) o `sudo apt install python3-tk` (Ubuntu/Debian) |
| `ModuleNotFoundError`             | Ejecutá `source venv/bin/activate && pip install -r requirements.txt`                                        |
| La web no carga datos             | Verificá que MySQL esté corriendo. El backend estará en `http://localhost:8000`                              |
| `Error de conexión a MySQL`       | Verificá que MySQL esté corriendo y que las credenciales en `.env` sean correctas                            |
| El archivo no es reconocido       | El sistema solo acepta `.xls` o `.xlsx`. Exportá desde el BROU en formato **Excel**                          |
| Los servicios no levantan         | Revisá que el puerto 8000 y 5173 estén libres: `ss -tlnp \| grep -E '8000\|5173'`                            |

---

## Notas de seguridad

- El archivo `.env` con tus credenciales **nunca se sube a Git** (está en `.gitignore`)
- Los archivos del banco se guardan en `data/` que también está excluida del repositorio
- No compartas el archivo `.env` con nadie
