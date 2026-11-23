# Module 3: Python for Data Engineering Brief

**Week:** 3 of 4 · **Builds on:** Module 2 (dataframe workflow) · **Feeds into:** Capstone

## Objective

By the end of this stage, the trainee parses and normalizes messy timestamps, reads and writes JSON, CSV, Excel, and Avro, and collects web data responsibly from a local sandbox website that has its own robots.txt.

## Scope

| # | Subject | Time | Key concepts and terms | Research |
| --- | --- | --- | --- | --- |
| 3.1 | Working with datetime formats | 3.0 h | `datetime`, `date`, `time`, `timedelta`, naive vs aware, time zones and UTC, `strftime`/`strptime` codes, ISO 8601, `pd.to_datetime` (explicit format, `errors="coerce"`, NaT), `DatetimeIndex`, resampling, `.dt` date parts | Why silent parsing failures are dangerous and how to make them loud |
| 3.2 | Working with JSON, CSV, and Excel | 3.0 h | Flat vs nested data, `read_csv` options (`sep`, `header`, `dtype`, `usecols`, `nrows`, `chunksize`), `read_json`/`to_json`, `read_excel`/`to_excel` (needs `openpyxl`), `json_normalize`, encoding, row-oriented vs columnar storage | What changes when data makes a round trip between formats |
| 3.3 | Working with Avro | 2.0 h | Row-oriented binary format, JSON schema, primitive vs complex types, records, unions with null for optional fields, schema stored with the data, schema evolution, `fastavro` writer/reader, codecs | Why a schema-carrying format matters for pipelines |
| 3.4 | Web scraping against the local sandbox site | 2.5 h | HTTP request/response, HTML structure, Beautiful Soup, selectors, pagination, rate limiting, robots.txt and the Robots Exclusion Protocol (`urllib.robotparser`), terms of service, user-agent identification | The difference between "allowed by robots.txt" and "authorized" |
| 3.5 | Notebook build, run-all check, mentor review | 1.5 h | See Deliverable | n/a |
| | **Total** | **12 h** | | |

## Stack constraints

| Constraint | Detail |
| --- | --- |
| Runtime | Course compose file, `core` profile, plus the `scrape` profile for the `sandbox-site` service. Versions pinned in `requirements.txt` |
| Scraping target | A local `sandbox-site` container only: a static practice shop with about 5 listing pages of 12 items each, its own robots.txt, and one disallowed path (for example `/admin/`). The mentor supplies the HTML files, the trainee adds the service to the compose file. No commercial site is scraped |
| Data | Synthetic and self-created, in the mounted `data/` folder |

## Labs

The Acceptance row is what the mentor checks.

### Lab 3.1: Datetime

| Step | What the trainee does |
| --- | --- |
| 1 | Creates a column of 30 timestamp strings in three formats (for example `2026-03-05 14:30`, `05/03/2026`, `Mar 5, 2026 2:30 PM`). Parses each group with an explicit format, and uses `errors="coerce"` on a deliberately bad value, counting the resulting NaTs |
| 2 | Makes the datetimes timezone-aware (Asia/Manila), converts to UTC, and shows both side by side |
| 3 | Derives year, month, weekday, and hour columns, and resamples to daily counts |
| 4 | Computes the time between two events with `timedelta` |
| **Acceptance** | Zero silent failures. The NaT count matches the number of bad inputs inserted |

### Lab 3.2: JSON, CSV, and Excel

| Step | What the trainee does |
| --- | --- |
| 1 | Creates a small nested JSON file (orders, each with a customer object and a list of items), loads it, flattens it to one row per item with `pd.json_normalize`, and saves it to CSV and Excel |
| 2 | Reads the CSV back with explicit `dtype` and `usecols`, reads the Excel file back, and verifies the three versions match with `DataFrame.equals` or an explicit comparison |
| 3 | Reads a larger CSV in chunks and computes a running total |
| **Acceptance** | Row counts match across formats. The trainee notes one thing that changed in a round trip (for example dtypes or dates) |

### Lab 3.3: Avro

| Step | What the trainee does |
| --- | --- |
| 1 | Defines an Avro schema for the flattened order-item table, using a `["null", "string"]` union for one optional field |
| 2 | Writes the records to `orders.avro` with `fastavro`, reads them back, and loads them into a DataFrame |
| 3 | Compares file sizes of CSV, JSON, and Avro for the same data in a small table |
| 4 | Adds a field to the schema and shows reading old data with the new schema |
| **Acceptance** | Round-trip data equals the original. The size comparison table is present |

### Lab 3.4: Web scraping (local sandbox)

| Step | What the trainee does |
| --- | --- |
| 1 | Adds the `sandbox-site` service (an nginx container serving `./sandbox_site`) under the `scrape` profile and starts it |
| 2 | Fetches the site's `robots.txt` and parses it with `urllib.robotparser`. Writes down in the notebook what it allows for the trainee's user agent and the date checked |
| 3 | Scrapes one listing page, extracting at least 4 fields per item (for example name, price, rating, link) with Beautiful Soup |
| 4 | Follows pagination across all pages with a delay between requests and a descriptive user-agent string |
| 5 | Adds a check that skips any URL robots.txt disallows, and shows it refusing the `/admin/` path |
| 6 | Cleans the results with pandas (price to float) and saves them to `data/products.csv` |
| Optional | Changes `robots.txt`, restarts the container, and shows the scraper's behavior changing without code edits |
| **Acceptance** | Delay, user-agent, and the robots.txt check are visible in code. The disallowed path is skipped. At least 30 records are collected |

## Deliverable

File: `module3_python_for_de.ipynb`.

The notebook contains:

- [ ] A title cell (trainee name, stage, date, Python version, image tag)
- [ ] Section 3.1: parsing, time zones, NaT handling, resample output
- [ ] Section 3.2: nested JSON flattening, CSV and Excel round trip, chunked read
- [ ] Section 3.3: schema, write and read round trip, size comparison table
- [ ] Section 3.4: robots.txt finding, scraper code, cleaned CSV preview
- [ ] Diagrams 3-A timestamp normalization, 3-B format conversion map, 3-C responsible scraping flow
- [ ] A debugging log with at least two real errors
- [ ] A reflection of 3 to 5 sentences
- [ ] A clean Kernel, Restart and Run All with no errors

The review rubric and pass mark are in [`../README.md`](../README.md).

## Still open / ask the trainer

| Question | Why it matters |
| --- | --- |
| Which timestamp normalization standard is the target? | Lab 3.1 step 2. The trainee proposes one with a justification and confirms it |
| How is a schema change handled for old data? | Lab 3.3 step 4. The brief does not prescribe a strategy |
| Is the optional scraping step expected? | Lab 3.4 optional row |
