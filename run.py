"""
Lanzador cross-platform del importador de movimientos bancarios.

Uso:
  Linux/Mac:  python run.py
  Windows:    python run.py
  Con archivo: python run.py /ruta/al/archivo.xls
"""
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Detectar el Python del venv según OS
if sys.platform == "win32":
    venv_python = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"
else:
    venv_python = PROJECT_ROOT / "venv" / "bin" / "python"

if not venv_python.exists():
    print("Error: no se encontró el entorno virtual.")
    print(f"  Buscado en: {venv_python}")
    print("  Creá el venv con: python -m venv venv")
    print("  Instalá dependencias con: pip install -r requirements.txt")
    sys.exit(1)

result = subprocess.run(
    [str(venv_python), "main.py"] + sys.argv[1:],
    cwd=PROJECT_ROOT,
)
sys.exit(result.returncode)
