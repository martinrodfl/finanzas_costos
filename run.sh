#!/bin/bash
# Lanzador para Linux/Mac. Se auto-localiza sin importar desde dónde se llame.
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
cd "$SCRIPT_DIR"
python3 run.py
echo ""
read -rp "Presioná Enter para cerrar..."
