# M1 Write-Up: Python Intermediate

## 1. Deliverable & Evidence

**Repository:** [ejandrea-strat/python-training](https://github.com/ejandrea-strat/python-training)

**Overview:** I built a small pipeline that reads a messy order file, checks each record, then writes the valid rows to a CSV and the invalid ones to a log with the line number and reason. After that I turned it into a package that runs from the container terminal and gets imported by the notebook.
**Deliverable:** `module1_python_intermediate.ipynb`, the `orders_pipeline/` package, and `requirements.txt`

*   **DoD-1.2.2:** Output showing two isolated environments reporting different versions of the same package, with the `requirements.txt` contents
    *   *Output/Evidence:*
        ```
        Image Version: 0.9.0
        Image requirements.txt ['jupyterlab==4.4.0', 'tabulate==0.9.0']
        Venv Version: 0.8.10
        ```
*   **DoD-1.4.1:** The valid and rejected counts compared with the total non-blank input lines, plus a preview of `rejects.log`
    *   *Output/Evidence:*
        ```
        Valid: 33, Rejected: 7
        33 valid + 7 rejected = 40, non-blank lines = 40: True

        line 5: quantity is not a whole number or is <= 0 | ORD-1005|Pen|abc|1.20
        line 10: quantity is not a whole number or is <= 0 | ORD-1010|Stapler|-2|8.00
        line 16: quantity is not a whole number or is <= 0 | ORD-1015|Marker|0|2.50
        line 21: ['ORD-1020', 'Folder', '5'] should be 4, got 3 | ORD-1020|Folder|5
        line 28: empty product | ORD-1027||4|3.00
        line 33: price is not a number | ORD-1032|Tape|2|free
        line 39: ['ORD-1038', 'Glue', '1', '2.00', 'extra'] should be 4, got 5 | ORD-1038|Glue|1|2.00|extra
        ```
*   **DoD-1.8.3:** A comparison showing the terminal run and the notebook run produce identical output files
    *   *Output/Evidence:*
        ```
        $ python -m orders_pipeline
        Valid: 33, Rejected: 7
        $ python check_pipeline.py
        All 3 checks passed: 33 valid + 7 rejected = 40 lines

        clean files same: True
        rejects files same: True
        same as Lab 1.4: True
        ```

## 2. How to build it (teach it to the next trainee)

**Guide scope:** from a raw text file to a package that runs from the container terminal and is imported by a thin notebook

1. **Set up Docker first.** Make the `Dockerfile`, `docker-compose.yml`, `requirements.txt` and `.env.example`, and mount `./work` and `./data`. Put your notebook inside `work/`, not at the top level of JupyterLab, because `/workspace` itself isn't mounted. I got `No module named 'config'` until I moved my notebook there. Also check `sys.version`, my notebook was running on my local Windows Python (3.14) at first instead of the container's 3.11.
2. **Do Labs 1.1 to 1.3 before the pipeline.** Comprehensions, adding a package through `requirements.txt` and rebuilding the image, and `safe_to_float` with specific exceptions. The pipeline uses all of these later, for example `safe_to_float` becomes the price check.
3. **Write the pipeline as one script first (Lab 1.4).** Read `orders_raw.txt` line by line with `with open(...)`, skip the blank lines, split on `|` and strip the spaces, then check the rules one by one. Valid rows go to `clean_orders.csv` and the rejects go to `rejects.log` with the line number and reason. Check the counts right away, mine was 33 valid + 7 rejected = 40 non-blank lines.
4. **Break it into functions (Lab 1.5).** `read_lines`, `parse_record`, `validate_record` and `write_outputs`. `validate_record` returns the reason instead of printing it, so the main code decides what to do with it.
5. **Turn it into classes (Lab 1.7).** `OrderRecord` holds one valid order, and the two readers (`TextOrderReader` and `CsvOrderReader`) both return `(line_number, fields)`. Since they return the same shape, `load_orders` and `OrderPipeline` work with either one without changing anything.
6. **Move it into a package (Lab 1.8).** Each module has one job and a one-line docstring. Shared code like `safe_to_float` goes in `validators.py`, since it doesn't import anything from the package, so the imports can't go in a circle. Run it with `python -m orders_pipeline` from `/workspace/work`, then import it in the notebook with `%autoreload 2`.
7. **Check that everything matches.** `check_pipeline.py` has 3 asserts for the counts, totals and reasons, and `filecmp` shows the terminal run, the notebook run and Lab 1.4 all give the same `clean_orders.csv`.

Tip: check your file and folder names with `ls` before debugging the code. My two longest errors in Lab 1.8 were just a misspelled folder (`orders_pipelline`) and an `__init.__.py` with an extra dot.

## 3. Decisions & Core Concepts

**Key Decisions**

*   **Where did the trainee draw the line between a function, a class, and a module, and why?:** A function is enough if there is no need for retaining data between calls, like `safe_to_float` or `validate_record`. A class with only a single action method is unnecessary and should be a function instead. I only used classes when the data and its actions belong together, like `OrderRecord` and `total()`, or when I needed different versions that work the same way, like the readers. A module groups the functions and classes that have the same job, for example all the checks are in `validators.py`.
*   **What reject policy was chosen for borderline records, and what is the tradeoff behind it?:** 
I reject a record if the quantity isn't a whole number or is 0 or below. I also reject records with the wrong number of fields, an empty order_id or product, or a price that isn't a number. The tradeoff is a quantity of 0 could be a real record (like a cancelled order), so I might lose some valid data. But the rejects aren't just thrown away, they all go to `rejects.log` with the line number and reason so they can still be checked later.
*   **Why does the pipeline use composition instead of inheriting from a reader?:** OrderPipeline uses composition because a pipeline has a reader and a writer; it isn't a type of reader. Because it only calls read() and write(), I could pass TextOrderReader or CsvOrderReader without changing the class, and it gave 33/7 and 22/3. If it inherited from a reader instead, I'd need a separate pipeline class for each reader, which means duplicated code.

**Concepts Applied**

**Exception handling:** An else block runs only when the try block didn't fail, while a finally block runs whether or not the try block failed. Catching specific exceptions like ValueError and TypeError is better than using a bare except because it allows the program to handle expected data errors without stopping the entire process, while still allowing unexpected errors caused by programming bugs to surface instead of being silently ignored. In my Lab 1.3 loop, 8 values were valid, 5 raised a ValueError and 2 raised a TypeError, and I counted each one separately.

**Packages and reproducible environments:** A virtual environment inside a container is useful when two pieces of code need different versions of the same package side by side (such as during code migration). Another scenario seen in the labs is when you want to quickly try a different version without rebuilding the image. For a single project with one set of dependencies, the image alone is enough since the container already provides isolation, and anyone who builds the same image will get the specific package versions pinned in requirements.txt. 

**Comprehensions:** A comprehension creates and fills a collection in one go, it doesn't have a concept of an empty container and an append logic that a loop needs. It also has a compact way of filtering and transforming in one expression, right side for filtering and left side for transforming. A loop is a better choice when the logic is more complex, has side effects like printing, or needs error handling. In B-1.1.3, my loop kept a running total with `.get(product_name, 0)`, but my comprehension couldn't do that because it can't update a value it already wrote, so I used sum() over the matching rows for each product instead.

## 4. AI Collaboration Log

*   **Tools & Scope:** I used Claude for most of the module. I used it for tutoring and explanations in every lab, a study plan with lessons for each lab, reviewing my code and explaining my errors, and fixing the grammar in my explanations while keeping my own words. Claude also wrote some areas of the code: the first version of the Lab 1.8 package modules and `check_pipeline.py` (based on my Lab 1.3 to 1.7 code), and the diagrams. I wrote the code for Labs 1.1 to 1.7 myself with Claude reviewing it. In Lab 1.8, I set up the package in my repo, adjusted it, made and fixed the circular import, debugged the import errors, and wrote the notebook sections, with Claude reviewing my fixes.
*   **Prompt Examples:** 

    1. **Creating lessons from the brief**
        ```
        Context: I'm starting Module 1 (Python Intermediate) of a Python for Data Engineering training.
        Attached are the module brief and tasks.md.
        Task: Create a lesson for each scope item (1.1 to 1.8) based on the brief, covering the key
        concepts and the research question listed for it, so I can study before doing each lab.
        Constraints: Follow the brief's scope and labs. Use small examples that aren't the lab answers,
        and link the official Python docs as sources.
        Output: One lesson per lab, with a "Check yourself" section and a plan for doing the lab.
        ```
        Result: I studied each lesson before its lab, then did the lab myself. I used the lessons alongside the Python docs, not as the lab answers.

    2. **Converting each value only once in a comprehension**
        ```
        Context: Lab 1.1 step 1. I have 20 order amounts as strings like " 12.50 " and need one
        comprehension that strips, converts to float, and drops values at or below zero.
        Problem: My version calls float() twice, once in the filter and once in the result.
        Task: Show me how to convert each value only once while keeping it a single comprehension.
        Constraints: No helper function. Explain why it works, not just the code.
        ```
        Result: It suggested a generator expression inside the list comprehension, so each amount is converted once and then filtered. I wrote it myself and later removed an extra `list()` I had added (see Course Correction).
        
    3. **Debugging a package import**
        ```
        Context: My orders_pipeline package runs fine from the container terminal with
        python -m orders_pipeline.
        Problem: In the notebook, from orders_pipeline import TextOrderReader fails with
        ImportError: cannot import name 'TextOrderReader' from 'orders_pipeline' (unknown location).
        Task: Explain what "unknown location" means and give me the possible causes, most likely first.
        Output: The causes, and one command to check each.
        ```
        Result: "Unknown location" means Python found the folder but no `__init__.py`. Running `ls -la orders_pipeline` showed my file was named `__init.__.py`.
*   **Course Correction:**
    - In Lab 1.1, I wrapped the generator in `list()`, which built the whole list again and defeated the point of the generator. I removed it after learning that the `for` already calls `next()` on the generator, and checked that 17 of 20 values were still kept.
    - For the data path, Claude suggested using `os.environ` in `config.py`. I didn't use it since the path is already fixed by the compose mount, so I just used `Path("/workspace/data")`.
    - In Lab 1.8, the notebook comparison first showed `False`. When I checked `OrderPipeline.__module__`, the notebook was still using my Lab 1.7 classes because the import failed. The actual causes were a `%cd` with no path that moved the notebook to `/root`, and my `__init.__.py` typo.
*   **Human Intervention:** I wrote the code for Labs 1.1 to 1.7, all the written explanations, and the reject policy myself. For Lab 1.8, Claude gave me the first version of the package, and I set it up in my repo, adjusted it, and checked it against my own Lab 1.4 output (the same `clean_orders.csv`, 33/7, and all 3 checks passing). I broke and fixed the circular import myself, found and fixed the misspelled folder, the `__init.__.py` typo and the `%cd` that moved the notebook to `/root`, and wrote the Lab 1.8 notebook sections and reflection, with Claude reviewing them.

## 5. Retrospective & Self-Assessment

*   **Friction Log (What tripped the trainee up):**
    - **Lab 1.1 took me around 4 hours,** way more than the 1.5 hours planned. The dictionary comprehension took a lot of tries: first `TypeError: 'int' object is not iterable`, then `TypeError: unsupported operand type(s) for +: 'int' and 'str'`, then every product getting 230, until I filtered the inner sum() by product.
    - **Setup:** `docker compose build` failed with `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine` because Docker Desktop wasn't running. Then I got `ModuleNotFoundError: No module named 'config'` because my notebook was in `/workspace` instead of `work/`.
    - **Lab 1.8:** most of my time went to imports. First `No module named orders_pipeline` because I misspelled the folder as `orders_pipelline`. Then the notebook couldn't find the package because a `%cd` with no path sent it to `/root`. Then `ImportError: cannot import name 'TextOrderReader' from 'orders_pipeline' (unknown location)` because the file was named `__init.__.py`. The circular import (`cannot import name 'safe_to_float' from partially initialized module 'orders_pipeline.pipeline'`) was on purpose.
    - **Lab 1.7:** my pipeline test cell got switched to Markdown so Run All skipped it, and it was also overwriting Lab 1.4's `clean_orders.csv`. I changed it back to Code and added `_1-7` to its file names.
*   **What I'd do differently:** I'd check my file and folder names with `ls` first before debugging, and give each lab's output files their own names from the start so they don't overwrite each other.
*   **DoD Self-Assessment:**
    - DoD-1.2.2: Met. The image shows tabulate 0.9.0, the venv shows 0.8.10, and requirements.txt is printed.
    - DoD-1.4.1: Met. 33 valid + 7 rejected = 40 non-blank lines, with a preview of rejects.log.
    - DoD-1.8.1: Met. No function or class is defined twice in the package.
    - DoD-1.8.2: Partly Met. The Lab 1.8 section only imports from the package, but the Lab 1.3 to 1.7 sections still have the code that the package was built from.
    - DoD-1.8.3: Met. The terminal and notebook runs give the same files, and both match Lab 1.4.
    - Rubric: around 80%. I think completeness and correctness are good, but my understanding of the parts Claude wrote is weaker, and I went over the time estimate.
*   **Blind Spots:** I'd have a hard time explaining the module search path and why `python -m` worked without `__init__.py` but the notebook import didn't. I'd also need to re-read the whole of Lab 1.8 before explaining it line by line.