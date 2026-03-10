import sys
import subprocess
import time
import socket
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
CSV_OUTPUT = PROJECT_ROOT / "data" / "processed" / "movimientos.csv"

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))


def obtener_ruta():
    if len(sys.argv) > 1:
        return Path(sys.argv[1].strip().strip("'\""))

    # Abrir selector de archivos gráfico
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal de tkinter
        root.attributes("-topmost", True)  # El diálogo aparece al frente

        ruta_str = filedialog.askopenfilename(
            title="Seleccioná el archivo de movimientos del banco",
            initialdir=Path.home(),
            filetypes=[
                ("Excel", "*.xls *.xlsx"),
                ("Todos los archivos", "*.*"),
            ]
        )
        root.destroy()

        if not ruta_str:
            print("No se seleccionó ningún archivo. Cancelado.")
            sys.exit(0)

        return Path(ruta_str)

    except Exception:
        # Fallback a entrada por terminal si tkinter falla
        entrada = input("Ingresá la ruta al archivo del banco (.xls o .xlsx): ").strip().strip("'\"")  
        return Path(entrada)


def main():
    print("=== Importador de Movimientos Bancarios ===\n")

    ruta = obtener_ruta()

    if not ruta.exists():
        print(f"Error: no se encontró el archivo '{ruta}'.")
        sys.exit(1)

    extension = ruta.suffix.lower()
    print(f"Archivo detectado: {ruta.name}")

    if extension in (".xls", ".xlsx"):
        import parse_excel
        parse_excel.parse(str(ruta), str(CSV_OUTPUT))

    else:
        print(f"Formato no soportado: '{extension}'. Usá un archivo .xls o .xlsx.")
        sys.exit(1)

    import save_mysql
    save_mysql.save(str(CSV_OUTPUT))

    print("\n✓ Proceso completado exitosamente.")

    levantar_servicios()


def _puerto_libre(puerto: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", puerto)) != 0


def levantar_servicios():
    print("\n— Levantando servicios —")

    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Detectar ruta del Python del venv de la API según OS
    if sys.platform == "win32":
        api_python = str(PROJECT_ROOT / "api" / "venv" / "Scripts" / "python.exe")
    else:
        api_python = str(PROJECT_ROOT / "api" / "venv" / "bin" / "python")

    # Backend (uvicorn)
    if _puerto_libre(8000):
        log_backend = open(logs_dir / "backend.log", "w")
        subprocess.Popen(
            [api_python, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=PROJECT_ROOT,
            stdout=log_backend,
            stderr=log_backend,
            stdin=subprocess.DEVNULL,
        )
        time.sleep(2)  # Esperar a que uvicorn arranque
        if _puerto_libre(8000):
            print("  [ERROR] Backend no pudo iniciar. Revisá logs/backend.log")
        else:
            print("  Backend iniciado en http://localhost:8000")
    else:
        print("  Backend ya estaba corriendo en http://localhost:8000")

    # Frontend (Vite)
    if _puerto_libre(5173):
        log_frontend = open(logs_dir / "frontend.log", "w")
        subprocess.Popen(
            "npm run dev",
            cwd=PROJECT_ROOT / "web",
            stdout=log_frontend,
            stderr=log_frontend,
            shell=True,
            stdin=subprocess.DEVNULL,
        )
        print("  Frontend iniciado en http://localhost:5173")
        time.sleep(4)  # Esperar a que Vite arranque
    else:
        print("  Frontend ya estaba corriendo en http://localhost:5173")

    webbrowser.open("http://localhost:5173")
    print("  Navegador abierto. ¡Listo!")


if __name__ == "__main__":
    main()
