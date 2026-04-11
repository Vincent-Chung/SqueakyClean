import pandas as pd
import pytest

from squeakyclean.squeakytext import (
    FindReplace,
    LeftPadZero,
    SmooshColNames,
    SubstringLeft,
    SubstringRight,
    SubStringMiddle,
)


def test_substringleft_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['hello world']})

    with pytest.raises(KeyError, match='Columns not found'):
        SubstringLeft(df, 'missing', ' ')


def test_substringright_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['hello world']})

    with pytest.raises(KeyError, match='Columns not found'):
        SubstringRight(df, 'missing', ' ')


def test_substringmiddle_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['hello']})

    with pytest.raises(KeyError, match='Columns not found'):
        SubStringMiddle(df, 'missing', 1, 3)


def test_findreplace_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['hello']})

    with pytest.raises(KeyError, match='Columns not found'):
        FindReplace(df, 'missing', 'old', 'new')


def test_leftpadzero_raises_key_error_for_missing_column():
    df = pd.DataFrame({'a': ['123']})

    with pytest.raises(KeyError, match='Columns not found'):
        LeftPadZero(df, 'missing', 5)


def test_substringleft_splits_correctly():
    df = pd.DataFrame({'name': ['John Doe', 'Jane Smith']})
    result = SubstringLeft(df, 'name', ' ')

    assert list(result['name']) == ['John', 'Jane']


def test_substringright_splits_correctly():
    df = pd.DataFrame({'name': ['John Doe', 'Jane Smith']})
    result = SubstringRight(df, 'name', ' ')

    assert list(result['name']) == ['Doe', 'Smith']


def test_substringmiddle_extracts_correctly():
    df = pd.DataFrame({'text': ['hello']})
    result = SubStringMiddle(df, 'text', 2, 4)

    assert list(result['text']) == ['ell']


def test_findreplace_works():
    df = pd.DataFrame({'text': ['hello world', 'goodbye world']})
    result = FindReplace(df, 'text', 'world', 'universe')

    assert list(result['text']) == ['hello universe', 'goodbye universe']


def test_leftpadzero_pads_correctly():
    df = pd.DataFrame({'id': ['123', '45']})
    result = LeftPadZero(df, 'id', 5)

    assert list(result['id']) == ['00123', '00045']


def test_smooshcolnames_removes_spaces():
    df = pd.DataFrame({'First Name': [1], 'Last Name': [2]})
    result = SmooshColNames(df)

    assert list(result.columns) == ['FirstName', 'LastName']