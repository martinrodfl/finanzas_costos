import os
from datetime import datetime
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path


def save(csv_path: str):
    load_dotenv(Path(__file__).parent.parent / ".env", override=True)

    df = pd.read_csv(csv_path)
    # Reemplaza NaN por None para que MySQL lo trate como NULL
    df = df.astype(object).where(pd.notnull(df), None)

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()

    sql_check = """
    SELECT COUNT(*) FROM movimientos
    WHERE fecha = %s AND descripcion = %s AND debito = %s AND credito = %s
    """

    sql_insert = """
    INSERT INTO movimientos (fecha, descripcion, documento, asunto, dependencia, debito, credito)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    insertados = 0
    omitidos = 0
    for _, row in df.iterrows():
        fecha_raw = row["fecha"]
        if isinstance(fecha_raw, str):
            for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
                try:
                    fecha = datetime.strptime(fecha_raw, fmt).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Formato de fecha no reconocido: '{fecha_raw}'")
        else:
            fecha = fecha_raw
        debito = row["debito"] if row["debito"] is not None else 0.0
        credito = row["credito"] if row["credito"] is not None else 0.0

        cursor.execute(sql_check, (fecha, row["descripcion"], debito, credito))
        (existe,) = cursor.fetchone()

        if existe:
            omitidos += 1
            continue

        cursor.execute(sql_insert, (
            fecha,
            row["descripcion"],
            row.get("documento", None),
            row.get("asunto", None),
            row.get("dependencia", None),
            debito,
            credito
        ))
        insertados += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{insertados} registros nuevos guardados en MySQL. ({omitidos} ya existían, omitidos)")