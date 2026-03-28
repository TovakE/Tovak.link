# Export Schema: `person-record-<id>.json`

This document defines the expected JSON structure for exported person records.

## Top-level object

```json
{
  "id": "string",
  "name": {
    "first": "string",
    "last": "string"
  },
  "contact": {
    "email": "string",
    "phone": "string"
  },
  "metadata": {
    "created_at": "ISO-8601 datetime string",
    "source": "web-form"
  }
}
```

## Field definitions

- `id` (`string`, required): Unique identifier used in the export filename.
- `name` (`object`, required): Person name fields.
  - `first` (`string`, required): Given name.
  - `last` (`string`, required): Family name.
- `contact` (`object`, required): Contact details.
  - `email` (`string`, optional): Email address if supplied.
  - `phone` (`string`, optional): Phone number if supplied.
- `metadata` (`object`, required): Export metadata.
  - `created_at` (`string`, required): Timestamp of export in ISO-8601 format.
  - `source` (`string`, required): Must be `"web-form"` for browser-generated exports.

## Output rules

1. Filename must follow `person-record-<id>.json`.
2. `id` in the payload must match `<id>` in the filename.
3. Output must be valid UTF-8 JSON.
4. Unknown fields should be ignored by downstream consumers unless schema versioning is introduced.
