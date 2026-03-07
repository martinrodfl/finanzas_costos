import re
import pdfplumber
import pandas as pd
from pathlib import Path


def parse(input_path: str, output_path: str):
    movimientos = []

    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                # Detecta líneas que empiecen con fecha dd/mm/yyyy
                match = re.match(r"(\d{2}/\d{2}/\d{4})\s+(.*)", line)
                if not match:
                    continue

                fecha = match.group(1)
                resto = match.group(2).strip()

                # Extrae números con formato uruguayo al final de la línea
                numeros = re.findall(r"\d{1,3}(?:\.\d{3})*(?:,\d{2})", resto)
                descripcion = re.sub(r"\s+\d{1,3}(?:\.\d{3})*(?:,\d{2}).*$", "", resto).strip()

                debito = 0.0
                credito = 0.0
                if len(numeros) >= 2:
                    debito = float(numeros[0].replace(".", "").replace(",", "."))
                    credito = float(numeros[1].replace(".", "").replace(",", "."))
                elif len(numeros) == 1:
                    debito = float(numeros[0].replace(".", "").replace(",", "."))

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