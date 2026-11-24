# M3 Write-Up: Python for Data Engineering

## 1. Deliverable & Evidence

**Repository:** [ejandrea-strat/python-training](https://github.com/ejandrea-strat/python-training)

**Overview:** I parsed timestamps that arrive in three different formats from three source systems, normalized them to UTC, and moved order data between JSON, CSV, Excel and Avro to see what survives each round trip. Lastly, I scraped a local sandbox while following its `robots.txt`.

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
    *   *Output/Evidence:* robots.txt checked on 2026-11-24 with my user agent (`AndreaTrainingScraper/1.0`). Every listing page is allowed, `/admin/` is disallowed, and the crawl delay is 1 second. The same `can_fetch` check runs before every request in the pagination loop; for `/admin/` it refuses without sending a request.

        ```text
        User-agent: *
        Disallow: /admin/
        Crawl-delay: 1
        
        Delay between requests (seconds): 1
        /page-1.html   allowed: True
        ...
        /page-5.html   allowed: True
        /admin/        allowed: False
        Skipped http://sandbox-site/admin/ because robots.txt disallows it.
        Collected 60 products across 5 pages.
        ```

## 2. How to build it (teach it to the next trainee)

**Guide scope:** from messy timestamp strings to format round trips and a compliant scraper against the local sandbox site

Do the labs in order (3.1 → 3.4). Each one builds on the last: 3.2's flat table becomes 3.3's Avro input, and the "parse, then check" habit from 3.1 carries through every lab.

### 3.1 Datetime: look before you parse
1. Open `timestamps.csv`. The `source_system` column tells you the format (crm, erp, web).
2. Scan the 30 rows and write down the bad ones. I found 2: `31/02/2026` and `Marz 9`.
3. Parse each source with its own format and `errors="coerce"`. I got exactly 2 NaTs, the same rows I'd flagged, so nothing failed silently.
4. Localize to Asia/Manila, then convert to UTC. `event_id` 2 went from Mar 2 00:00 in Manila to Mar 1 16:00 in UTC: the date itself changes, which is why timestamps should be stored in UTC.
5. Get date parts from local time and resample to daily counts: 28 valid events over 22 days.

**Watch out:** Mar 6 shows 0. That's normal, because resample keeps empty days.

### 3.2 JSON, CSV, Excel: count, then flatten
1. Count the items in the 12 orders first. There are 36, which gives you a number to check against.
2. Flatten with `json_normalize`: `record_path="items"`, plus `meta` for the order and customer fields. The result had 36 rows.
3. Save to CSV and Excel, then read both back. All three versions had 36 rows and 7 missing emails, but the missing emails appeared as `None`, `<NA>` and `NaN`. CSV and Excel only store an empty cell, so the reader decides what "missing" becomes.
4. Read `large_events.csv` in chunks of 10,000. It took 5 chunks, and the total matched a full read.

**Watch out:** `.equals()` fails at first. `usecols` keeps the file's column order, and `dtype="string"` turns `None` into `<NA>`. Match the order and dtypes before comparing.

### 3.3 Avro: schema first
1. Write the schema as a dict and check it with `parse_schema`.
2. Make `customer_email` optional: `["null", "string"]` with `"default": None`.
3. Convert NaN to `None`, then write, read back and compare. All 36 rows matched the original.
4. Compare file sizes for the same 36 rows: CSV 3,155 bytes, Avro 3,729 bytes, and Avro with `codec="deflate"` 1,029 bytes. Plain Avro loses to CSV here only because its schema header is large compared with so little data.
5. Add a field with a default, and read the old file with the new schema. All 36 rows got `order_status = "unknown"` without rewriting the file.

**Watch out:** writing NaN raises a `ValueError`, because Avro only accepts `None` as null.

### 3.4 Scraping: rules before requests
1. Add the `sandbox-site` nginx service under the `scrape` profile. (The mentor's files weren't in the repo, so the site was generated; see the AI log.)
2. Read `robots.txt` with your user agent. Mine allowed every page except `/admin/` and asked for a 1-second delay (checked 2026-11-24).
3. Inspect one product card in the browser to find the selectors.
4. Scrape page 1, then loop: check `can_fetch`, wait, fetch, parse, follow "Next". I collected 60 products across 5 pages, and `/admin/` was refused without a request.
5. Clean price and rating, then save the CSV. 8 products had no rating and became `NaN`.

**Watch out:** prices come out garbled (`â±`), because nginx sends no charset. Pass `response.content` to BeautifulSoup instead.


## 3. Decisions & Core Concepts

**Key Decisions**

**1. Which timestamp normalization target was chosen, and why?**

**UTC, because it's the one time zone every system can compare without guessing.**
- UTC has no daylight saving and no local offset, so a timestamp means the same moment everywhere.
- If one system stored Manila time and another stored UTC, the same event could land on different days. `event_id` 2 is Mar 2 00:00 in Manila but Mar 1 16:00 in UTC.
- To get there, I parsed each source with its own explicit format (crm `%Y-%m-%d %H:%M`, erp `%d/%m/%Y` day-first, web `%b %d, %Y %I:%M %p`), localized to Asia/Manila, then converted to UTC.
- I kept local time only for date parts like weekday and hour, since those should follow the customer's clock.

*Rejected:* storing local Manila time, which breaks as soon as data from another time zone arrives; and letting `pd.to_datetime` guess the formats, which could read `02/03/2026` as Feb 3 with no error.

**2. How are old records read after a schema change, and what alternatives were rejected?**

**Old records are read with a newer reader schema, and Avro fills in the new field's default.**
- I copied the schema (`deepcopy`, so the original stayed at 10 fields) and added `order_status` with the default `"unknown"`.
- Reading the old `orders.avro` with it gave all 36 rows `"unknown"`. The old file wasn't changed.

*Rejected:* rewriting old files into the new schema every time it changes. Fine for 36 rows, but slow on real data and risky for data that was already correct.

**3. What scraping conduct (delay, client identity) was adopted, given what robots.txt allowed?**

**A 1-second delay and a named user agent on every request, because that's what robots.txt asked for and it identifies who's crawling.**
- robots.txt allowed every listing page, blocked `/admin/`, and set `Crawl-delay: 1`.
- The scraper waits 1 second before each request (with a 1-second fallback if a site sets no delay).
- Every request, including robots.txt, sends `AndreaTrainingScraper/1.0 (Python Training Lab 3.4; contact: ...)`, so a site owner can see who's crawling and how to reach them.
- It checks `can_fetch` before every URL, and follows only the listing pages' "Next" links.

*Rejected:* scraping without a delay. Faster on a local site, but not acceptable on a real one, and building the habit is the point of the lab.

**Concepts Applied**

**1. Naive versus aware time**

- **Naive** time has a date and a clock time but no time zone. After parsing, `08:00` could have meant Manila or London; pandas didn't know.
- **Aware** time includes the zone, so it points to one exact moment.
- How I used it:
  - `tz_localize("Asia/Manila")` attached the zone **without changing the clock time**.
  - `tz_convert("UTC")` then **changed the clock time** to the same moment in UTC.
- Why it matters: `event_id` 2 is Mar 2 00:00 in Manila but Mar 1 16:00 in UTC, so even the date changes. If one system stored local time and another UTC, a daily report would count the same event on two different days. That's why pipelines store UTC and convert only for display.

**2. Schema-carrying formats**

- An Avro file stores its **schema inside the file**, so any later stage knows each field's type (`qty` is an int, `customer_email` can be null) without being told.
- How I used it:
  - **The schema is checked when writing.** My first write failed because missing emails were `NaN` (a float), and `customer_email` only accepts null or string.
  - **Old files still work after a schema change.** Reading the old file with a new field and a default filled in `"unknown"` for all 36 rows.
- Why it matters: CSV stores no types, only text and empty cells. In 3.2, the CSV and Excel read-backs each guessed differently what a missing email was (`<NA>` vs `NaN`). With Avro, the file itself says what the data is.

## 4. AI Collaboration Log

*   **Tools & Scope:** Claude, as a coach and reviewer across all of Module 3: explaining concepts, reviewing my code and explanations, and suggesting checks. Claude also generated the sandbox site for the `Lab 3.4`.
*   **Prompt Examples:**
    *   Asked why missing emails showed up as `None`, `<NA>` and `nan` in the three versions.
    *   Asked for help formatting my design cells and for the assert snippets after parsing and after the resample.
*   **Course Correction:**
    *   Claude said the invalid `31/02/2026` row was the reason Mar 6 showed 0 in the daily counts. I pointed out that a date that doesn't exist has no known intended date, so that can't be concluded. I kept my own explanation, which only says resample includes empty days.
*   **Human Intervention:**
    *   **Written by me:**
        *   3.1: the parsing loop, the time zone conversion and the date parts
        *   3.2: the `json_normalize` call and the chunked read (including `usecols=["amount"]` to load only one column)
        *   3.3: the Avro schema, the write and read-back, and the schema evolution with `deepcopy`
        *   3.4: the compose service, the robots.txt parsing, the pagination loop with the visited-pages guard, and the cleaning
    *   **Taken largely as given from Claude:**
        *   the assert snippets for the NaT count and the resample total
        *   the robots.txt path loop, the cleaning checks and the preview cell
        *   the formatting of my design cells and the What broke table
        *   the three Mermaid diagrams
        *   the sandbox site (`sandbox_site/` and its generator script). It's test data, not graded work
    *   **Writing:** most notebook explanations are in my own words. Where I kept Claude's wording, it's listed above.

## 5. Retrospective & Self-Assessment

*   **Friction Log (What tripped the trainee up):** (from the notebook's What broke section)
    *   `NameError: name 'customer' is not defined`: I wrote `*customer` in `json_normalize`'s `meta` as if it were a variable. Nested fields need a list path like `["customer", "id"]`.
    *   `ValueError: nan (type <class 'float'>) do not match ['null', 'string'] on field customer_email`: the missing emails were NaN when I first wrote the Avro file. Fixed by converting NaN to `None` with `.astype(object).where(items_df.notna(), None)`.
    *   `FutureWarning: Mismatched null-like values <NA> and None`: comparing the CSV read-back (`string` dtype, `<NA>`) with the original (`None` from JSON). Fixed by casting the original to the same dtypes before comparing.
    *   Prices came out as `â±4,199.00` and ratings as `â 3.4`: nginx sends `Content-Type: text/html` without a charset, so `requests` decoded the UTF-8 page as ISO-8859-1. Fixed by passing `response.content` (raw bytes) to BeautifulSoup, which reads the page's `<meta charset="utf-8">`.
    *   Most time spent: 3.2's round-trip comparison. `.equals()` kept failing on column order and dtypes, even though the data was the same.
*   **What I'd do differently:** Prepare everything the module needs before starting the first lab: all four packages in `requirements.txt`, the `sandbox-site` service, and a check that every provided file is actually in the repo. I rebuilt the Jupyter image three times mid-module, and only found out at Lab 3.4 that the sandbox site files were missing. One setup pass at the start would have kept the labs focused on the concepts.
*   **DoD Self-Assessment:**
    *   DoD-3.1.2: **Met**. 2 NaTs = the 2 bad inputs I flagged, asserted.
    *   DoD-3.3.1: **Met**. The Avro round trip equals the original, asserted.
    *   DoD-3.4.2: **Met**. `/admin/` refused without a request; robots.txt finding and date recorded.
    *   Rubric:

        | Criterion | Weight | Self-grade | Why |
        |---|---|---|---|
        | Completeness | 30% | 27 | Every section, exercise, diagram, What broke and reflection is present; the optional robots.txt stretch wasn't done |
        | Correctness | 30% | 28 | All acceptance checks pass with asserts, and Restart and Run All is clean |
        | Understanding | 20% | 13 | I can explain most concepts, but several explanations were reworded with AI help, so they show my understanding less directly |
        | Craft | 10% | 8 | Clear names, asserts after each step, and a loop guard; some cells could be split into small functions |
        | Reflection and debugging log | 10% | 8 | Four real errors with causes and fixes |
        | **Total** | | **84%** | Above the 70% pass mark |

*   **Blind Spots:**
    *   Explaining `json_normalize`'s `record_path` vs `meta` from memory. I needed a worked example before it clicked.
    *   Why each format shows missing values differently (`None`, `<NA>`, `NaN`), and when pandas picks which.
    *   How Avro matches a reader schema to an old file's writer schema beyond the simple "new field with a default" case, such as renamed or removed fields.

