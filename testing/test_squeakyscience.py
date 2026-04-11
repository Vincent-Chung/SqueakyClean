import pandas as pd
import pytest

from squeakyscience import (
    calc_min_max_norm,
    calc_quantile,
    easy_drop,
    one_hot_encode,
    tfidf_clusters,
)


def test_onehotencode_creates_indicator_columns():
    df = pd.DataFrame({'color': ['red', 'blue', 'blue'], 'value': [1, 2, 3]})
    result = one_hot_encode(df, 'color')

    assert 'color_blue' in result.columns
    assert 'color' not in result.columns
    assert list(result['value']) == [1, 2, 3]


def test_tfidf_clusters_raises_key_error_for_missing_column():
    df = pd.DataFrame({'text': ['apple', 'banana']})

    with pytest.raises(KeyError, match='Columns not found'):
        tfidf_clusters(df, 'missing', 'cluster', K=2, KeepPct=0.5)


def test_calcminmaxnorm_handles_constant_column():
    df = pd.DataFrame({'x': [5, 5, 5]})
    result = calc_min_max_norm(df, 'x', 'x_norm')

    assert list(result['x_norm']) == [0.0, 0.0, 0.0]


def test_calcquantile_raises_value_error_for_too_many_groups():
    df = pd.DataFrame({'x': [1, 1, 1, 1]})

    with pytest.raises(ValueError, match='Groups must be smaller'):
        calc_quantile(df, 'x', 'bucket', Groups=3)


def test_easydrop_drops_high_missing_and_constant_columns():
    df = pd.DataFrame({
        'target': [0, 1, 0],
        'full_missing': [None, None, None],
        'constant': [1, 1, 1],
        'good': [1, 2, 3],
        'high_card': ['a', 'b', 'c'],
    })
    result = easy_drop(df, 'target')

    assert 'full_missing' not in result.columns
    assert 'constant' not in result.columns
    assert 'good' in result.columns
    assert 'target' in result.columns
