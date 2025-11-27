# TheMealDB Explorer

As part of this task, develop **TheMealDB Explorer**

API INFO
Use the public TheMealDB API:
**https://www.themealdb.com/api.php**
This API provides information about recipes, ingredients, and meal categories.

# Specifications

Your product should have 2 components

- **Web service API** (serving RESTful APIs using nodejs / java / python)
- **Front end layer** rendering content (HTML + CSS + JavaScript/TypeScript + toolsets like ReactJS or similar)

## Web Service

Develop a **web service component** that fetches data from TheMealDB API and exposes a set of simplified endpoints for the UI.

Requirements:

- Cache responses (Redis or in-memory)
- Cache expiry + max size
- Follow REST practices
- Runs locally
- Handle API interactions (use test key `1` for development)

## UI Layer

Ideas:

- **Recipe Search**: Search bar to find meals by name.
- **Category Browser**: Browse meals by category (Chicken, Vegan, etc.).
- **Random Meal**: "I'm feeling hungry" button to show a random recipe.
- **Recipe Details**: Ingredients list, instructions, and YouTube video embed.
- **Responsive Design**: Looks good on mobile and desktop.

## Points to Note

- Follow REST guidelines
- Must run locally
- Violations = invalid submission

## Evaluation

- Code quality
- Extensible structure
- Best practices
- UI/UX
- Performance

## Submission

- Public GitHub repo
- Reply to email without changing subject
- Include repo link
