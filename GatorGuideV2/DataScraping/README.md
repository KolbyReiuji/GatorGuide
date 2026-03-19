# Overview

This module is responsible for fetching, transforming and loading data from over 6100 US colleges and universities into the MySQL database. It pulls data from College Scoreboard API.

## Feature

**API Fetching:** 

**Data normalization:**

**Data loading:** 

## Running the Pipeline (fetch -> transform -> load)

```
1. python main.py --run full pipeline
```

### Individual Stages

**Fetch only** (download from API, ~55 API calls):

```bash
python main.py --fetch-only
```

- Caches raw JSON to `./data_cache/` (pagination-safe)
- Handles rate limiting automatically
- Skip if you already have cached data

**Transform only** (normalize cached data):

```bash
python main.py --transform-only
```

- Converts JSON to SQL-ready records
- Exports to CSV in `./data_output/` for inspection
- Takes ~2-5 minutes for 5,000+ institutions

**Load only** (insert into MySQL):

```bash
python main.py --load-only
```

- Batch-inserts pre-transformed data
- Validates foreign keys
- Prints summary statistics

**Validate loaded data:**

```bash
python main.py --validate
```

- Counts records per table
- Checks referential integrity
- Detects orphaned records
