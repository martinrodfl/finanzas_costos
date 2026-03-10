"""
Crea la base de datos y la tabla leyendo db/schemas.sql.
Lee DB_HOST, DB_USER, DB_PASSWORD de las variables de entorno
(seteadas por install.bat con set /p).
"""
import os
import sys
from pathlib import Path


def main():
    host = os.environ.get("DB_HOST", "localhost")
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "")

    try:
        import mysql.connector
    except ImportError:
        print("[ERROR] mysql-connector-python no esta instalado en el venv")
        sys.exit(1)

    sql_path = Path(__file__).parent.parent / "db" / "schemas.sql"
    if not sql_path.exists():
        print(f"[ERROR] No se encontro {sql_path}")
        sys.exit(1)

    try:
        conn = mysql.connector.connect(host=host, user=user, password=password)
        cursor = conn.cursor()

        sql = sql_path.read_text(encoding="utf-8")
        for statement in sql.split(";"):
            statement = statement.strip()
            if statement and not statement.startswith("--"):
                cursor.execute(statement)

        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Base de datos y tabla creadas exitosamente")
    except mysql.connector.Error as e:
        print(f"[ERROR] MySQL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
