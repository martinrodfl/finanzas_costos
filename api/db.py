import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

# Carga el .env de la raíz del proyecto
load_dotenv(Path(__file__).parent.parent / ".env")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
