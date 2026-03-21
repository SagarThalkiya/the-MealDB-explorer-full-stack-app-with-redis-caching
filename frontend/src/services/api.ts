import type { Category, MealDetail, MealSummary } from '../types';

// --- SIMPLEST SOLUTION: Replace the old line with this ---
const API_BASE_URL = window.location.hostname === "localhost" 
  ? "http://localhost:8000" 
  : "https://the-meal-db-explorer-full-stack-app.vercel.app";
// ---------------------------------------------------------

async function request<T>(endpoint: string, init?: RequestInit): Promise<T> {
  // Ensure we include /api because your backend routes are prefixed with it
  const url = `${API_BASE_URL}/api${endpoint}`;
  
  const response = await fetch(url, {
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