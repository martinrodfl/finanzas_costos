import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

// Inyecta el token JWT en cada request automáticamente
api.interceptors.request.use((config) => {
	const token = localStorage.getItem('token');
	if (token) config.headers.Authorization = `Bearer ${token}`;
	return config;
});

// Si el token expiró, redirige al login
api.interceptors.response.use(
	(res) => res,
	(error) => {
		if (error.response?.status === 401) {
			localStorage.removeItem('token');
			window.location.href = '/login';
		}
		return Promise.reject(error);
	},
);

export default api;
