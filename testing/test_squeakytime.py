import pandas as pd
import pytest

from squeakyclean.squeakytime import (
    CalcDaysSinceX,
    CalcDuration,
    DateExtract,
    FilterBetweenDates,
)


def test_filterbetweendates_raises_key_error_for_missing_column():
    df = pd.DataFrame({'date': [1.0], 'start': [1.0]})

    with pytest.raises(KeyError, match='Columns not found'):
        FilterBetweenDates(df, 'date', 'start', 'missing')


def test_calcduration_raises_key_error_for_missing_column():
    df = pd.DataFrame({'start': ['20230101']})

    with pytest.raises(KeyError, match='Columns not found'):
        CalcDuration(df, 'duration', 'start', 'missing')


def test_calcdaysincex_raises_key_error_for_missing_column():
    df = pd.DataFrame({'other': ['2023-01-01']})

    with pytest.raises(KeyError, match='Columns not found'):
        CalcDaysSinceX(df, 'missing', 'days_since')


def test_dateextract_raises_key_error_for_missing_column():
    df = pd.DataFrame({'other': ['20230101']})

    with pytest.raises(KeyError, match='Columns not found'):
        DateExtract(df, 'month', 'missing', 'month_col')


def test_filterbetweendates_filters_correctly():
    df = pd.DataFrame({
        'date': [1.5, 2.5, 3.5],
        'start': [1.0, 1.0, 1.0],
        'end': [2.0, 3.0, 4.0]
    })
    result = FilterBetweenDates(df, 'date', 'start', 'end')

    assert len(result) == 3  # All dates fall within their respective ranges
    assert list(result['date']) == [1.5, 2.5, 3.5]


def test_calcduration_calculates_correctly():
    df = pd.DataFrame({
        'start': ['20230101', '20230105'],
        'end': ['20230103', '20230110']
    })
    result = CalcDuration(df, 'duration', 'start', 'end')

    assert list(result['duration']) == [2, 5]


def test_calcdaysincex_calculates_days():
    df = pd.DataFrame({'date': ['2023-01-01']})
    result = CalcDaysSinceX(df, 'date', 'days_since')

    # Should have a days_since column with positive integer
    assert 'days_since' in result.columns
    assert result['days_since'].iloc[0] > 0
    # Check for integer-like type (including numpy integers)
    import numpy as np
    assert isinstance(result['days_since'].iloc[0], (int, np.integer))


def test_dateextract_month():
    df = pd.DataFrame({'date': ['20230115', '20230620']})
    result = DateExtract(df, 'month', 'date', 'month_col')

    assert list(result['month_col']) == [1, 6]


def test_dateextract_day():
    df = pd.DataFrame({'date': ['20230115', '20230620']})
    result = DateExtract(df, 'day', 'date', 'day_col')

    assert list(result['day_col']) == [15, 20]


def test_dateextract_day_of_week():
    df = pd.DataFrame({'date': ['20230102', '20230103']})  # Monday, Tuesday
    result = DateExtract(df, 'day_of_week', 'date', 'dow_col')

    assert list(result['dow_col']) == [0, 1]  # Monday=0, Tuesday=1


def test_dateextract_invalid_extract_type():
    df = pd.DataFrame({'date': ['20230101']})

    with pytest.raises(ValueError, match='ExtractType must be'):
        DateExtract(df, 'invalid', 'date', 'col')