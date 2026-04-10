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

# 1. Load a dataset with messy headers and mixed types
df = pd.DataFrame({
    "  Full Name  ": ["Vincent", "Jane"],
    "Phone #!": ["123-456", "987-654"],
    "Birth_Date": ["1988-01-01", "1992-05-15"]
})

# 2. Apply the SqueakyClean transformation
# This will normalize headers to snake_case and handle basic type casting
clean_df = sc.clean_dataframe(df)

# 3. Enjoy your production-ready data
print(clean_df.columns)
# Output: Index(['full_name', 'phone', 'birth_date'], dtype='object')](https://github.com/Vincent-Chung/SqueakyClean/tree/master)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
