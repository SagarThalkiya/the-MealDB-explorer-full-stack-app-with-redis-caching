import type { FormEvent } from 'react';
import { useEffect, useMemo, useState } from 'react';

import { mealService } from './services/api';
import type { Category, MealDetail, MealSummary } from './types';
import './App.css';

type LoadingState = 'idle' | 'search' | 'random' | 'detail' | 'category';

const formatMealMetadata = (...parts: Array<string | null | undefined>) => {
  const normalized = parts
    .map((value) => value?.trim())
    .filter((value): value is string => Boolean(value && value.toLowerCase() !== 'null'));
  return normalized.join(' • ');
};

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState<MealSummary[]>([]);
  const [categoryMeals, setCategoryMeals] = useState<MealSummary[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedMeal, setSelectedMeal] = useState<MealDetail | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const data = await mealService.getCategories();
        setCategories(data);
        if (data.length) {
          setSelectedCategory(data[0].name);
        }
      } catch {
        setError('Unable to load categories right now.');
      }
    };

    void loadCategories();
  }, []);

  useEffect(() => {
    if (!selectedCategory) return;

    const loadCategoryMeals = async () => {
      setLoading('category');
      setError(null);
      try {
        const meals = await mealService.getMealsByCategory(selectedCategory);
        setCategoryMeals(meals);
      } catch {
        setError('Unable to load meals for this category.');
      } finally {
        setLoading('idle');
      }
    };

    void loadCategoryMeals();
  }, [selectedCategory]);

  const handleSearch = async (event: FormEvent) => {
    event.preventDefault();
    const trimmed = searchTerm.trim();
    if (!trimmed) {
      setSearchResults([]);
      return;
    }

    setLoading('search');
    setError(null);
    try {
      const meals = await mealService.searchMeals(trimmed);
      setSearchResults(meals);
    } catch {
      setError('Search failed. Try again later.');
    } finally {
      setLoading('idle');
    }
  };

  const loadMealDetail = async (mealId: string, state: LoadingState = 'detail') => {
    setLoading(state);
    setError(null);
    try {
      const detail = await mealService.getMeal(mealId);
      setSelectedMeal(detail);
    } catch {
      setError('Unable to fetch meal details.');
    } finally {
      setLoading('idle');
    }
  };

  const handleRandomMeal = async () => {
    setLoading('random');
    setError(null);
    try {
      const meal = await mealService.getRandomMeal();
      setSelectedMeal(meal);
    } catch {
      setError('Unable to fetch a random meal.');
    } finally {
      setLoading('idle');
    }
  };

  const isLoading = (state: LoadingState) => loading === state;

  const infoBanner = useMemo(() => {
    if (error) return { tone: 'error', message: error };
    if (loading !== 'idle') {
      const messages: Record<LoadingState, string> = {
        idle: '',
        search: 'Searching for tasty meals...',
        random: 'Picking something delicious at random...',
        detail: 'Loading recipe details...',
        category: 'Browsing meals in this category...',
      };
      return { tone: 'info', message: messages[loading] };
    }
    return null;
  }, [error, loading]);

  return (
    <main className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">TheMealDB Explorer</p>
          <h1>Discover new meals, ingredients, and inspiration.</h1>
          <p className="subtitle">
            Search by name, browse categories, or let us surprise you with something random.
          </p>
        </div>
        <button className="random-btn" onClick={handleRandomMeal} disabled={isLoading('random')}>
          {isLoading('random') ? 'Serving...' : "I'm feeling hungry"}
        </button>
      </header>

      <section className="panel search-panel">
        <form className="search-bar" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Try “Arrabiata”, “Chicken”, or “Vegan”"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />
          <button type="submit" disabled={isLoading('search')}>
            {isLoading('search') ? 'Searching...' : 'Search'}
          </button>
        </form>
        <MealList
          title="Search results"
          meals={searchResults}
          loading={isLoading('search')}
          emptyMessage={searchTerm ? 'No meals found for that search.' : 'Start by searching for a meal.'}
          onSelect={(meal) => loadMealDetail(meal.id, 'detail')}
        />
      </section>

      <section className="panel categories-panel">
        <header className="panel-header">
          <div>
            <h2>Browse by category</h2>
            <p>Select a category to see what is on the menu.</p>
          </div>
          <select value={selectedCategory} onChange={(event) => setSelectedCategory(event.target.value)}>
            {categories.map((category) => (
              <option key={category.id} value={category.name}>
                {category.name}
              </option>
            ))}
          </select>
        </header>
        <MealList
          title={`${selectedCategory || 'Category'} meals`}
          meals={categoryMeals}
          loading={isLoading('category')}
          emptyMessage="Pick a category to discover meals."
          onSelect={(meal) => loadMealDetail(meal.id, 'detail')}
        />
      </section>

      <section className="panel detail-panel">
        <h2>Recipe details</h2>
        <MealDetailView meal={selectedMeal} loading={isLoading('detail') || isLoading('random')} />
      </section>

      {infoBanner && infoBanner.message && (
        <div className={`banner ${infoBanner.tone}`}>{infoBanner.message}</div>
      )}
    </main>
  );
};

