# Module 1: Python Intermediate Brief

**Week:** 1 of 4 · **Builds on:** none (course entry point) · **Feeds into:** Module 2

## Objective

By the end of this stage, the trainee writes clean, reusable Python that reads a text file, validates each record, handles failures, and produces a cleaned output, then packages it as a small multi-file Python package run from the terminal inside the Jupyter container.

## Scope

| # | Subject | Time | Key concepts and terms | Research |
| --- | --- | --- | --- | --- |
| 1.1 | List comprehensions | 1.5 h | Syntax (expression, for, optional if), nested comprehensions, readability limits, `map()`/`filter()`, iterables | When a plain loop is the better choice |
| 1.2 | Packages and reproducible environments | 1.0 h | Module vs package, `import` vs `from ... import`, standard library vs third-party, PyPI, pip, `requirements.txt`, version pinning, isolation | When an isolated environment is needed inside a container, and when the image alone is enough |
| 1.3 | Exception handling | 1.5 h | Syntax error vs exception, `try`/`except`/`else`/`finally`, specific exception types, re-raising, `raise`, `ValueError`, `FileNotFoundError` | Why catching the most specific error matters |
| 1.4 | Text files | 1.5 h | `open()` and modes (r, w, a, b), text vs binary, encoding, the `with` statement, line by line vs all at once, container file paths (mounted volumes) | Where files written in the container appear on the host |
| 1.5 | Functions | 1.5 h | `def`, parameters, return values, default and keyword arguments, `*args`/`**kwargs`, docstrings, scope, single responsibility | The mutable-default-argument trap |
| 1.6 | Lambda functions | 1.0 h | Anonymous function, lambda vs `def`, `key=` in `sorted()`, `map`/`filter` | When not to use a lambda |
| 1.7 | Object-oriented programming | 2.5 h | Class vs object, `__init__` and `self`, instance vs class attributes, methods, `__repr__`/`__str__`, encapsulation by naming convention, inheritance, overriding, `super()`, polymorphism, abstract-style base class (`NotImplementedError`), composition vs inheritance | When a function is enough |
| 1.8 | Modular Python programming | 2.0 h | Module vs package (`__init__.py`), absolute vs relative imports, module search path, `if __name__ == "__main__":`, entry point, separation of concerns, circular imports, project layout, thin notebooks (`%autoreload`) | How a circular import fails and how to remove it |
| 1.9 | Notebook build, run-all check, mentor review | 1.5 h | See Deliverable | n/a |
| | **Total** | **14 h** | | |

## Stack constraints

| Constraint | Detail |
| --- | --- |
| Runtime | Everything runs in the `jupyter` container from the course compose file (`core` profile), Python 3.11 or newer |
| Environment | Dependencies come from a pinned `requirements.txt`. The image is rebuilt, never changed in a running container. The image tag is recorded in the notebook |
| Data | Self-created, synthetic order data in the mounted `data/` folder, visible on the host machine |

## Labs

Each lab builds on the previous one. The Acceptance row is what the mentor checks.

### Lab 1.1: Comprehensions

| Step | What the trainee does |
| --- | --- |
| 1 | Takes a list of 20 order amounts as strings (such as `" 12.50 "`) and builds a cleaned list of floats with one comprehension that strips, converts, and drops values at or below zero |
| 2 | Rewrites the same logic as a plain `for` loop and compares readability |
| 3 | Builds a dictionary comprehension that maps product name to total quantity |
| **Acceptance** | Both versions give identical results. The trainee explains in one sentence when a loop is the better choice |

### Lab 1.2: Packages and reproducible environments

| Step | What the trainee does |
| --- | --- |
| 1 | Imports one standard library module and one third-party package (for example `rich` or `tabulate`) in the notebook |
| 2 | Adds the third-party package to `requirements.txt` with a pinned version, rebuilds the image (`docker compose build jupyter`), restarts the container, and confirms the import works |
| 3 | Creates a virtual environment in a scratch folder (`python -m venv`), installs a different version of the same package, and shows the two environments report different versions |
| 4 | Writes two or three sentences on when a virtual environment is needed inside a container and when the image alone is enough |
| **Acceptance** | The environment is rebuilt from `requirements.txt` alone. The notebook prints both package versions and the file contents |

### Lab 1.3: Exception handling

| Step | What the trainee does |
| --- | --- |
| 1 | Writes `safe_to_float(value)`, which returns a float or raises a clear message for bad input |
| 2 | Feeds it valid numbers, empty strings, letters, and `None`, catches specific exceptions, and counts each type |
| 3 | Demonstrates `else` and `finally` with a real example |
| **Acceptance** | No bare `except:`. Counts per error type are printed |

### Lab 1.4: Text files

