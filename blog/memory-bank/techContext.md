# Tech Context

## Technologies Used

- **Frontend**: Vanilla HTML5, CSS3, Javascript (ES6+).
- **Markdown Parsing**: `marked.js` (via CDN).
- **Styling**: Vanilla CSS with CSS Variables.
- **Data**: `posts.json` for metadata.
- **RSS**: `rss.xml` (Static/Manual).

## Development Setup

- GitHub Pages hosting at `/blog/`.
- Local development requires a local server (like Live Server) due to Fetch API CORS/File restrictions.

## Technical Constraints

- **Subpath**: `/blog/` is the root. All assets must be prefixed with `/blog/`.
- **Client-Side Fetching**: Markdown files are fetched dynamically on navigation.

## Tool Usage

- Use Google Fonts ('Crimson Pro' and 'Inter') for a personal/educational feel.