interface MealListProps {
  title: string;
  meals: MealSummary[];
  emptyMessage: string;
  loading: boolean;
  onSelect: (meal: MealSummary) => void;
}

const MealList = ({ title, meals, emptyMessage, loading, onSelect }: MealListProps) => (
  <div className="meal-list">
    <div className="panel-header">
      <h3>{title}</h3>
      {meals.length > 0 && <span className="pill">{meals.length}</span>}
    </div>
    {loading ? (
      <p className="muted">Loading…</p>
    ) : meals.length ? (
      <div className="meals-grid">
        {meals.map((meal) => {
          const metadata = formatMealMetadata(meal.category, meal.area);
          return (
            <article key={meal.id} className="meal-card" onClick={() => onSelect(meal)}>
              {meal.thumbnail && <img src={meal.thumbnail} alt={meal.name} loading="lazy" />}
              <div>
                <h4>{meal.name}</h4>
                {metadata && <p className="muted">{metadata}</p>}
              </div>
            </article>
          );
        })}
      </div>
    ) : (
      <p className="muted">{emptyMessage}</p>
    )}
  </div>
);

interface MealDetailViewProps {
  meal: MealDetail | null;
  loading: boolean;
}

const MealDetailView = ({ meal, loading }: MealDetailViewProps) => {
  if (loading) {
    return <p className="muted">Loading recipe…</p>;
  }

  if (!meal) {
    return <p className="muted">Select or search for a meal to view its recipe.</p>;
  }

  const metadata = formatMealMetadata(meal.category, meal.area);

  return (
    <article className="meal-detail">
      <header>
        <div>
          <h3>{meal.name}</h3>
          {metadata && <p className="muted">{metadata}</p>}
        </div>
        {meal.thumbnail && <img src={meal.thumbnail} alt={meal.name} />}
      </header>

      <section>
        <h4>Ingredients</h4>
        <ul>
          {meal.ingredients.map((ingredient) => (
            <li key={`${ingredient.name}-${ingredient.measure ?? ''}`}>
              <span>{ingredient.name}</span>
              {ingredient.measure && <span className="muted">{ingredient.measure}</span>}
            </li>
          ))}
        </ul>
      </section>

      {meal.instructions && (
        <section>
          <h4>Instructions</h4>
          <p>{meal.instructions}</p>
        </section>
      )}

      <footer className="links">
        {meal.youtube && (
          <a href={meal.youtube} target="_blank" rel="noreferrer">
            Watch on YouTube
          </a>
        )}
        {meal.source && (
          <a href={meal.source} target="_blank" rel="noreferrer">
            View source
          </a>
        )}
      </footer>
    </article>
  );
};

export default App;

