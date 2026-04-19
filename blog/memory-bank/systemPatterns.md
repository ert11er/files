# System Patterns

## Architecture

- **Static Content**: Posts reside in `posts/*.md`.
- **Manifest**: A `posts.json` file acts as the source of truth for post metadata (title, date, tags, filename).
- **Single Page Application (SPA) feel**: The index page handles routing/rendering without full page reloads for posts using URL hashes.

## Data Flow

1. User loads `index.html`.
2. App fetches `posts.json`.
3. App renders list of posts.
4. User clicks post -> App fetches `posts/filename.md`.
5. `marked.js` converts MD to HTML and injects into the main content area.

## Key Technical Decisions

- **Turkish Localization**: All hardcoded strings in JS/HTML are in Turkish.
- **Path Handling**: All links and fetches include the `/blog/` prefix for GitHub Pages compatibility.
- **Dark Mode**: Implementation via `data-theme` attribute and CSS variables.
