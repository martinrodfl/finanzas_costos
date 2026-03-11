from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from pydantic import BaseModel
from api.db import get_connection
from api.auth import get_usuario_actual

router = APIRouter(prefix="/movimientos", tags=["movimientos"])


@router.get("")
def listar(
    mes: Optional[str] = Query(None, description="Filtrar por mes en formato YYYY-MM"),
    _usuario: str = Depends(get_usuario_actual)
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if mes:
        cursor.execute(
            """SELECT m.*, r.categoria AS categoria_regla
               FROM movimientos m
               LEFT JOIN categoria_reglas r ON r.descripcion = m.descripcion
               WHERE DATE_FORMAT(m.fecha, '%Y-%m') = %s
               ORDER BY m.fecha DESC""",
            (mes,)
        )
    else:
        cursor.execute(
            """SELECT m.*, r.categoria AS categoria_regla
               FROM movimientos m
               LEFT JOIN categoria_reglas r ON r.descripcion = m.descripcion
               ORDER BY m.fecha DESC"""
        )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convertir fecha a string para serialización JSON
    for row in rows:
        if row.get("fecha"):
            row["fecha"] = str(row["fecha"])
        if row.get("created_at"):
            row["created_at"] = str(row["created_at"])

    return rows


@router.get("/meses")
def listar_meses(_usuario: str = Depends(get_usuario_actual)):
    """Devuelve la lista de meses disponibles en la BD."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT DATE_FORMAT(fecha, '%Y-%m') as mes FROM movimientos ORDER BY mes DESC"
    )
    meses = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return meses


@router.get("/resumen")
def resumen(_usuario: str = Depends(get_usuario_actual)):
    """Totales de débito y crédito agrupados por mes."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            DATE_FORMAT(fecha, '%Y-%m') AS mes,
            SUM(debito)  AS total_debito,
            SUM(credito) AS total_credito
        FROM movimientos
        GROUP BY mes
        ORDER BY mes DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


class CategoriaUpdate(BaseModel):
    categoria: Optional[str] = None


@router.patch("/{id}/categoria")
def actualizar_categoria(
    id: int,
    body: CategoriaUpdate,
    _usuario: str = Depends(get_usuario_actual)
):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE movimientos SET categoria_manual = %s WHERE id = %s",
        (body.categoria, id)
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    if body.categoria is not None:
        cursor.execute(
            """
            INSERT INTO categoria_reglas (descripcion, categoria)
            SELECT descripcion, %s FROM movimientos WHERE id = %s
            ON DUPLICATE KEY UPDATE categoria = VALUES(categoria)
            """,
            (body.categoria, id)
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"ok": True}
