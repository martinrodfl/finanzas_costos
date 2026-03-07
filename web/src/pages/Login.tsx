import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Login.module.css';

export default function Login() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [error, setError] = useState('');
	const [loading, setLoading] = useState(false);
	const navigate = useNavigate();

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setError('');
		setLoading(true);

		try {
			const form = new URLSearchParams();
			form.append('username', username);
			form.append('password', password);

			const { data } = await axios.post('/api/auth/login', form);
			localStorage.setItem('token', data.access_token);
			navigate('/dashboard');
		} catch {
			setError('Usuario o contraseña incorrectos');
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className={styles.container}>
			<div className={styles.card}>
				<h1 className={styles.titulo}>Finanzas Gastos</h1>
				<p className={styles.subtitulo}>
					Iniciá sesión para ver tus movimientos
				</p>

				<form
					onSubmit={handleSubmit}
					className={styles.form}
				>
					<div className={styles.campo}>
						<label>Usuario</label>
						<input
							type='text'
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							placeholder='admin'
							required
							autoFocus
						/>
					</div>

					<div className={styles.campo}>
						<label>Contraseña</label>
						<input
							type='password'
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							placeholder='••••••••'
							required
						/>
					</div>

					{error && <p className={styles.error}>{error}</p>}

					<button
						type='submit'
						className={styles.boton}
						disabled={loading}
					>
						{loading ? 'Ingresando...' : 'Ingresar'}
					</button>
				</form>
			</div>
		</div>
	);
}
