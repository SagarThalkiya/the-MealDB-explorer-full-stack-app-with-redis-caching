import type { Category, MealDetail, MealSummary } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api';

async function request<T>(endpoint: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Request failed');
  }

  return response.json() as Promise<T>;
}

export const mealService = {
  searchMeals(query: string) {
    const params = new URLSearchParams({ q: query });
    return request<MealSummary[]>(`/meals/search?${params.toString()}`);
  },
  getMeal(id: string) {
    return request<MealDetail>(`/meals/${id}`);
  },
  getRandomMeal() {
    return request<MealDetail>('/meals/random');
  },
  getCategories() {
    return request<Category[]>('/categories');
  },
  getMealsByCategory(category: string) {
    return request<MealSummary[]>(`/categories/${encodeURIComponent(category)}/meals`);
  },
};

