import pandas as pd
import pytest

from squeakyessentials import (
    ColDroppie,
    ColKeepie,
    DataTypeSwitcheroo,
    DeleteRowsContains,
    KeepRowsContains,
)


def test_colkeepie_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': [1], 'b': [2]})

    with pytest.raises(KeyError, match='Columns not found'):
        ColKeepie(df, ['missing'])


def test_coldroppie_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': [1], 'b': [2]})

    with pytest.raises(KeyError, match='Columns not found'):
        ColDroppie(df, ['missing'])


def test_datatypeswitcheroo_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': [1]})

    with pytest.raises(KeyError, match='Columns not found'):
        DataTypeSwitcheroo(df, 'missing', int)


def test_datatypeswitcheroo_raises_type_error_for_invalid_type():
    df = pd.DataFrame({'a': [1]})

    with pytest.raises(TypeError, match='Type must be'):
        DataTypeSwitcheroo(df, 'a', 'notatype')


def test_deleterowscontains_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['foo', 'bar']})

    with pytest.raises(KeyError, match='Columns not found'):
        DeleteRowsContains(df, 'missing', 'foo')


def test_keeprowscontains_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['foo', 'bar']})

    with pytest.raises(KeyError, match='Columns not found'):
        KeepRowsContains(df, 'missing', 'foo')


def test_colkeepie_keeps_only_requested_columns():
    df = pd.DataFrame({'a': [1], 'b': [2], 'c': [3]})
    result = ColKeepie(df, ['a', 'c'])

    assert list(result.columns) == ['a', 'c']
    assert result.equals(pd.DataFrame({'a': [1], 'c': [3]}))


def test_coldroppie_drops_requested_columns():
    df = pd.DataFrame({'a': [1], 'b': [2], 'c': [3]})
    result = ColDroppie(df, ['b'])

    assert list(result.columns) == ['a', 'c']
    assert result.equals(pd.DataFrame({'a': [1], 'c': [3]}))


def test_datatypeswitcheroo_converts_to_datetime():
    df = pd.DataFrame({'a': ['2025-01-01', '2025-02-02']})
    result = DataTypeSwitcheroo(df, 'a', 'datetime')

    assert pd.api.types.is_datetime64_any_dtype(result['a'])


def test_deleterowscontains_removes_matching_rows():
    df = pd.DataFrame({'a': ['foo', 'bar', 'foobar']})
    result = DeleteRowsContains(df, 'a', 'foo')

    assert list(result['a']) == ['bar']


def test_keeprowscontains_keeps_matching_rows():
    df = pd.DataFrame({'a': ['foo', 'bar', 'foobar']})
    result = KeepRowsContains(df, 'a', 'foo')

    assert list(result['a']) == ['foo', 'foobar']
