// ...existing code...
### Prerequisites
- Python 3.9+
- UV package manager
- MySQL 9.5.0+ (local or remote)
- College Scorecard API key (free from https://api.data.gov)

### Required Libraries
The following Python packages are required (automatically installed via `uv sync`):
- `mysql-connector-python` (Database interaction)
- `pandas` (Data dictionary processing)
- `openpyxl` (Excel file reading)
- `python-dotenv` (Environment variable management)
- `requests` (API communication)

### Installation

1. **Clone/navigate to project:**
// ...existing code...# College Scorecard Data Pipeline

A Python-based ETL pipeline for ingesting College Scorecard API data into a normalized MySQL database.

## Overview

This project downloads comprehensive data on ~5,465 U.S. colleges and universities from the [College Scorecard API](https://collegescorecard.ed.gov/data/api-documentation), normalizes it into a relational schema, and loads it into MySQL for analysis.

## Features

✅ **Paginated API Fetching** - Handles 1,000 req/hour rate limit with exponential backoff
✅ **Data Normalization** - Converts nested JSON → normalized relational tables
✅ **Batch Insertion** - Efficient bulk loads (1,000 records/batch)
✅ **Comprehensive Schema** - 15+ tables covering:
  - Institution metadata (location, type, characteristics)
  - Enrollment & student demographics
  - Admissions metrics (test scores, acceptance rates)
  - Financial aid (tuition, net price, living costs)
  - Completion rates & graduation outcomes
  - Earnings & loan debt metrics
  - Repayment statistics
  - Field of Study data (CIP codes, earnings by major)

✅ **Error Handling** - Connection retries, transaction rollback, detailed logging
✅ **Data Validation** - Referential integrity checks, orphaned record detection

## Project Structure

```
DataScrapeV2/
├── main.py                 # Orchestration script with CLI interface
├── api_client.py          # API communication & caching
├── transform.py           # JSON normalization & transformation
├── db_loader.py           # MySQL loading & validation
├── schema.sql             # Complete database schema
├── pyproject.toml         # UV project configuration
├── .env                   # API key & database credentials (local only)
├── .gitignore             # Exclude .env, cache, venv
└── README.md              # This file

## Setup

### Prerequisites
- Python 3.9+
- UV package manager
- MySQL 9.5.0+ (local or remote)
- College Scorecard API key (free from https://api.data.gov)

### Required Libraries
The following Python packages are required (automatically installed via `uv sync`):
- `mysql-connector-python` (Database interaction)
- `pandas` (Data dictionary processing)
- `openpyxl` (Excel file reading)
- `python-dotenv` (Environment variable management)
- `requests` (API communication)

### Copy this file to .env and fill in your values
COLLEGE_SCORECARD_API_KEY=your_api_key_here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=collegescorecard

### Installation

1. **Clone/navigate to project:**
   ```bash
   cd /home/klby/Documents/DataScrapeV2
   ```

2. **Create and activate virtual environment:**
   ```bash
   uv sync
   source .venv/bin/activate.fish  # Fish shell
   # OR
   source .venv/bin/activate       # Bash/Zsh
   ```

3. **Configure credentials** (already done in .env):
   - `COLLEGE_SCORECARD_API_KEY` - Your API key
   - `MYSQL_USER` - Database user (root)
   - `MYSQL_PASSWORD` - Database password
   - `MYSQL_DATABASE` - Database name (collegescorecard)

4. **Review schema** (optional):
   - Open `schema.sql` in MySQL Workbench to review table structure
   - All dimension tables (State, Region, Credential Levels) are pre-populated

### Windows Installation Note
If you are installing on Windows and encounter issues with `mysql-connector-python` (specifically looking for a wheel for version 9.6.0), this is a known issue with that specific release. This project's `pyproject.toml` is configured to exclude version 9.6.0 (`!=9.6.0`) to resolve this. Ensure your dependency definition respects this exclusion if you are installing manually.

## Usage

### Full Pipeline (Fetch → Transform → Load)
```bash
python main.py --full-pipeline
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

### Schema & Validation

**Create database & schema only:**
```bash
python main.py --create-schema
```
- Safe to run multiple times (uses `CREATE TABLE IF NOT EXISTS`)
- Pre-populates dimension tables (States, Credential Levels, etc.)

**Validate loaded data:**
```bash
python main.py --validate
```
- Counts records per table
- Checks referential integrity
- Detects orphaned records

## Database Schema

### Core Tables
- **institution** - 5,465 institution records with location, type, status
- **state** - 50 states + DC (lookup)
- **region** - 9 US regions (lookup)

### Metric Tables (keyed by institution_id + cohort_year)
- **enrollment_metrics** - Student size, full-time %, Pell recipients, retention
- **admission_metrics** - Acceptance rate, SAT/ACT scores
- **financial_aid_metrics** - Tuition, net price, living costs
- **completion_metrics** - Graduation rates (4yr, 6yr, 8yr)
- **earnings_metrics** - Median earnings at 5yr, 6yr, 10yr post-graduation
- **debt_metrics** - Federal loan debt, Parent PLUS debt, repayment
- **repayment_metrics** - Default rates, income-driven repayment status

### Field of Study Tables
- **field_of_study** - CIP codes + credential level lookup
- **institution_field_of_study** - Junction: institution ↔ program
- **field_of_study_earnings** - Earnings by field of study (5yr post-completion)
- **field_of_study_debt** - Debt by field of study

### Demographic Data
- **institution_demographics** - Enrollment by race/ethnicity (normalized)

## Data Fields Included

**Institution Info**: Name, city, state, zip, coordinates, degree types, institution type

**Enrollment**: Total size, full-time %, Pell grant recipients, federal loan recipients, student-faculty ratio, retention rates

**Admissions**: Acceptance rate, SAT/ACT 25th/75th percentiles

**Financial**: In-state/out-of-state tuition, net price, living costs

**Completion**: 4-year, 6-year, 8-year graduation/completion rates

**Outcomes**: Median earnings at 5yr, 6yr, 10yr; % earning above high school graduate

**Debt**: Median federal loan debt, Parent PLUS debt, monthly payment estimates, repayment rates by status

**Field of Study**: Earnings and debt by CIP code + credential level

## Performance Notes

- **Full pipeline**: ~10-15 minutes (55 API calls + transform + batch load)
- **API fetch**: ~2-3 minutes (rate limit: 1,000 req/hr)
- **Transform**: ~2-5 minutes (5,465 institutions, ~89K field-of-study programs)
- **Load**: ~5 minutes (batch inserts, depends on MySQL hardware)

## Incremental Updates

To update existing data:
1. Delete cached files: `rm data_cache/*.json`
2. Re-run pipeline: `python main.py --full-pipeline`
3. Currently loads all institutions; modify `api_client.py` for incremental logic

## Troubleshooting

**API errors:**
- Check API key in .env
- Verify internet connection
- Check API rate limit: 1,000 req/IP/hour

**MySQL connection errors:**
- Verify MySQL server is running
- Check credentials in .env
- Ensure database name exists or use `--create-schema`

**Foreign key violations:**
- Run `--create-schema` first
- Ensure dimension tables (state, region, etc.) are populated

**Memory issues (large datasets):**
- Reduce batch size in `db_loader.py` (change `batch_size=1000`)
- Process subsets by state (filter in `api_client.py`)

## API Reference

College Scorecard API: https://collegescorecard.ed.gov/data/api-documentation

Key endpoints:
- Base: `https://api.data.gov/ed/collegescorecard/v1/schools`
- Query: `?api_key=YOUR_KEY&page=0&per_page=100`
- Fields: Specify comma-separated field names; defaults to all
- Filter: `school.state=CA&admission_rate__range=0..0.2`

## Contributing

To modify schema:
1. Edit `schema.sql` before running `--create-schema`
2. Update corresponding table in `transform.py`
3. Update field mappings in `db_loader.py`

## License

This project uses public data from the U.S. Department of Education. See https://collegescorecard.ed.gov/data/ for terms.

## Notes

- Data includes ~5,465 Title IV-eligible institutions
- Field of Study data: 2014-15, 2015-16, 2018-19, 2019-20 cohorts (measured 5-10 years post-completion)
- Some metrics unavailable for all institutions (NULL values retained)
- Earnings data: May reflect pandemic impact for 2020-21 cohort
- Please setup your own mySQL or other SQL runner if you want to test the schema out

---

**Last Updated**: February 2026
**Python Version**: 3.9+
**MySQL Version**: 9.5.0+
