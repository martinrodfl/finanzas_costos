import re
import pdfplumber
import pandas as pd
from pathlib import Path

FECHA_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
MONTO_RE = re.compile(r"^\d{1,3}(?:\.\d{3})*,\d{2}$")


def _parse_monto(text: str) -> float:
    return float(text.replace(".", "").replace(",", "."))


def _agrupar_por_fila(words: list, tolerancia: float = 3.0) -> list[list]:
    """Agrupa palabras en filas según su coordenada Y top."""
    filas = []
    for w in sorted(words, key=lambda x: (x["top"], x["x0"])):
        agregado = False
        for fila in filas:
            if abs(w["top"] - fila[0]["top"]) <= tolerancia:
                fila.append(w)
                agregado = True
                break
        if not agregado:
            filas.append([w])
    return filas


def _detectar_umbral_columnas(filas: list) -> float | None:
    """Busca la fila de encabezados y devuelve el punto medio entre Débito y Crédito."""
    for fila in filas:
        textos = [w["text"] for w in fila]
        if "Débito" in textos and "Crédito" in textos:
            x_debito = next(w["x0"] for w in fila if w["text"] == "Débito")
            x_credito = next(w["x0"] for w in fila if w["text"] == "Crédito")
            return (x_debito + x_credito) / 2
    return None


def parse(input_path: str, output_path: str):
    movimientos = []
    umbral_global = None

    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            if not words:
                continue

            filas = _agrupar_por_fila(words)

            # Detectar umbral en esta página; si no hay headers, usar el detectado antes
            umbral = _detectar_umbral_columnas(filas)
            if umbral is not None:
                umbral_global = umbral
            elif umbral_global is not None:
                umbral = umbral_global
            else:
                continue  # Ninguna página anterior tuvo headers todavía

            i = 0
            while i < len(filas):
                fila = filas[i]
                # Buscar celda de fecha (x0 pequeño, texto == dd/mm/yyyy)
                fecha_word = next(
                    (w for w in fila if FECHA_RE.match(w["text"]) and w["x0"] < 80),
                    None
                )
                if fecha_word is None:
                    i += 1
                    continue

                fecha = fecha_word["text"]

                # Montos: clasificar por posición respecto al umbral
                debito = 0.0
                credito = 0.0
                desc_words = []

                for w in fila:
                    if MONTO_RE.match(w["text"]):
                        if w["x0"] >= umbral:
                            credito = _parse_monto(w["text"])
                        else:
                            debito = _parse_monto(w["text"])
                    elif not FECHA_RE.match(w["text"]) and w["x0"] < umbral - 50:
                        desc_words.append(w["text"])

                # Recoger líneas de descripción adicionales (sin fecha, sin montos)
                j = i + 1
                while j < len(filas):
                    sig = filas[j]
                    tiene_fecha = any(FECHA_RE.match(w["text"]) and w["x0"] < 80 for w in sig)
                    if tiene_fecha:
                        break
                    # Solo agregar si es texto de descripción (no montos, no encabezados)
                    extra = [w["text"] for w in sig if not MONTO_RE.match(w["text"]) and w["x0"] < umbral - 50]
                    if extra:
                        desc_words.extend(extra)
                    j += 1
                i = j

                descripcion = " ".join(desc_words).strip()
                movimientos.append({
                    "fecha": fecha,
                    "descripcion": descripcion,
                    "debito": debito,
                    "credito": credito
                })

    df = pd.DataFrame(movimientos, columns=["fecha", "descripcion", "debito", "credito"])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"PDF procesado: {len(df)} registros → {output_path}")