import { useEffect, useState } from 'react';
import api from '../api/client';
import styles from './VistaMensual.module.css';

interface ResumenMes {
	mes: string;
	total_debito: number;
	total_credito: number;
}

export default function VistaMensual() {
	const [datos, setDatos] = useState<ResumenMes[]>([]);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		api
			.get('/movimientos/resumen')
			.then(({ data }) => setDatos(data))
			.finally(() => setLoading(false));
	}, []);

	if (loading) return <p className={styles.cargando}>Cargando...</p>;
	if (datos.length === 0)
		return <p className={styles.cargando}>No hay datos disponibles.</p>;

	const maxValor = Math.max(
		...datos.flatMap((d) => [Number(d.total_debito), Number(d.total_credito)]),
		1,
	);

	const fmt = (n: number) =>
		`$ ${Number(n).toLocaleString('es-UY', { minimumFractionDigits: 2 })}`;

	const formatMes = (m: string) => {
		const [year, month] = m.split('-');
		const fecha = new Date(Number(year), Number(month) - 1);
		return fecha.toLocaleDateString('es-UY', {
			month: 'long',
			year: 'numeric',
		});
	};

	// Ordenar de más antiguo a más reciente para el gráfico
	const datosAsc = [...datos].reverse();

	const totalEgresos = datos.reduce((s, d) => s + Number(d.total_debito), 0);
	const totalIngresos = datos.reduce((s, d) => s + Number(d.total_credito), 0);

	return (
		<div className={styles.contenedor}>
			{/* Resumen global */}
			<div className={styles.resumenGlobal}>
				<div className={`${styles.pill} ${styles.pillEgreso}`}>
					<span>Total egresos (todos los meses)</span>
					<strong>{fmt(totalEgresos)}</strong>
				</div>
				<div className={`${styles.pill} ${styles.pillIngreso}`}>
					<span>Total ingresos (todos los meses)</span>
					<strong>{fmt(totalIngresos)}</strong>
				</div>
				<div className={`${styles.pill} ${styles.pillSaldo}`}>
					<span>Balance general</span>
					<strong
						style={{
							color: totalIngresos - totalEgresos >= 0 ? '#38a169' : '#e53e3e',
						}}
					>
						{fmt(totalIngresos - totalEgresos)}
					</strong>
				</div>
			</div>

			{/* Gráfico de barras */}
			<div className={styles.graficoCard}>
				<h3 className={styles.graficoTitulo}>Evolución mensual</h3>
				<div className={styles.grafico}>
					{datosAsc.map((d) => {
						const pctEgreso = (Number(d.total_debito) / maxValor) * 100;
						const pctIngreso = (Number(d.total_credito) / maxValor) * 100;
						const [year, month] = d.mes.split('-');
						const label = new Date(Number(year), Number(month) - 1)
							.toLocaleDateString('es-UY', { month: 'short' })
							.replace('.', '');
						return (
							<div
								key={d.mes}
								className={styles.columna}
							>
								<div className={styles.barras}>
									<div className={styles.barraWrap}>
										<div
											className={`${styles.barra} ${styles.barraEgreso}`}
											style={{ height: `${pctEgreso}%` }}
											title={`Egresos: ${fmt(Number(d.total_debito))}`}
										/>
									</div>
									<div className={styles.barraWrap}>
										<div
											className={`${styles.barra} ${styles.barraIngreso}`}
											style={{ height: `${pctIngreso}%` }}
											title={`Ingresos: ${fmt(Number(d.total_credito))}`}
										/>
									</div>
								</div>
								<span className={styles.labelMes}>{label}</span>
							</div>
						);
					})}
				</div>
				<div className={styles.leyenda}>
					<span className={styles.leyendaEgreso}>■ Egresos</span>
					<span className={styles.leyendaIngreso}>■ Ingresos</span>
				</div>
			</div>

			{/* Tabla detallada */}
			<div className={styles.tablaCard}>
				<table className={styles.tabla}>
					<thead>
						<tr>
							<th>Mes</th>
							<th className={styles.monto}>Egresos</th>
							<th className={styles.monto}>Ingresos</th>
							<th className={styles.monto}>Balance</th>
							<th>Proporción</th>
						</tr>
					</thead>
					<tbody>
						{datos.map((d) => {
							const egreso = Number(d.total_debito);
							const ingreso = Number(d.total_credito);
							const balance = ingreso - egreso;
							const total = egreso + ingreso || 1;
							const pctEgreso = (egreso / total) * 100;
							return (
								<tr key={d.mes}>
									<td className={styles.mesTd}>{formatMes(d.mes)}</td>
									<td className={`${styles.monto} ${styles.colorEgreso}`}>
										{fmt(egreso)}
									</td>
									<td className={`${styles.monto} ${styles.colorIngreso}`}>
										{fmt(ingreso)}
									</td>
									<td
										className={styles.monto}
										style={{
											color: balance >= 0 ? '#38a169' : '#e53e3e',
											fontWeight: 700,
										}}
									>
										{fmt(balance)}
									</td>
									<td>
										<div className={styles.propWrapper}>
											<div
												className={styles.propEgreso}
												style={{ width: `${pctEgreso}%` }}
												title={`Egresos ${pctEgreso.toFixed(0)}%`}
											/>
											<div
												className={styles.propIngreso}
												style={{ width: `${100 - pctEgreso}%` }}
												title={`Ingresos ${(100 - pctEgreso).toFixed(0)}%`}
											/>
										</div>
									</td>
								</tr>
							);
						})}
					</tbody>
				</table>
			</div>
		</div>
	);
}
