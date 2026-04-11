# SqueakyClean 🧹

**SqueakyClean** is an opinionated Python library designed to simplify the "grunt work" of data preparation. By providing high-level abstractions for `pandas`, it helps data engineers and analysts transform messy, inconsistent datasets into "Squeaky Clean" dataframes ready for analysis or production.

> [!IMPORTANT]
> **Project Status: Early Development & Refactoring**
> This package is technically installable and functional, but it is currently undergoing a significant architectural overhaul. I am in the process of stabilizing the API and maturing the test suite. Expect frequent updates as the library moves toward a stable 1.0.0 release.

---

## Why SqueakyClean?

### The Historical Impetus: From Verbosity to Legibility
SqueakyClean was born from a recurring frustration in the data ecosystem: **"The Wall of Pandas."** Traditional data cleaning often results in brittle scripts filled with repetitive `df.assign()`, `df.drop()`, and nested regex calls. While functional, these scripts are difficult to audit and a nightmare to maintain. The original goal of this project was to **abstract the mechanical "how" into a semantic "what,"** turning 50 lines of verbose manipulation into 5 lines of **intent-driven logic.**

### The Evolution: Trust in the Age of "Vibe Coding"
In an era where code can be generated in seconds via LLMs (the "Vibe Coding" shift), the bottleneck has moved from *writing* code to **validating and trusting** it. 

SqueakyClean provides the **Semantic Guardrails** necessary for modern development:
* **Reliability:** Instead of relying on a dozen different AI-generated snippets for the same task, SqueakyClean provides a standardized, tested "contract" for your data.
* **Intent-Driven Design:** By using a consistent vocabulary of cleaning "verbs" (`ColKeepie`, `DataTypeSwitcheroo`), your pipelines remain readable to humans and auditable by AI, preventing the accumulation of prompt-engineered technical debt.
* **Human-Centric Engineering:** We focus on reducing syntax friction so architects can focus on the high-level data lifecycle and the human impact of the resulting analytics.

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
