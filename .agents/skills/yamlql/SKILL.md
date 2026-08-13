---
name: yamlql
description: "How the KISS repo gets SQLite-like SQL over its flat YAML sidecars using YamlQL (DuckDB-backed). Explains kiss/utils/yaml_query.py, the `root` table schema, the `query.py` CLI, and conventions for writing new queries. Use before touching or extending the query layer."
---

# YamlQL Query-Layer Skill (flat files + SQL)

KISS stores metadata as flat YAML sidecars (`public/images/<img>.yml`) — those files are the single source of truth. This skill explains the thin layer that lets us run real SQL over them (SQLite-like support) using **YamlQL**, a small library that transforms a YAML document into DuckDB tables.

Vendored reference: `kiss/third_party/YamlQL` (cloned from `github.com/AKSarav/YamlQL`). Also installed as the pip package `yamlql` (which itself depends on `duckdb`, `pandas`, `pyyaml`).

---

## 1. Why this design

- No ETL / no index sync: every query re-reads the sidecars, so results are always fresh.
- The `.yml` files stay human-editable and diff-able (they remain the source of truth).
- Real SQL (joins, aggregates, filters) instead of hand-written Python filtering.

## 2. How the merged document is built

`utils/yaml_query.py::load_all_sidecars()` reads every `*.yml` under `public/images/`, and for each image produces one record dict:

```
image_path, filename, language, caption, status, tags (list), source, notes,
created, llm_evaluation_* (flattened), is_annotated (computed: lang+caption present)
```

`query_all()` dumps those records as a YAML **list** (top level is `- record`), then hands it to `YamlQL(..., strategy="depth")`. Because the top level is a list, the transformer produces ONE table named **`root`** where each row is one image.

## 3. The `root` table

Columns you can rely on (flattened from each sidecar):

| column | type | meaning |
|---|---|---|
| `image_path` | str | relative path like `monsoon_field.jpg` |
| `filename` | str | basename |
| `language` | str | BCP-47 tag, empty if missing |
| `status` | str | `todo` / `drafted` / `reviewed` / `done` |
| `caption` | str | caption text |
| `tags` | list | tags as a list column |
| `source`, `notes`, `created` | str | provenance |
| `llm_evaluation_score`, `llm_evaluation_feedback`, `llm_evaluation_qa_history` | … | flattened LLM eval |
| `is_annotated` | bool | computed: `language AND caption` present |

Nested dicts flatten with `_` (e.g. `llm_evaluation.score` → `llm_evaluation_score`). A broken sidecar becomes a row with `error` set and empty fields so one bad file never breaks a query.

## 4. API

```python
from utils.yaml_query import query_all, table_names, preview, status_counts

query_all("SELECT image_path, language FROM root WHERE status = 'drafted'")
query_all("SELECT status, count(*) AS n FROM root GROUP BY status ORDER BY n DESC")
query_all("SELECT image_path FROM root WHERE is_annotated ORDER BY image_path LIMIT 10")

table_names()     # -> ['root']
preview(limit=5)  # first rows, core columns
status_counts()   # -> {"drafted": n, "total": n, "annotated": n, ...}
```

Results come back as a **pandas DataFrame**. Use `df.iterrows()` or `df.to_dict("records")`.

## 5. CLI

```bash
python query.py "SELECT image_path, language, status FROM root"
python query.py "SELECT status, count(*) n FROM root GROUP BY status"
python query.py "SELECT image_path FROM root WHERE is_annotated"
python query.py --list        # list tables
python query.py --help
```

## 6. Gotchas

- `query_all` takes **no bind parameters** (the library passes the SQL string straight to DuckDB). Sanitize/whitelist any user input before embedding it — never interpolate raw user text into SQL.
- `max_depth=2` keeps `llm_evaluation` flattened to one level. Raising it changes the schema — keep the default unless a query needs deeper nesting.
- Queries are read-only by construction (YamlQL loads into an in-memory DuckDB; nothing writes to disk except the temp merged file in `tempfile.gettempdir()`).
- To change the query layer, prefer editing `utils/yaml_query.py` — the vendored library under `third_party/YamlQL` should not be modified (it is upstream code).
