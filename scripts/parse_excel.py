import pandas as pd
from pathlib import Path


def _encontrar_fila_header(input_path: str) -> int:
    """Busca la fila donde está el encabezado real (la que contiene 'Fecha')."""
    raw = pd.read_excel(input_path, header=None)
    for i, row in raw.iterrows():
        if any(str(v).strip() == "Fecha" for v in row.values):
            return i
    raise ValueError("No se encontró la fila de encabezado 'Fecha' en el archivo.")


def parse(input_path: str, output_path: str):
    header_row = _encontrar_fila_header(input_path)
    df = pd.read_excel(input_path, header=header_row)

    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Fecha": "fecha",
        "Descripción": "descripcion",
        "Número de documento": "documento",
        "Asunto": "asunto",
        "Dependencia": "dependencia",
        "Débito": "debito",
        "Crédito": "credito"
    })

    # Mantener solo las columnas relevantes
    columnas = [c for c in ["fecha", "descripcion", "documento", "asunto", "dependencia", "debito", "credito"] if c in df.columns]
    df = df[columnas]

    df["debito"] = df["debito"].fillna(0)
    df["credito"] = df["credito"].fillna(0)

    # Convertir fecha y descartar filas sin fecha válida (pie de página, textos del banco, etc.)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df = df[df["fecha"].notna()]
    df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Excel procesado: {len(df)} registros → {output_path}")