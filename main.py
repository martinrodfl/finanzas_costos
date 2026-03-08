#!/home/martin/Programacion/Proyectos/Python/finanzas_gastos/venv/bin/python
import sys
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
                ("Archivos del banco", "*.xls *.xlsx *.pdf"),
                ("Excel", "*.xls *.xlsx"),
                ("PDF", "*.pdf"),
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
        entrada = input("Ingresá la ruta al archivo del banco (.xls, .xlsx o .pdf): ").strip().strip("'\"")
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

    elif extension == ".pdf":
        import parse_pdf
        parse_pdf.parse(str(ruta), str(CSV_OUTPUT))

    else:
        print(f"Formato no soportado: '{extension}'. Usá un archivo .xls, .xlsx o .pdf.")
        sys.exit(1)

    import save_mysql
    save_mysql.save(str(CSV_OUTPUT))

    print("\n✓ Proceso completado exitosamente.")


if __name__ == "__main__":
    main()
