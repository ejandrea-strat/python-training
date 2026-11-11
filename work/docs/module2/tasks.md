# Module 2: Python Advance Tasks

**Objective:** The trainee loads a tabular dataset, inspects and cleans it, derives new columns, aggregates it, and exports the result with NumPy and pandas, and explains why vectorized operations beat Python loops.

There is no solutions file for this stage. This checklist guides the work and does not contain it. Lab steps and acceptance rows live in `brief.md`; each task cites its source there.

## ID scheme

| Prefix | Meaning | Source in `brief.md` |
| --- | --- | --- |
| `R-2.x` | Research for subject 2.x | Scope table, Research column |
| `B-2.x.n` | Build, Lab 2.x step n | Lab 2.x, Step n |
| `V-2.x.n` | Verify, clause n of Lab 2.x Acceptance | Lab 2.x, Acceptance row |
| `DoD-<lab>.<n>` | Definition-of-done ID checked by the matching `V-` task, derived from the same Acceptance clause | Lab Acceptance row |

## Traceability

| Subject | Research | Build | Verify |
| --- | --- | --- | --- |
| 2.1 NumPy | R-2.1 | B-2.1.1 to B-2.1.3 | V-2.1.1, V-2.1.2 |
| 2.2 pandas basics | R-2.2 | B-2.2.1 to B-2.2.3 | V-2.2.1 |
| 2.3 Transformation mini project | R-2.3 | B-2.3.1 to B-2.3.5 | V-2.3.1, V-2.3.2 |

## Build

### Lab 2.1: NumPy

- [] **R-2.1** Research: what "axis" means for each aggregation (Scope 2.1).
- [x] **B-2.1.1** Create a 1,000,000-element array, compute its mean with NumPy and with a Python loop, time both with `%timeit`, and record the ratio (Lab 2.1 step 1).
- [x] **B-2.1.2** Build a 5x4 array of simulated daily sales and compute the total per store, the average per week, and a boolean mask of cells above the overall mean (Lab 2.1 step 2).
- [ ] **B-2.1.3** Demonstrate broadcasting by applying a per-store tax rate vector to the matrix (Lab 2.1 step 3).

### Lab 2.2: pandas basics

- [ ] **R-2.2** Research: how one dtype per column (DataFrame) differs from one dtype per array (NumPy) (Scope 2.2).
- [ ] **B-2.2.1** Create a synthetic `sales.csv` in `data/` with at least 200 rows and deliberately planted missing values and duplicates (Lab 2.2 step 1).
- [ ] **B-2.2.2** Load it and report shape, dtypes, nulls per column, duplicate count, and numeric summary statistics (Lab 2.2 step 2).
- [ ] **B-2.2.3** Select rows with `loc`, `iloc`, and a boolean filter, one example of each (Lab 2.2 step 3).

### Lab 2.3: Transformation mini project

- [ ] **R-2.3** Research: when a per-row `apply` is still justified versus a vectorized operation (Scope 2.3).
- [ ] **B-2.3.1** Remove duplicates and decide and document the treatment for each column's missing values (Lab 2.3 step 1).
- [ ] **B-2.3.2** Add the `revenue` column and a `size_band` column based on revenue (Lab 2.3 step 2).
- [ ] **B-2.3.3** Produce revenue by category, top 5 customers by revenue, and average order value by month, keeping dates as plain strings (Lab 2.3 step 3).
- [ ] **B-2.3.4** Add three `assert` statements about the cleaned data (Lab 2.3 step 4).
- [ ] **B-2.3.5** Export a cleaned CSV and a summary CSV to `data/` (Lab 2.3 step 5).

## Verify

Each task is a checkpoint criterion taken from the lab's Acceptance row and names the build tasks it validates.

### Lab 2.1

- [ ] **V-2.1.1** (DoD-2.1.1) Verify the timing comparison between the vectorized and looped computation is shown with the ratio. Validates B-2.1.1.
- [ ] **V-2.1.2** (DoD-2.1.2) Verify each aggregation is labelled with the axis it used. Validates R-2.1, B-2.1.2.

### Lab 2.2

- [ ] **V-2.2.1** (DoD-2.2.1) Verify a short data-quality summary table is printed in the notebook and matches the planted defects. Validates B-2.2.1, B-2.2.2.

### Lab 2.3

- [ ] **V-2.3.1** (DoD-2.3.1) Verify all assertions pass. Validates B-2.3.4.
- [ ] **V-2.3.2** (DoD-2.3.2) Verify every cleaning decision has a one-line justification in a markdown cell. Validates B-2.3.1, B-2.3.2.
