'''
SqueakyClean 🧹

An opinionated Python library designed to simplify the "grunt work" of data preparation.
By providing high-level abstractions for pandas, it helps data engineers and analysts
transform messy, inconsistent datasets into "Squeaky Clean" dataframes ready for analysis.

Example:

    import pandas as pd
    import squeakyclean as sc

    # Setup some messy sample data
    data = {
        "User ID": [1, 2, 3],
        "Account_Balance": ["$1,200", "$3,500", "ERROR"],
        "Internal_Notes": ["Active", "Active", "Delete Me"],
        "Irrelevant_Col": [None, None, None]
    }
    df = pd.DataFrame(data)

    # Method Chaining with SqueakyClean
    clean_df = (
        df
        .pipe(sc.ColDroppie, ColList=["Irrelevant_Col"])
        .pipe(sc.DeleteRowsContains, Col="Internal_Notes", Contains="Delete Me")
        .pipe(sc.DataTypeSwitcheroo, Col="Account_Balance", Type="float")
    )

    print(clean_df)
'''

from .squeakyessentials import (
    ColKeepie,
    ColDroppie,
    DataTypeSwitcheroo,
    DeleteRowsContains,
    KeepRowsContains,
)
from .squeakyscience import (
    one_hot_encode,
    tfidf_clusters,
    calc_quantile,
    calc_min_max_norm,
    easy_drop,
)
from .squeakytext import (
    SubstringLeft,
    SubstringRight,
    SubStringMiddle,
    FindReplace,
    LeftPadZero,
    SmooshColNames,
)
from .squeakytime import (
    FilterBetweenDates,
    CalcDuration,
    CalcDaysSinceX,
    DateExtract,
)

__all__ = [
    'ColKeepie',
    'ColDroppie',
    'DataTypeSwitcheroo',
    'DeleteRowsContains',
    'KeepRowsContains',
    'one_hot_encode',
    'tfidf_clusters',
    'calc_quantile',
    'calc_min_max_norm',
    'easy_drop',
    'SubstringLeft',
    'SubstringRight',
    'SubStringMiddle',
    'FindReplace',
    'LeftPadZero',
    'SmooshColNames',
    'FilterBetweenDates',
    'CalcDuration',
    'CalcDaysSinceX',
    'DateExtract',
]

