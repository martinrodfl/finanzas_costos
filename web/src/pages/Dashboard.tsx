import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import TablaMovimientos from '../components/TablaMovimientos';
import styles from './Dashboard.module.css';

interface Movimiento {
	id: number;
	fecha: string;
	descripcion: string;
	documento: string | null;
	dependencia: string | null;
	debito: number;
	credito: number;
}

export default function Dashboard() {
	const [movimientos, setMovimientos] = useState<Movimiento[]>([]);
	const [meses, setMeses] = useState<string[]>([]);
	const [mesSeleccionado, setMesSeleccionado] = useState('');
	const [loading, setLoading] = useState(true);
	const navigate = useNavigate();

	const totalDebito = movimientos.reduce((s, m) => s + Number(m.debito), 0);
	const totalCredito = movimientos.reduce((s, m) => s + Number(m.credito), 0);

	useEffect(() => {
		api.get('/movimientos/meses').then(({ data }) => {
			setMeses(data);
			if (data.length > 0) setMesSeleccionado(data[0]);
		});
	}, []);

	useEffect(() => {
		if (!mesSeleccionado) return;
		setLoading(true);
		api
			.get('/movimientos', { params: { mes: mesSeleccionado } })
			.then(({ data }) => setMovimientos(data))
			.finally(() => setLoading(false));
	}, [mesSeleccionado]);

	const salir = () => {
		localStorage.removeItem('token');
		navigate('/login');
	};

	const formatMes = (m: string) => {
		const [year, month] = m.split('-');
		const fecha = new Date(Number(year), Number(month) - 1);
		return fecha.toLocaleDateString('es-UY', {
			month: 'long',
			year: 'numeric',
		});
	};

	return (
		<div className={styles.container}>
			<header className={styles.header}>
				<h1>Finanzas Gastos</h1>
				<button
					onClick={salir}
					className={styles.btnSalir}
				>
					Salir
				</button>
			</header>

			<main className={styles.main}>
				<div className={styles.controles}>
					<div className={styles.filtroMes}>
						<label>Período</label>
						<select
							value={mesSeleccionado}
							onChange={(e) => setMesSeleccionado(e.target.value)}
						>
							{meses.map((m) => (
								<option
									key={m}
									value={m}
								>
									{formatMes(m)}
								</option>
							))}
						</select>
					</div>
				</div>

				<div className={styles.resumen}>
					<div className={`${styles.tarjeta} ${styles.debito}`}>
						<span>Total egresos</span>
						<strong>
							${' '}
							{totalDebito.toLocaleString('es-UY', {
								minimumFractionDigits: 2,
							})}
						</strong>
					</div>
					<div className={`${styles.tarjeta} ${styles.credito}`}>
						<span>Total ingresos</span>
						<strong>
							${' '}
							{totalCredito.toLocaleString('es-UY', {
								minimumFractionDigits: 2,
							})}
						</strong>
					</div>
					<div className={`${styles.tarjeta} ${styles.saldo}`}>
						<span>Diferencia</span>
						<strong>
							${' '}
							{(totalCredito - totalDebito).toLocaleString('es-UY', {
								minimumFractionDigits: 2,
							})}
						</strong>
					</div>
				</div>

				{loading ? (
					<p className={styles.cargando}>Cargando movimientos...</p>
				) : (
					<TablaMovimientos movimientos={movimientos} />
				)}
			</main>
		</div>
	);
}
