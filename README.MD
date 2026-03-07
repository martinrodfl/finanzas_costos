# finanzas_gastos — Importador de Movimientos Bancarios

Herramienta para **importar y consultar movimientos bancarios** del Banco República (BROU). Descargá el extracto de tu cuenta y en segundos tenés todos tus datos en una base de datos lista para consultar.

---

## ¿Qué hace?

- Acepta archivos **Excel (.xls / .xlsx) o PDF** descargados directamente del homebanking del BROU
- Abre un **selector gráfico de archivos** — no hace falta escribir rutas ni arrastrar el archivo
- Procesa y guarda los movimientos en **MySQL** automáticamente
- Incluye una **API REST** con autenticación para consultar los datos desde cualquier aplicación

---

## Documentación

| Documento                            | Para quién                                                    |
| ------------------------------------ | ------------------------------------------------------------- |
| [INSTRUCCIONES.md](INSTRUCCIONES.md) | **Usuario final** — cómo importar movimientos día a día       |
| [DESARROLLO.md](DESARROLLO.md)       | **Desarrollador** — instalación desde cero, arquitectura, API |

---

## Uso (ya instalado)

```bash
python main.py
```

Se abre una ventana para seleccionar el archivo del banco. Listo.

---

## Formatos soportados

| Formato    | Extensión       |
| ---------- | --------------- |
| Excel BROU | `.xls`, `.xlsx` |
| PDF BROU   | `.pdf`          |

---

## Roadmap

- [ ] Clasificación automática de gastos por categoría
- [ ] Soporte para otros bancos (ITAU, Santander, Scotiabank)
- [ ] Dashboard web con gráficos y filtros
- [ ] Importador con interfaz visual completa

---

## Licencia

Proyecto de uso personal. Puede evolucionar hacia una herramienta comercial de análisis financiero.
