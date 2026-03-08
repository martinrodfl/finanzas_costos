#!/bin/bash
# Crea un acceso directo en el Escritorio que funciona con doble click.
# Ejecutar UNA SOLA VEZ después de clonar/mover el proyecto.
#
# Uso:
#   bash instalar_acceso_directo.sh

DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"

# Detectar carpeta del Escritorio (español o inglés)
if [ -d "$HOME/Escritorio" ]; then
    DESKTOP="$HOME/Escritorio"
elif [ -d "$HOME/Desktop" ]; then
    DESKTOP="$HOME/Desktop"
else
    DESKTOP="$HOME"
fi

DESTINO="$DESKTOP/Importador BROU.desktop"

cat > "$DESTINO" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Importador BROU
Comment=Importa movimientos bancarios del BROU a la base de datos
Exec=bash "$DIR/run.sh"
Icon=accessories-calculator
Terminal=true
Categories=Finance;Office;
StartupNotify=true
EOF

chmod +x "$DESTINO"

# En GNOME es necesario marcar el archivo como confiable
gio set "$DESTINO" metadata::trusted true 2>/dev/null || true

echo ""
echo "✓ Acceso directo creado en: $DESTINO"
echo "  Ya podés hacer doble click en él desde el Escritorio."
echo ""
read -rp "Presioná Enter para cerrar..."
