# M3 Write-Up: Python for Data Engineering

## 1. Deliverable & Evidence

**Repository:** [ejandrea-strat/python-training](https://github.com/ejandrea-strat/python-training)

**Overview:** I parsed timestamps that arrive in three different formats from three source systems, normalized them to UTC, and moved order data between JSON, CSV, Excel and Avro to see what survives each round trip.

**Deliverable:** `module3_python_for_de.ipynb`, the Avro and CSV outputs, and the sandbox scraper

*   **DoD-3.1.2:** The count of unparseable timestamps next to the number of bad inputs inserted
    *   *Output/Evidence:* I scanned `timestamps.csv` by eye before parsing and found 2 bad values. After parsing each `source_system` with its own explicit format and `errors="coerce"`, exactly those 2 rows became NaT, and the assert passed.
        ```text
            event_id source_system                ts_raw
        7          8           erp            31/02/2026
        20        21           web  Marz 9, 2026 3:00 PM
        ```
        `event_id` 8 has no February 31; `event_id` 21 has "Marz", which isn't a valid month name. Expected 2, got 2.
 
*   **DoD-3.3.1:** The comparison showing the Avro round-trip data equals the original
    *   *Output/Evidence:* I wrote the 36 flattened item rows to `orders.avro` with fastavro, read the file back into a DataFrame, and compared it with the original.
        ```text
        Rows read back: 36
        Avro round trip matches the original
        ```
        The asserts check the row count (36) and `items_from_avro.equals(items_df)`. Missing emails come back as `None`, Avro's null.
 
*   **DoD-3.4.2:** The scraper refusing the disallowed path, with the robots.txt finding and the date it was checked
    *   *Output/Evidence:* TODO after Lab 3.4


## 2. How to build it (teach it to the next trainee)

**Guide scope:** from messy timestamp strings to format round trips and a compliant scraper against the local sandbox site

## 3. Decisions & Core Concepts

**Key Decisions**

*   **Which timestamp normalization target was chosen, and why?**
    UTC. The three source systems (crm, erp, web) each use their own format, so I split the rows by `source_system` and parsed each group with an explicit format: `%Y-%m-%d %H:%M`, `%d/%m/%Y` and `%b %d, %Y %I:%M %p`. I treated erp dates as day-first because values like `15/03/2026` can't be month-first. I localized everything to Asia/Manila, then converted to UTC for storage and comparison, and kept local time for date parts like weekday and hour, since those should follow the customer's clock.
    *Rejected:* letting `pd.to_datetime` guess the format for the whole column. It could read `02/03/2026` as Feb 3 instead of Mar 2, which gives a wrong date with no error at all.
*   **How are old records read after a schema change, and what alternatives were rejected?**
    With a reader schema. I added `order_status` (string, default `"unknown"`) to a copy of the schema and read the existing `orders.avro` with it. All 36 old rows came back with `"unknown"` and the file wasn't rewritten. I used `deepcopy` so the original schema stayed at 10 fields.
    *Rejected:* rewriting the old file into the new schema. It works for 36 rows, but on real data volumes it's slow and risks damaging data that was already correct.
*   **What scraping conduct (delay, client identity) was adopted, given what robots.txt allowed?**
    TODO after Lab 3.4


**Concepts Applied**

*   **Naive versus aware time.** After parsing, the timestamps were naive: they had a date and time but no time zone, so pandas didn't know whether `08:00` meant Manila or London. `tz_localize("Asia/Manila")` attached the zone without changing the clock time, and `tz_convert("UTC")` changed the clock time to match UTC. The clearest example was `event_id` 2: midnight on Mar 2 in Manila is 16:00 on Mar 1 in UTC, so even the date changes. If one system stored local time and another stored UTC, a daily report would put the same event on two different days. That's why pipelines store UTC and convert only for display.
*   **Schema-carrying formats.** An Avro file stores its schema in the file itself, so any later stage knows that `qty` is an int and `customer_email` can be null without anyone telling it. The schema is also enforced when writing: my first write failed because the missing emails were NaN (a float), and `customer_email` only accepts null or string. CSV would have quietly stored an empty cell, and in the 3.2 round trip the CSV and Excel read-backs each guessed differently (`<NA>` vs `NaN`). Avro also handles schema changes, as described above.


## 4. AI Collaboration Log

*   **Tools & Scope:** Claude, as a coach and reviewer across all of Module 3: explaining concepts, reviewing my code and explanations, and suggesting checks.
*   **Prompt Examples:**
    *   Asked why missing emails showed up as `None`, `<NA>` and `nan` in the three versions.
    *   Asked for help formatting my design cells and for the assert snippets after parsing and after the resample.
*   **Course Correction:**
    *   Claude said the invalid `31/02/2026` row was the reason Mar 6 showed 0 in the daily counts. I pointed out that a date that doesn't exist has no known intended date, so that can't be concluded. I kept my own explanation, which only says resample includes empty days.
*   **Human Intervention:** I wrote the parsing loop, the time zone conversion, the date parts, the `json_normalize` call, the chunked read (including `usecols=["amount"]` to load only one column), the Avro schema and write, and the schema evolution with `deepcopy`. I took these largely as given from Claude: the assert snippets for the NaT count and the resample total, the cell that shows the three null representations, and the formatted versions of my design cells. I rewrote the explanations in my own words.

## 5. Retrospective & Self-Assessment

*   **Friction Log (What tripped the trainee up):** (from the notebook's What broke section)
    *   `NameError: name 'customer' is not defined`: I wrote `*customer` in `json_normalize`'s `meta` as if it were a variable. Nested fields need a list path like `["customer", "id"]`.
    *   `ValueError: nan (type <class 'float'>) do not match ['null', 'string'] on field customer_email`: the missing emails were NaN when I first wrote the Avro file. Fixed by converting NaN to `None` with `.astype(object).where(items_df.notna(), None)`.
    *   `FutureWarning: Mismatched null-like values <NA> and None`: comparing the CSV read-back (`string` dtype, `<NA>`) with the original (`None` from JSON). Fixed by casting the original to the same dtypes before comparing.
    *   TODO: add any 3.4 errors (Docker, sandbox-site).
*   **What I'd do differently:** TODO at the end
*   **DoD Self-Assessment:** TODO at the end (DoD-3.1.2 and DoD-3.3.1 look Met so far)
*   **Blind Spots:** TODO at the end

