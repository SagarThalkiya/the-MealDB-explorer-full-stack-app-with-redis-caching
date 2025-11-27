export interface Ingredient {
  name: string;
  measure?: string | null;
}

export interface MealSummary {
  id: string;
  name: string;
  category?: string | null;
  area?: string | null;
  thumbnail?: string | null;
}

export interface MealDetail extends MealSummary {
  instructions?: string | null;
  tags?: string[];
  youtube?: string | null;
  source?: string | null;
  ingredients: Ingredient[];
}

export interface Category {
  id: string;
  name: string;
  description?: string | null;
  thumbnail?: string | null;
}

