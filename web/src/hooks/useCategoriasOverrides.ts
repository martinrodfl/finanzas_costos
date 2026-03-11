import { useState } from 'react';

const KEY = 'finanzas_cat_overrides';

type Overrides = Record<number, string>;

export function useCategoriasOverrides(): [
	Overrides,
	(id: number, categoria: string) => void,
	(id: number) => void,
] {
	const [overrides, setOverrides] = useState<Overrides>(() => {
		try {
			const raw = localStorage.getItem(KEY);
			return raw ? JSON.parse(raw) : {};
		} catch {
			return {};
		}
	});

	const setOverride = (id: number, categoria: string) => {
		setOverrides((prev) => {
			const next = { ...prev, [id]: categoria };
			localStorage.setItem(KEY, JSON.stringify(next));
			return next;
		});
	};

	const removeOverride = (id: number) => {
		setOverrides((prev) => {
			const next = { ...prev };
			delete next[id];
			localStorage.setItem(KEY, JSON.stringify(next));
			return next;
		});
	};

	return [overrides, setOverride, removeOverride];
}
