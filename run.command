#!/bin/bash
# Double-click este archivo en macOS para lanzar el importador.
# Si aparece un error de permisos, ejecutá una vez desde Terminal:
#   chmod +x run.command

SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$SCRIPT_DIR"
python3 run.py
echo ""
read -rp "Presioná Enter para cerrar..."
