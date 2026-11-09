# Module 2: Python Advance Brief

**Week:** 2 of 4 · **Builds on:** Module 1 (cleaned-record workflow and package habits) · **Feeds into:** Module 3

## Objective

By the end of this stage, the trainee loads a tabular dataset, inspects and cleans it, derives new columns, aggregates it, and exports the result with NumPy and pandas, and explains why vectorized operations beat Python loops. All work runs in the Jupyter container.

## Scope

| # | Subject | Time | Key concepts and terms | Research |
| --- | --- | --- | --- | --- |
| 2.1 | NumPy fundamentals | 4.5 h | `ndarray`, shape, dtype, axis, creation (`arange`, `zeros`, `random`), indexing and slicing, boolean masks, vectorization, broadcasting, aggregation along an axis, reshaping | What "axis" means for each aggregation |
| 2.2 | pandas basics | 3.5 h | Series, DataFrame, index, `head`/`tail`, dtypes, `describe`, `loc` and `iloc`, boolean filtering, sorting, missing data (NaN), `value_counts` | How one dtype per column (DataFrame) differs from one dtype per array (NumPy) |
| 2.3 | pandas transformation mini project | 2.5 h | Type casting, `fillna`/`dropna`, `drop_duplicates`, derived columns, `apply` vs vectorized string methods, `groupby` (split-apply-combine), `merge` and `concat`, pivoting, exporting results | When a per-row `apply` is still justified versus a vectorized operation |
| 2.4 | Notebook build, run-all check, mentor review | 1.5 h | See Deliverable | n/a |
| | **Total** | **12 h** | | |

## Stack constraints

| Constraint | Detail |
| --- | --- |
| Runtime | Everything runs in the `jupyter` container (`core` profile), versions pinned in `requirements.txt` |
| Data | Synthetic, self-created `sales.csv` in the mounted `data/` folder with at least 200 rows and deliberately planted missing values and duplicates |
| Dates | Kept as plain strings in this stage. Date handling belongs to Module 3 |

## Labs

Lab 2.2 and Lab 2.3 share one dataset. The Acceptance row is what the mentor checks.

### Lab 2.1: NumPy

| Step | What the trainee does |
| --- | --- |
| 1 | Creates a 1,000,000-element array and computes its mean with NumPy, then with a Python `for` loop. Times both with `%timeit` and records the ratio |
| 2 | Builds a 5x4 array of simulated daily sales (5 stores, 4 weeks). Computes the total per store (axis 1), the average per week (axis 0), and a boolean mask of cells above the overall mean |
| 3 | Demonstrates broadcasting by applying a per-store tax rate vector to the matrix |
| **Acceptance** | Timing comparison shown. Each aggregation is labelled with the axis used |

### Lab 2.2: pandas basics

| Step | What the trainee does |
| --- | --- |
| 1 | Creates a synthetic `sales.csv` in `data/` with at least 200 rows (`order_id`, `customer`, `product`, `category`, `quantity`, `unit_price`, `order_date`), with missing values and duplicates added on purpose |
| 2 | Loads it and reports shape, dtypes, null count per column, duplicate count, and summary statistics of numeric columns |
| 3 | Selects rows using `loc`, `iloc`, and a boolean filter, with one example of each |
| **Acceptance** | A short data-quality summary table is printed in the notebook |

### Lab 2.3: Transformation mini project

| Step | What the trainee does |
| --- | --- |
| 1 | Removes duplicates and decides, and documents, how to treat each column's missing values |
| 2 | Adds `revenue = quantity * unit_price` and a `size_band` column (small / medium / large) based on revenue |
| 3 | Produces revenue by category, top 5 customers by revenue, and average order value by month (dates stay plain strings) |
| 4 | Adds three `assert` statements (for example: no negative revenue, no duplicate `order_id`, row count after cleaning is at most the original) |
| 5 | Exports a cleaned CSV and a summary CSV to `data/` |
| **Acceptance** | Assertions pass. Every cleaning decision has a one-line justification in a markdown cell |

## Deliverable

File: `module2_python_advance.ipynb`.

The notebook contains:

- [ ] A title cell (trainee name, stage, date, Python version, image tag)
- [ ] Section 2.1: timing comparison, axis aggregations, boolean mask, broadcasting demo
- [ ] Section 2.2: data-quality summary table, `loc`/`iloc`/boolean filter examples
- [ ] Section 2.3: full cleaning and transformation workflow, assertions, exported CSVs
- [ ] Diagrams 2-A NumPy to pandas concept map and 2-B transformation pipeline (2-C join logic is optional)
- [ ] A debugging log with at least two real errors
- [ ] A reflection of 3 to 5 sentences
- [ ] A clean Kernel, Restart and Run All with no errors

The review rubric and pass mark are in [`../README.md`](../README.md).

## Still open / ask the trainer

| Question | Why it matters |
| --- | --- |
| How are the `size_band` thresholds decided? | Lab 2.3 step 2. The brief does not prescribe them |
| What treatment applies to each column's missing values? | Lab 2.3 step 1. The trainee proposes one per column and confirms the riskiest |
| Is the optional join diagram (2-C) expected? | Affects the diagram workload |
