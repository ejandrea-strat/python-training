# Module 3: Python for Data Engineering Tasks

**Objective:** The trainee parses and normalizes messy timestamps, reads and writes JSON, CSV, Excel, and Avro, and collects web data responsibly from a local sandbox site.

There is no solutions file for this stage. This checklist guides the work and does not contain it. Lab steps and acceptance rows live in `brief.md`; each task cites its source there.

## ID scheme

| Prefix | Meaning | Source in `brief.md` |
| --- | --- | --- |
| `R-3.x` | Research for subject 3.x | Scope table, Research column |
| `B-3.x.n` | Build, Lab 3.x step n | Lab 3.x, Step n |
| `V-3.x.n` | Verify, clause n of Lab 3.x Acceptance | Lab 3.x, Acceptance row |
| `DoD-<lab>.<n>` | Definition-of-done ID checked by the matching `V-` task, derived from the same Acceptance clause | Lab Acceptance row |

## Traceability

| Subject | Research | Build | Verify |
| --- | --- | --- | --- |
| 3.1 Datetime | R-3.1 | B-3.1.1 to B-3.1.4 | V-3.1.1, V-3.1.2 |
| 3.2 JSON, CSV, Excel | R-3.2 | B-3.2.1 to B-3.2.3 | V-3.2.1, V-3.2.2 |
| 3.3 Avro | R-3.3 | B-3.3.1 to B-3.3.4 | V-3.3.1, V-3.3.2 |
| 3.4 Web scraping | R-3.4 | B-3.4.1 to B-3.4.6, B-3.4.7 (optional) | V-3.4.1 to V-3.4.3 |

## Build

### Lab 3.1: Datetime

- [x] **R-3.1** Research: why silent parsing failures are dangerous and how to make them loud (Scope 3.1).
- [x] **B-3.1.1** Create 30 timestamp strings in three formats, parse each group with an explicit format, and count the NaTs produced by a deliberately bad value (Lab 3.1 step 1).
- [x] **B-3.1.2** Make the datetimes timezone-aware, convert to UTC, and show both side by side (Lab 3.1 step 2).
- [x] **B-3.1.3** Derive year, month, weekday, and hour columns, and resample to daily counts (Lab 3.1 step 3).
- [x] **B-3.1.4** Compute the time between two events with `timedelta` (Lab 3.1 step 4).

### Lab 3.2: JSON, CSV, and Excel

- [x] **R-3.2** Research: what changes when data makes a round trip between formats (Scope 3.2).
- [x] **B-3.2.1** Create a small nested JSON file, flatten it to one row per item, and save it to CSV and Excel (Lab 3.2 step 1).
- [x] **B-3.2.2** Read the CSV back with explicit `dtype` and `usecols`, read the Excel file back, and compare the three versions (Lab 3.2 step 2).
- [x] **B-3.2.3** Read a larger CSV in chunks and compute a running total (Lab 3.2 step 3).

### Lab 3.3: Avro

- [ ] **R-3.3** Research: why a schema-carrying format matters for pipelines (Scope 3.3).
- [ ] **B-3.3.1** Define an Avro schema for the flattened order-item table with one optional field (Lab 3.3 step 1).
- [ ] **B-3.3.2** Write `orders.avro`, read it back, and load it into a DataFrame (Lab 3.3 step 2).
- [ ] **B-3.3.3** Compare file sizes of CSV, JSON, and Avro for the same data in a table (Lab 3.3 step 3).
- [ ] **B-3.3.4** Add a field to the schema and show reading old data with the new schema (Lab 3.3 step 4).

### Lab 3.4: Web scraping (local sandbox)

- [ ] **R-3.4** Research: the difference between "allowed by robots.txt" and "authorized" (Scope 3.4).
- [ ] **B-3.4.1** Add the `sandbox-site` service under the `scrape` profile and start it (Lab 3.4 step 1).
- [ ] **B-3.4.2** Fetch and parse the site's `robots.txt`, and write down what it allows for the trainee's user agent and the date checked (Lab 3.4 step 2).
- [ ] **B-3.4.3** Scrape one listing page, extracting at least 4 fields per item (Lab 3.4 step 3).
- [ ] **B-3.4.4** Follow pagination across all pages with a delay and a descriptive user-agent string (Lab 3.4 step 4).
- [ ] **B-3.4.5** Add a check that skips disallowed URLs and show it refusing the `/admin/` path (Lab 3.4 step 5).
- [ ] **B-3.4.6** Clean the results (price to float) and save them to `data/products.csv` (Lab 3.4 step 6).
- [ ] **B-3.4.7** (Optional) Change `robots.txt`, restart the container, and show the scraper's behavior changing without code edits (Lab 3.4 optional row).

## Verify

Each task is a checkpoint criterion taken from the lab's Acceptance row and names the build tasks it validates.

### Lab 3.1

- [ ] **V-3.1.1** (DoD-3.1.1) Verify there are zero silent parse failures. Validates R-3.1, B-3.1.1.
- [ ] **V-3.1.2** (DoD-3.1.2) Verify the NaT count matches the number of bad inputs inserted. Validates B-3.1.1.

### Lab 3.2

- [ ] **V-3.2.1** (DoD-3.2.1) Verify row counts match across the JSON-derived, CSV, and Excel versions. Validates B-3.2.1, B-3.2.2.
- [ ] **V-3.2.2** (DoD-3.2.2) Verify the trainee notes one thing that changed in a round trip. Validates R-3.2, B-3.2.2.

### Lab 3.3

- [ ] **V-3.3.1** (DoD-3.3.1) Verify the Avro round-trip data equals the original. Validates B-3.3.2.
- [ ] **V-3.3.2** (DoD-3.3.2) Verify the size comparison table is present. Validates B-3.3.3.

### Lab 3.4

- [ ] **V-3.4.1** (DoD-3.4.1) Verify the delay, user-agent, and robots.txt check are visible in code. Validates B-3.4.2, B-3.4.4, B-3.4.5.
- [ ] **V-3.4.2** (DoD-3.4.2) Verify the disallowed path is skipped. Validates B-3.4.5.
- [ ] **V-3.4.3** (DoD-3.4.3) Verify at least 30 records are collected. Validates B-3.4.3, B-3.4.4, B-3.4.6.
