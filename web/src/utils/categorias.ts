export interface Categoria {
	nombre: string;
	color: string;
	icono: string;
	palabras: string[];
}

export const CATEGORIAS: Categoria[] = [
	{
		nombre: 'Supermercado',
		color: '#38a169',
		icono: '🛒',
		palabras: [
			'SUPERM',
			'DISCO',
			'TIENDA INGLESA',
			'DEVOTO',
			'GEANT',
			'TA-TA',
			'TATA',
			'MACROMERCADO',
			'FRESH MARKET',
			'EL DORADO',
			'MULTIAHORRO',
		],
	},
	{
		nombre: 'Servicios',
		color: '#3182ce',
		icono: '⚡',
		palabras: [
			'UTE',
			'OSE',
			'ANTEL',
			'ANCAP',
			'GAS',
			'AGUA ',
			'LUZ ',
			'TELEFON',
			'INTERNET',
			'FIBRA',
			'MOVISTAR',
			'CLARO',
			'PERSONAL ',
		],
	},
	{
		nombre: 'Alquiler',
		color: '#805ad5',
		icono: '🏠',
		palabras: ['ALQUILER', 'INMOBILIARIA', 'ARRIENDO', 'ADMINISTRACION'],
	},
	{
		nombre: 'Salud',
		color: '#e53e3e',
		icono: '🏥',
		palabras: [
			'FARMACI',
			'SALUD',
			'MEDIC',
			'CLINICA',
			'HOSPITAL',
			'DENTIST',
			'OPTICA',
			'MUTUALISTA',
			'ASSE',
			'HOSPITAL',
		],
	},
	{
		nombre: 'Transporte',
		color: '#d69e2e',
		icono: '🚌',
		palabras: [
			'STM',
			'TAXI',
			'UBER',
			'COPSA',
			'TURISMAR',
			'CUTCSA',
			'OMNIBUS',
			'CABIFY',
			'PEDIDO YA',
			'NAFTA',
			'COMBUSTIBLE',
			'PEAJE',
		],
	},
	{
		nombre: 'Educación',
		color: '#2b6cb0',
		icono: '📚',
		palabras: [
			'UDELAR',
			'EDUCACION',
			'LICEO',
			'ESCUELA',
			'COLEGIO',
			'UNIVERSIDAD',
			'INSTITUTO',
			'CURSO',
			'CAPACITACION',
		],
	},
	{
		nombre: 'Entretenimiento',
		color: '#ed8936',
		icono: '🎬',
		palabras: [
			'NETFLIX',
			'SPOTIFY',
			'CINEMA',
			'CABLEVISION',
			'DIRECTV',
			'YOUTUBE',
			'DISNEY',
			'HBO',
			'CINE ',
			'TEATRO',
			'RESTAU',
			'RESTAURANT',
			'PIZZ',
			'SUSHI',
			'BURGER',
			'MCDONALD',
			'DELIVERY',
		],
	},
	{
		nombre: 'Transferencias',
		color: '#718096',
		icono: '↔️',
		palabras: ['TRANSFERENCIA', 'TEFI', 'PAGO '],
	},
	{
		nombre: 'Ingresos',
		color: '#276749',
		icono: '💰',
		palabras: [
			'SALARIO',
			'HABERES',
			'SUELDO',
			'HONORARIO',
			'COBRO',
			'ACREDITACION',
		],
	},
];

export const CATEGORIA_OTROS: Categoria = {
	nombre: 'Otros',
	color: '#a0aec0',
	icono: '📋',
	palabras: [],
};

export function categorizar(descripcion: string): Categoria {
	const desc = descripcion.toUpperCase();
	for (const cat of CATEGORIAS) {
		if (cat.palabras.some((p) => desc.includes(p))) {
			return cat;
		}
	}
	return CATEGORIA_OTROS;
}

export function getCategorias(): Categoria[] {
	return [...CATEGORIAS, CATEGORIA_OTROS];
}
