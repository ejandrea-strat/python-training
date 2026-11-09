# Module 1: Python Intermediate Tasks

**Objective:** The trainee writes clean, reusable Python that reads a text file, validates each record, handles failures, and produces a cleaned output, packaged and run from a container terminal.

There is no solutions file for this stage. This checklist guides the work and does not contain it. Lab steps and acceptance rows live in `brief.md`; each task cites its source there.

## ID scheme

| Prefix | Meaning | Source in `brief.md` |
| --- | --- | --- |
| `R-1.x` | Research for subject 1.x | Scope table, Research column |
| `B-1.x.n` | Build, Lab 1.x step n | Lab 1.x, Step n |
| `V-1.x.n` | Verify, clause n of Lab 1.x Acceptance | Lab 1.x, Acceptance row |
| `DoD-<lab>.<n>` | Definition-of-done ID checked by the matching `V-` task, derived from the same Acceptance clause | Lab Acceptance row |

## Traceability

| Subject | Research | Build | Verify |
| --- | --- | --- | --- |
| 1.1 Comprehensions | R-1.1 | B-1.1.1 to B-1.1.3 | V-1.1.1, V-1.1.2 |
| 1.2 Packages and environments | R-1.2 | B-1.2.1 to B-1.2.4 | V-1.2.1, V-1.2.2 |
| 1.3 Exception handling | R-1.3 | B-1.3.1 to B-1.3.3 | V-1.3.1, V-1.3.2 |
| 1.4 Text files | R-1.4 | B-1.4.1 to B-1.4.4 | V-1.4.1 |
| 1.5 Functions | R-1.5 | B-1.5.1 to B-1.5.3 | V-1.5.1 |
| 1.6 Lambda functions | R-1.6 | B-1.6.1, B-1.6.2 | V-1.6.1 |
| 1.7 Object-oriented programming | R-1.7 | B-1.7.1 to B-1.7.5, B-1.7.6 (optional) | V-1.7.1 to V-1.7.3 |
| 1.8 Modular programming | R-1.8 | B-1.8.1 to B-1.8.6 | V-1.8.1 to V-1.8.3 |

## Build

### Lab 1.1: Comprehensions

- [x] **R-1.1** Research: when a plain loop is the better choice than a comprehension (Scope 1.1).
- [x] **B-1.1.1** Build a cleaned list of floats from 20 messy amount strings with one comprehension that strips, converts, and drops values at or below zero (Lab 1.1 step 1).
- [x] **B-1.1.2** Rewrite the same logic as a plain `for` loop and compare readability (Lab 1.1 step 2).
- [x] **B-1.1.3** Build a dictionary comprehension mapping product name to total quantity (Lab 1.1 step 3).

### Lab 1.2: Packages and reproducible environments

- [x] **R-1.2** Research: when an isolated environment is needed inside a container, and when the image alone is enough (Scope 1.2).
- [x] **B-1.2.1** Import one standard library module and one third-party package in the notebook (Lab 1.2 step 1).
- [x] **B-1.2.2** Add the third-party package to `requirements.txt` with a pinned version, rebuild the image, restart the container, and confirm the import works (Lab 1.2 step 2).
- [x] **B-1.2.3** Create a virtual environment in a scratch folder, install a different version of the same package, and show the two environments report different versions (Lab 1.2 step 3).
- [x] **B-1.2.4** Write two or three sentences on when a virtual environment is needed inside a container (Lab 1.2 step 4).

### Lab 1.3: Exception handling

- [x] **R-1.3** Research: why catching the most specific error matters (Scope 1.3).
- [x] **B-1.3.1** Write `safe_to_float(value)` that returns a float or raises a clear message for bad input (Lab 1.3 step 1).
- [x] **B-1.3.2** Feed it valid numbers, empty strings, letters, and `None`; catch specific exceptions and count each type (Lab 1.3 step 2).
- [x] **B-1.3.3** Demonstrate `else` and `finally` with a real example (Lab 1.3 step 3).

### Lab 1.4: Text files

- [x] **R-1.4** Research: where files written inside the container appear on the host (Scope 1.4).
- [x] **B-1.4.1** Create `orders_raw.txt` in the mounted `data/` folder: at least 30 lines, 5 broken lines, one blank line, one line with extra whitespace (Lab 1.4 step 1).
- [x] **B-1.4.2** Read it line by line with `with open(...)`, writing valid rows to `clean_orders.csv` and invalid rows to `rejects.log` with line number and reason (Lab 1.4 step 2).
- [x] **B-1.4.3** Handle a missing input file (Lab 1.4 step 3).
- [x] **B-1.4.4** Confirm the output files appear on the host machine (Lab 1.4 step 4).

### Lab 1.5: Functions

- [x] **R-1.5** Research: the mutable-default-argument trap (Scope 1.5).
- [x] **B-1.5.1** Refactor the Lab 1.4 script into at least four documented functions (`read_lines`, `parse_record`, `validate_record`, `write_outputs`) (Lab 1.5 step 1).
- [x] **B-1.5.2** Show one function with a default argument and one called with keyword arguments (Lab 1.5 step 2).
- [x] **B-1.5.3** Demonstrate the mutable-default-argument trap and the `None` fix (Lab 1.5 step 3).

### Lab 1.6: Lambda functions

