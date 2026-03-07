# Guía de uso — Importador de Movimientos Bancarios

> Esta guía es para el **uso diario** del sistema, asumiendo que ya fue instalado y configurado correctamente.  
> Si es la primera vez que instalás el proyecto en un equipo nuevo, consultá [DESARROLLO.md](DESARROLLO.md) primero.

---

## Cómo importar tus movimientos

### Paso 1 — Descargá el archivo del banco

1. Ingresá al **homebanking del BROU**
2. Andá a **Movimientos** → **Exportar / Descargar**
3. Elegí el formato **Excel (.xls)** o **PDF**
4. Guardalo donde quieras (Descargas, Escritorio, o cualquier carpeta)

---

### Paso 2 — Ejecutá el importador

Desde la carpeta del proyecto:

```bash
python main.py
```

Se abrirá una **ventana para seleccionar el archivo**. Navegá hasta donde guardaste el archivo, seleccionalo y hacé clic en **Abrir**.

El sistema lo procesa automáticamente y guarda los movimientos en la base de datos.

---

### Resultado esperado

```
=== Importador de Movimientos Bancarios ===

Archivo detectado: Detalle_Movimiento_Cuenta.xls
Excel procesado: 39 registros → data/processed/movimientos.csv
39 registros guardados en MySQL.

✓ Proceso completado exitosamente.
```

---

## Uso avanzado

Si preferís pasar la ruta del archivo directamente sin que se abra la ventana:

```bash
python main.py /ruta/al/archivo/movimientos.xls
```

---

## Solución de problemas

| Problema                          | Qué hacer                                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| No se abre la ventana de archivos | Instalá tkinter: `sudo dnf install python3-tkinter` (Fedora) o `sudo apt install python3-tk` (Ubuntu/Debian) |
| `ModuleNotFoundError`             | Activá el entorno virtual (`source venv/bin/activate`) y ejecutá `pip install -r requirements.txt`           |
| `Error de conexión a MySQL`       | Verificá que MySQL esté corriendo y que las credenciales en `.env` sean correctas                            |
| El archivo no es reconocido       | Usá el archivo original exportado del BROU sin modificarlo                                                   |

---

## Notas de seguridad

- El archivo `.env` con tus credenciales **nunca se sube a Git** (está en `.gitignore`)
- Los archivos del banco se guardan en `data/` que también está excluida del repositorio
- No compartas el archivo `.env` con nadie
