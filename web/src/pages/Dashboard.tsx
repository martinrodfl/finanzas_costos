import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import TablaMovimientos from '../components/TablaMovimientos';
import VistaCategorias from '../components/VistaCategorias';
import VistaMensual from '../components/VistaMensual';
import styles from './Dashboard.module.css';

interface Movimiento {
	id: number;
	fecha: string;
	descripcion: string;
	documento: string | null;
	dependencia: string | null;
	debito: number;
	credito: number;
	categoria_manual: string | null;
	categoria_regla: string | null;
}

export default function Dashboard() {
	const [movimientos, setMovimientos] = useState<Movimiento[]>([]);
	const [meses, setMeses] = useState<string[]>([]);
	const [mesSeleccionado, setMesSeleccionado] = useState('');
	const [loading, setLoading] = useState(true);
	const [vista, setVista] = useState<'tabla' | 'categorias' | 'mensual'>(
		'tabla',
	);
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

	const handleCategoriaChange = (id: number, categoria: string | null) => {
		setMovimientos((prev) => {
			const desc = prev.find((m) => m.id === id)?.descripcion;
			return prev.map((m) => {
				if (m.id === id) return { ...m, categoria_manual: categoria };
				if (categoria !== null && m.descripcion === desc)
					return { ...m, categoria_regla: categoria };
				return m;
			});
		});
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
					<div className={styles.toggleVista}>
						<button
							className={
								vista === 'tabla' ? styles.toggleActivo : styles.toggleBtn
							}
							onClick={() => setVista('tabla')}
						>
							Gastos Mensuales
						</button>
						<button
							className={
								vista === 'categorias' ? styles.toggleActivo : styles.toggleBtn
							}
							onClick={() => setVista('categorias')}
						>
							Gastos Por Categoría
						</button>
						<button
							className={
								vista === 'mensual' ? styles.toggleActivo : styles.toggleBtn
							}
							onClick={() => setVista('mensual')}
						>
							Gastos Por Año
						</button>
					</div>
					{vista === 'tabla' && (
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
					)}
				</div>

				{vista !== 'mensual' && (
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
				)}

				{vista === 'mensual' ? (
					<VistaMensual />
				) : loading ? (
					<p className={styles.cargando}>Cargando movimientos...</p>
				) : vista === 'tabla' ? (
					<TablaMovimientos movimientos={movimientos} />
				) : (
					<VistaCategorias
						movimientos={movimientos}
						onCategoriaChange={handleCategoriaChange}
					/>
				)}
			</main>
		</div>
	);
}