- [x] **R-1.6** Research: when not to use a lambda (Scope 1.6).
- [x] **B-1.6.1** Sort a list of order dictionaries by amount descending with `sorted(..., key=lambda ...)` (Lab 1.6 step 1).
- [x] **B-1.6.2** Apply a 12% tax with `map` and a lambda, then redo it as a list comprehension (Lab 1.6 step 2).

### Lab 1.7: Object-oriented programming

- [x] **R-1.7** Research: when a function is enough and a class is not needed (Scope 1.7).
- [x] **B-1.7.1** Write the `OrderRecord` class with `__init__`, `total()`, a readable `__repr__`, and a `ValueError` for non-positive quantity (Lab 1.7 step 1).
- [x] **B-1.7.2** Add a class attribute counting records created; show how it differs from an instance attribute and what assigning through an instance does (Lab 1.7 step 2).
- [x] **B-1.7.3** Write the `OrderReader` base class and the `TextOrderReader` and `CsvOrderReader` subclasses, using `super()` in at least one (Lab 1.7 step 3).
- [x] **B-1.7.4** Write `load_orders(reader)` that works unchanged with either reader (Lab 1.7 step 4).
- [x] **B-1.7.5** Write the `OrderPipeline(reader, writer)` class with a `run()` method returning valid and rejected counts (Lab 1.7 step 5).
- [ ] **B-1.7.6** (Optional) Rewrite `OrderRecord` with the standard library `dataclasses` module (Lab 1.7 optional step).

### Lab 1.8: Modular Python programming

- [ ] **R-1.8** Research: how a circular import fails and how to remove it (Scope 1.8).
- [x] **B-1.8.1** Convert the Lab 1.4 to 1.7 code into the `orders_pipeline/` package with the seven listed files (Lab 1.8 step 1).
- [x] **B-1.8.2** Give every module a one-sentence single-responsibility docstring (Lab 1.8 step 2).
- [x] **B-1.8.3** Deliberately create a circular import, read the error, fix it by moving shared code, and record it in the debugging log (Lab 1.8 step 3).
- [x] **B-1.8.4** Add `check_pipeline.py` with three `assert` statements: counts add up, no negative totals, rejected rows have reasons (Lab 1.8 step 4).
- [x] **B-1.8.5** Run the package from the container terminal and confirm it produces the same `clean_orders.csv` as Lab 1.4 (Lab 1.8 step 5).
- [x] **B-1.8.6** Import from the package in the notebook with cells of about 10 lines or fewer, and show the folder tree and one module's contents (Lab 1.8 step 6).

## Verify

Each task is a checkpoint criterion taken from the lab's Acceptance row and names the build tasks it validates.

### Lab 1.1

- [ ] **V-1.1.1** (DoD-1.1.1) Verify the comprehension and the loop produce identical results. Validates B-1.1.1, B-1.1.2.
- [ ] **V-1.1.2** (DoD-1.1.2) Verify the trainee explains in one sentence when a loop is the better choice. Validates R-1.1.

### Lab 1.2

- [ ] **V-1.2.1** (DoD-1.2.1) Verify the environment is rebuilt from `requirements.txt` alone. Validates B-1.2.2.
- [ ] **V-1.2.2** (DoD-1.2.2) Verify the notebook prints both package versions and the `requirements.txt` contents. Validates B-1.2.2, B-1.2.3.

### Lab 1.3

- [ ] **V-1.3.1** (DoD-1.3.1) Verify no bare `except:` appears in the code. Validates B-1.3.1, B-1.3.2.
- [ ] **V-1.3.2** (DoD-1.3.2) Verify counts per error type are printed. Validates B-1.3.2.

### Lab 1.4

- [ ] **V-1.4.1** (DoD-1.4.1) Verify valid plus rejected record counts equal the total non-blank lines in `orders_raw.txt`. Validates B-1.4.1 to B-1.4.3.

### Lab 1.5

- [ ] **V-1.5.1** (DoD-1.5.1) Verify the main script is under 15 lines and only calls functions. Validates B-1.5.1.

### Lab 1.6

- [ ] **V-1.6.1** (DoD-1.6.1) Verify the trainee notes one case where a named function is clearer than a lambda. Validates R-1.6, B-1.6.1.

### Lab 1.7

- [ ] **V-1.7.1** (DoD-1.7.1) Verify the pipeline runs with both readers without any change to `OrderPipeline`. Validates B-1.7.3 to B-1.7.5.
- [ ] **V-1.7.2** (DoD-1.7.2) Verify the trainee explains in two or three sentences why the pipeline uses composition instead of inheriting from a reader. Validates R-1.7, B-1.7.5.
- [ ] **V-1.7.3** (DoD-1.7.3) Verify at least five `OrderRecord` objects print cleanly via `__repr__`. Validates B-1.7.1.

### Lab 1.8

- [ ] **V-1.8.1** (DoD-1.8.1) Verify no function or class is defined twice across the package. Validates B-1.8.1.
- [ ] **V-1.8.2** (DoD-1.8.2) Verify the notebook contains no copy-pasted package code. Validates B-1.8.6.
- [ ] **V-1.8.3** (DoD-1.8.3) Verify the terminal run and the notebook run give identical output files. Validates B-1.8.5, B-1.8.6.
