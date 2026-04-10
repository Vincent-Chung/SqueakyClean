# SqueakyClean 🧹

**SqueakyClean** is an opinionated Python library designed to simplify the "grunt work" of data preparation. By providing high-level abstractions for `pandas`, it helps data engineers and analysts transform messy, inconsistent datasets into "Squeaky Clean" dataframes ready for analysis or production.

> [!IMPORTANT]
> **Project Status: Early Development & Refactoring**
> This package is technically installable and functional, but it is currently undergoing a significant architectural overhaul. I am in the process of stabilizing the API and maturing the test suite. Expect frequent updates as the library moves toward a stable 1.0.0 release.

---

## Why SqueakyClean?

Data cleaning is often 80% of the work. This library aims to reduce that friction by automating common tasks with a focus on readability and maintainable code:

* **Schema Normalization:** Automatically sanitize column names (snake_case, removing special characters, etc.).
* **Pandas Abstractions:** Perform complex data transformations without writing repetitive boilerplate.
* **Built for Reliability:** Designed to help analysts move from "ad-hoc scripts" to "production-ready pipelines."

## Installation

You can install the current development version directly from the repository:

```bash
pip install git+[https://github.com/Vincent-Chung/SqueakyClean.git](https://github.com/Vincent-Chung/SqueakyClean.git)
```

## Quick Start

Getting started with **SqueakyClean** is designed to be intuitive. Here is how to run a basic cleaning pipeline on a messy DataFrame:

```python
import pandas as pd
import squeakyclean as sc

# 1. Setup some messy sample data
data = {
    "User ID": [1, 2, 3],
    "Account_Balance": ["$1,200", "$3,500", "ERROR"],
    "Internal_Notes": ["Active", "Active", "Delete Me"],
    "Irrelevant_Col": [None, None, None]
}
df = pd.DataFrame(data)

# 2. Method Chaining with SqueakyClean
# This allows you to read the logic like a sentence.
clean_df = (
    df
    .pipe(sc.ColDroppie, columns=["Irrelevant_Col"])
    .pipe(sc.DeleteRowsContains, column="Internal_Notes", value="Delete Me")
    .pipe(sc.DataTypeSwitcheroo, column="Account_Balance", to_type="float")
)

print(clean_df)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