| Step | What the trainee does |
| --- | --- |
| 1 | Creates `orders_raw.txt` in the mounted `data/` folder: at least 30 lines, including 5 deliberately broken lines, a blank line, and one line with extra whitespace |
| 2 | Reads it with `with open(...)`, processes it line by line, and writes valid rows to `clean_orders.csv` and invalid rows to `rejects.log` with line number and reason |
| 3 | Handles a missing input file |
| 4 | Confirms the output files appear on the host machine (volume mount check) |
| **Acceptance** | Valid plus rejected counts equal the total non-blank lines |

### Lab 1.5: Functions

| Step | What the trainee does |
| --- | --- |
| 1 | Refactors the Lab 1.4 script into at least four functions (`read_lines`, `parse_record`, `validate_record`, `write_outputs`), each with a docstring |
| 2 | Shows one function with a default argument and one called with keyword arguments |
| 3 | Demonstrates the mutable-default-argument trap and the `None` fix |
| **Acceptance** | The main script is under 15 lines and only calls functions |

### Lab 1.6: Lambda functions

| Step | What the trainee does |
| --- | --- |
| 1 | Sorts a list of order dictionaries by amount (descending) with `sorted(..., key=lambda ...)` |
| 2 | Applies a 12% tax with `map` and a lambda, then redoes it as a list comprehension |
| **Acceptance** | The trainee notes one case where a named function is clearer than a lambda |

### Lab 1.7: Object-oriented programming

| Step | What the trainee does |
| --- | --- |
| 1 | Writes an `OrderRecord` class with `__init__` (`order_id`, `product`, `quantity`, `unit_price`), a `total()` method, and a readable `__repr__`. It raises `ValueError` when quantity is zero or negative (reuses Lab 1.3) |
| 2 | Adds a class attribute that counts records created. Shows how it differs from an instance attribute and what happens when it is assigned through an instance |
| 3 | Writes a base class `OrderReader` whose `read()` raises `NotImplementedError`, and two subclasses: `TextOrderReader` (reads `orders_raw.txt`) and `CsvOrderReader`. Uses `super()` in at least one subclass |
| 4 | Writes `load_orders(reader)` that works unchanged with either reader (polymorphism) |
| 5 | Writes an `OrderPipeline(reader, writer)` class that holds a reader and a writer and has a `run()` method returning counts of valid and rejected records (composition) |
| Optional | Rewrites `OrderRecord` with the standard library `dataclasses` module |
| **Acceptance** | The pipeline runs with both readers without changing `OrderPipeline`. The trainee explains in two or three sentences why it uses composition instead of inheriting from a reader. At least five `OrderRecord` objects print cleanly via `__repr__` |

### Lab 1.8: Modular Python programming

| Step | What the trainee does |
| --- | --- |
| 1 | Converts the Lab 1.4 to 1.7 code into a package folder `orders_pipeline/` with `__init__.py`, `models.py`, `readers.py`, `validators.py`, `writers.py`, `pipeline.py`, and `__main__.py` as the entry point |
| 2 | Gives every module a one-sentence docstring stating its single responsibility |
| 3 | Deliberately creates a circular import (for example `models.py` importing from `pipeline.py`), reads the error, fixes it by moving shared code, and records it in the debugging log |
| 4 | Adds `check_pipeline.py` with three `assert` statements (counts add up, no negative totals in the output, rejected rows have reasons) |
| 5 | Runs the package from a terminal in the Jupyter container (`python -m orders_pipeline`) and confirms it produces the same `clean_orders.csv` as Lab 1.4 |
| 6 | Imports from the package in the notebook, keeping each cell to about 10 lines or fewer, and shows the folder tree and one module's contents |
| **Acceptance** | No function or class is defined twice. The notebook has no copy-pasted package code. The terminal run and the notebook run give identical output files |

## Deliverable

Files: `module1_python_intermediate.ipynb`, the `orders_pipeline/` folder, and `requirements.txt`. The notebook imports the package and does not duplicate it.

The notebook contains:

- [ ] A title cell (trainee name, stage, date, Python version, image tag)
- [ ] One section per lab, 1.1 to 1.8, with code and printed output
- [ ] An integration section: the package running end to end from the notebook and from the container terminal
- [ ] Diagrams 1-A exception flow, 1-B text-file mini pipeline, 1-C class design, 1-D package structure (source or image)
- [ ] Evidence: `requirements.txt` output, `clean_orders.csv` preview, `rejects.log` preview, folder tree, `check_pipeline.py` passing
- [ ] A debugging log with at least two real errors, including the circular import
- [ ] A reflection of 3 to 5 sentences
- [ ] A clean Kernel, Restart and Run All with no errors

The review rubric and pass mark are in [`../README.md`](../README.md).

## Still open / ask the trainer

| Question | Why it matters |
| --- | --- |
| Where does the boundary sit between a function, a class, and a module? | Labs 1.5, 1.7 and 1.8 depend on it. The brief does not prescribe it |
| What reject policy applies to borderline records (for example, a quantity of zero)? | The trainee proposes one and confirms it before Lab 1.4 |
| How deep should the written explanations be? | Avoids over- or under-investing in the write-up |
