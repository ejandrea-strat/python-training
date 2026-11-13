# M2 Write-Up: Python Advance

## 1. Deliverable & Evidence

**Repository:** [ejandrea-strat/python-training](https://github.com/ejandrea-strat/python-training)

**Overview:** I used NumPy to compare vectorized and looped code, aggregate along axes and broadcast per-store values, then used pandas to profile a messy sales file, clean it, add revenue and size bands, summarize it, check it with assertions, and export the results.
**Deliverable:** `module2_python_advance.ipynb`, with the cleaned and summary CSVs in `data/module2/`

*   **DoD-2.1.1:** The timing output for the vectorized and looped computation, with the measured ratio
    *   *Output/Evidence:*
        ```
        NumPy mean: 256 μs
        Loop mean:  49.2 ms
        NumPy is about 192x faster
        ```
*   **DoD-2.2.1:** The data-quality summary table, matched against the defects the trainee planted
    *   *Output/Evidence:* I used the provided `sales.csv` instead of generating one (same approach as `orders_raw.txt` in Lab 1.4), so the table is matched against the file's known defects: missing values in 5 columns and 12 exact duplicate rows.
        ```
        Rows and Columns: (240, 7) | Duplicate rows: 12

        Quality:
                      dtype  nulls  null_%  unique
        order_id     object      0     0.0     228
        customer     object      8     3.3      20
        product      object      0     0.0      10
        category     object      7     2.9       3
        quantity    float64      6     2.5      12
        unit_price  float64      5     2.1      31
        order_date   object      3     1.2     134
        ```
*   **DoD-2.3.1:** The output of the passing assertions on the cleaned data
    *   *Output/Evidence:*
        ```python
        assert (df["revenue"] >= 0).all(), f"Negative revenue in {(df['revenue'] < 0).sum()} rows"
        assert df["order_id"].is_unique, f"{df['order_id'].duplicated().sum()} duplicate order_ids"
        assert len(df) <= len(sales), "Cleaning added rows?"
        ```
        ```
        All checks passed
        ```

## 2. How to build it (teach it to the next trainee)

**Guide scope:** from a raw synthetic sales file to cleaned and summary CSVs with passing assertions

1. **Profile before you touch anything.** Load the file and print the shape, a quality table (dtype, nulls, null %, unique per column), the duplicate count and `describe()`. Write down what you find in a markdown cell. Mine: nulls in customer (8), category (7), quantity (6), unit_price (5) and order_date (3), 12 duplicate rows, and three `unit_price` values of 999.99 when 75% of prices are 25 or less. These findings become your cleaning to-do list.
2. **Decide before you code.** For every finding, decide drop, fill or keep, with a one-line reason. Deciding first keeps the cleaning code short and makes the decisions table easy.
3. **Drop first, then fill.** I dropped duplicates (240 → 228), then the 999.99 rows (228 → 225), then rows missing quantity or unit_price (225 → 214). Drops come first so that the fills and counts only touch rows you're keeping. Print the row count after every step; those numbers are your evidence.
4. **Fix the types.** quantity was float64 only because NaN is a float. After dropping the missing rows, `astype(int)` turns it back. Add `.copy()` when you create a filtered DataFrame, or pandas warns with `SettingWithCopyWarning` when you change a column.
5. **Fill what's left.** customer → `"Unknown"`. category → looked up from product, after proving with `groupby("product")["category"].nunique()` that every product has exactly one category. order_date stays missing.
6. **Derive columns.** `revenue = quantity * unit_price`, check its spread with `describe()`, then cut `size_band` with `pd.cut` using thresholds based on the quartiles.
7. **Summarize with groupby.** Revenue by category, top 5 customers (excluding "Unknown"), and average order value by month (month = first 7 characters of order_date).
8. **Assert, then export.** Three asserts, then `to_csv(index=False)` for the cleaned data and `reset_index()` + `to_csv(index=False)` for the summary, so the group labels stay a named column. Read both files back to check them.

## 3. Decisions & Core Concepts

**Key Decisions**

*   **What treatment was chosen for each column's missing values, and why?:** 

    1. I dropped rows missing quantity or unit_price, because revenue needs both and there's no safe value to fill in. 
    2. Missing customers became `"Unknown"`, so the order's revenue still counts and the placeholder is obvious. 
    3. For missing categories, I initially wanted to label them "unknown", but since each product belongs to exactly one category, I filled them from the rows that already had one, using a product → category lookup with `.map()` inside `.fillna()`. I rejected `ffill`, because row order has nothing to do with category, so it would copy a neighbour's category onto the wrong product. 
    4. Missing order dates stay missing: dates are plain strings in this module, and a fake value would create a bogus month. Those 3 rows only drop out of the monthly table. 
    5. I also dropped the three 999.99 prices, because the same price shows up on three unrelated products (Stapler, Mouse, Chair Mat) and sits about 40 times above the 75% mark, so it's a placeholder, not a real price.
*   **How were the `size_band` thresholds decided?:** 
    1. I computed revenue first and looked at its spread: median 59, mean 103, max 480, so it's skewed and equal-width bands would put almost everything in Small. 
    2. I used the quartiles (25% at 22, 75% at 160) and rounded them: Small ≤ 25, Medium 25–150, Large > 150. That gives 68 / 88 / 58 of 214 rows, roughly the bottom quarter, the middle and the top quarter. `pd.cut` includes the right edge, so exactly 25 is Small and exactly 150 is Medium, and `np.inf` as the last edge means any future order above 150 still lands in Large.
*   **Where was per-row logic still justified over a vectorized operation?:** A per-row `apply()` is fine when your dataset is small enough that speed doesn't matter, when vectorizing messy logic would ruin readability, or when there's no vectorized version at all. None of the lab needed apply, since revenue, size_band, and month were all vectorized.

**Concepts Applied**

**Axis aggregation:** 

An axis defines which direction an aggregation function aggregates the data in. axis=0 collapses the rows (downwards), so it gives one result per column, and axis=1 squashes the columns (horizontally), which gives one result per row. In the 5 rows × 4 columns array lab, `sales.mean(axis=0)` gave 4 values (one average per week) and `sales.sum(axis=1)` gave 5 (one total per store). My mind trick is a Cartesian plane: axis=0 goes down from the center, and axis=1 goes right.

**Broadcasting:** 

NumPy tries to match 1D arrays to columns first, so reshape them to (n, 1) when you want to go down the rows. My 5 per-store tax rates had shape (5,), so multiplying them with the (5, 4) sales array failed. After `tax.reshape(5, 1)`, each store's rate stretched across its 4 weeks.

**Split-apply-combine:** 

NumPy can only handle one datatype because it stores everything in one single block of memory; if an input with a different type gets mixed in, everything gets upcast to one common type. A DataFrame keeps each column as a separate NumPy array and links them like a table, which is why it supports multiple data types: in the sales data, quantity is float64 and customer is object. groupby builds on that: it splits the rows by a key like category or month, applies a sum or a count to each group, and combines the results into one table, like my revenue by category and average order value by month.

## 4. AI Collaboration Log

*   **Tools & Scope:** Claude, used throughout the module: lessons and explanations for each lab, reviewing my code and written answers, explaining errors, formatting print statements and markdown tables (the What broke and cleaning decisions tables), and giving code skeletons with blanks for parts I was stuck on (the category lookup and diagram 2-B). I wrote the lab code and the written answers myself, then reviewed and edited the write-up.
*   **Prompt Examples:**
    1. "Won't ffill() accidentally copy the category from a different product if the rows aren't grouped?" (B-2.3.1). It explained that ffill copies the previous row's category regardless of product, so I used a product lookup instead.
    2. "Does np.inf work as an open-ended upper bound for the Large bin here?" (B-2.3.2). It explained it's the open top edge of the Large band.
*   **Course Correction:**
    - In B-2.1.3, Claude first suggested computing net sales (removing tax), then wobbled on the formula. I asked what the task actually wanted: it says "apply" a tax rate, so I multiplied to get sales with tax added.
*   **Human Intervention:** I accepted the print formatting and markdown table layouts largely as-is. I wrote the lab code, the findings, the R-2.x answers, the reflection and the What broke lesson myself, made all the cleaning and size_band decisions, chose the 999.99 handling from my own profiling, and built the category lookup with `to_dict()` instead of the suggested `drop_duplicates` version.

## 5. Retrospective & Self-Assessment

*   **Friction Log (What tripped the trainee up):**
    - **Broadcasting:** Got `ValueError: operands could not be broadcast together with shapes (5,4) (5,)` in B-2.1.3 because NumPy tried to match the 5 tax rates with the 4 week columns. Fixed it by reshaping `tax` to `(5, 1)`, though I accidentally hit the same error twice because I ran `tax.reshape(5, 1)` without saving it back to the `tax` variable first.
    - **`%timeit -o` returned None** in B-2.1.1 because I used it as a cell magic without a statement. Fixed by timing a one-line function call.
    - **`SettingWithCopyWarning`** when casting quantity to int in B-2.3.1. The DataFrame came from a filter and `dropna`. Fixed with `.copy()`.
    - **Wrong filter direction:** I first wrote `== 999.99`, which kept only the bad rows. Fixed with `!=`.
    - **Git:** I committed Jupyter's `work/.Trash-0` folder, then ran the "not pushed" fix after already pushing. Fixed with `git push --force-with-lease`, `git rm -r --cached work/.Trash-0` and a `.Trash-*/` line in `.gitignore`.
    - **Time:** most days started late, so Lab 2.3 and the notebook wrap-up ended up packed into the last two days.
*   **What I'd do differently:** Start the blocks on time, and always check `.shape` first before aligning arrays.
*   **DoD Self-Assessment:**
    - DoD-2.1.1: Met. NumPy 256 μs vs loop 49.2 ms, about 192x faster.
    - DoD-2.2.1: Met. The quality table shows the file's 5 columns with nulls and 12 duplicates. The defects came with the provided file rather than being planted by me.
    - DoD-2.3.1: Met. All three assertions pass on the cleaned data, and both CSVs are exported.
    - Rubric: about 80%. Completeness and correctness are strong; understanding is good for the parts I reasoned through, but I leaned on Claude's formatting and skeletons.
*   **Blind Spots:** I'd struggle to explain broadcasting rules beyond the (n, 1) case, and exactly when pandas returns a view versus a copy, without re-reading first.