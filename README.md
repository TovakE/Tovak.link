# Project Structure

This repository uses a clean split between web app files, data artifacts, documentation, and tests.

```text
web/
  index.html
  styles.css
  app.js

data/
  exports/   # generated files during local use
  samples/   # example exported documents

docs/
  README.md  # how to run static site + how export works
  schema.md  # field definitions and output schema

tests/       # optional future validation scripts
```

See `docs/README.md` for usage instructions and `docs/schema.md` for the export JSON schema.
