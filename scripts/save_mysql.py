import os
from datetime import datetime
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path


def save(csv_path: str):
    load_dotenv(Path(__file__).parent.parent / ".env")

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

    sql = """
    INSERT INTO movimientos (fecha, descripcion, documento, dependencia, debito, credito)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    count = 0
    for _, row in df.iterrows():
        fecha = datetime.strptime(row["fecha"], "%d/%m/%Y").date() if isinstance(row["fecha"], str) else row["fecha"]
        cursor.execute(sql, (
            fecha,
            row["descripcion"],
            row.get("documento", None),
            row.get("dependencia", None),
            row["debito"],
            row["credito"]
        ))
        count += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{count} registros guardados en MySQL.")