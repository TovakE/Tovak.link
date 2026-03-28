# Local Static Site Usage

## Run the site locally

1. Open `web/index.html` in your browser.
2. Fill out the person record form in the page.
3. Click the export/download action in the UI.

## Export output location

This project generates records client-side in the browser. The downloaded file is saved by the user into their chosen local download location (typically the browser's default Downloads folder unless changed).

For local project organization, exported files should be moved into:

- `data/exports/` for working files generated during local use.
- `data/samples/` for example documents you want to keep as references.

## Export file naming

Use this naming convention for exported documents:

- `person-record-<id>.json`

Example:

- `person-record-12345.json`

## Data handling notice

Exports are generated in the browser (client-side only). No backend storage or server-side processing is included unless a backend is explicitly added later.
