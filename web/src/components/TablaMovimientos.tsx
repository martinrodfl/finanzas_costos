import styles from './TablaMovimientos.module.css';

interface Movimiento {
	id: number;
	fecha: string;
	descripcion: string;
	documento: string | null;
	dependencia: string | null;
	debito: number;
	credito: number;
}

interface Props {
	movimientos: Movimiento[];
}

export default function TablaMovimientos({ movimientos }: Props) {
	const fmt = (n: number) =>
		n > 0
			? `$ ${Number(n).toLocaleString('es-UY', { minimumFractionDigits: 2 })}`
			: '—';

	const fmtFecha = (f: string) => {
		const [y, m, d] = f.split('-');
		return `${d}/${m}/${y}`;
	};

	if (movimientos.length === 0) {
		return (
			<p className={styles.vacio}>No hay movimientos para este período.</p>
		);
	}

	return (
		<div className={styles.wrapper}>
			<table className={styles.tabla}>
				<thead>
					<tr>
						<th>Fecha</th>
						<th>Descripción</th>
						<th>Dependencia</th>
						<th className={styles.monto}>Egreso</th>
						<th className={styles.monto}>Ingreso</th>
					</tr>
				</thead>
				<tbody>
					{movimientos.map((m) => (
						<tr
							key={m.id}
							className={m.credito > 0 ? styles.ingreso : ''}
						>
							<td className={styles.fecha}>{fmtFecha(m.fecha)}</td>
							<td>{m.descripcion}</td>
							<td className={styles.dependencia}>{m.dependencia ?? '—'}</td>
							<td className={`${styles.monto} ${styles.debito}`}>
								{fmt(m.debito)}
							</td>
							<td className={`${styles.monto} ${styles.credito}`}>
								{fmt(m.credito)}
							</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}
