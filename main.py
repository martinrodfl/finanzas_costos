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

    # Detectar ruta del Python del venv según OS
    if sys.platform == "win32":
        venv_python = str(PROJECT_ROOT / "venv" / "Scripts" / "python.exe")
        npm_cmd = "npm.cmd"
    else:
        venv_python = str(PROJECT_ROOT / "venv" / "bin" / "python")
        npm_cmd = "npm"

    # Backend (uvicorn)
    if _puerto_libre(8000):
        subprocess.Popen(
            [venv_python, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=PROJECT_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("  Backend iniciado en http://localhost:8000")
    else:
        print("  Backend ya estaba corriendo en http://localhost:8000")

    # Frontend (Vite)
    if _puerto_libre(5173):
        subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=PROJECT_ROOT / "web",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("  Frontend iniciado en http://localhost:5173")
        time.sleep(3)  # Esperar a que Vite arranque
    else:
        print("  Frontend ya estaba corriendo en http://localhost:5173")

    webbrowser.open("http://localhost:5173")
    print("  Navegador abierto. ¡Listo!")


if __name__ == "__main__":
    main()
