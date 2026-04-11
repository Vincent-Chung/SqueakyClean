'''
Text processing functions to supplement pandas.
Intention is to cleanly abstract procedures for string manipulation and text cleaning.

Example:

df_new = (df_original
          .pipe(SubstringLeft, Col='full_name', SplitChar=' ')
          .pipe(FindReplace, Col='description', OldString='old_text', NewString='new_text')
          .pipe(LeftPadZero, Col='id', Len=5)
          .pipe(SmooshColNames)
          )
'''


import pandas as pd


def _ensure_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df must be a pandas DataFrame')


def _ensure_columns_exist(df, columns):
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise KeyError(f"Columns not found in DataFrame: {missing}")


def SubstringLeft(df, Col, SplitChar):
    '''
    Extracts the left portion of a string column up to a specified delimiter.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name containing the text to split.
        SplitChar (str): The delimiter character to split on.

    Returns:
        pd.DataFrame: The DataFrame with the specified column modified to contain only the left portion.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    new = df[Col].str.split(SplitChar, n=1, expand=True)
    df[Col] = new[0]
    df[Col] = df[Col].str.strip()  # Remove white spaces
    return df

def SubstringRight(df, Col, SplitChar):
    '''
    Extracts the right portion of a string column after a specified delimiter.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name containing the text to split.
        SplitChar (str): The delimiter character to split on.

    Returns:
        pd.DataFrame: The DataFrame with the specified column modified to contain only the right portion.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    new = df[Col].str.split(SplitChar, n=1, expand=True)
    df[Col] = new[1]
    df[Col] = df[Col].str.strip()  # Remove white spaces
    return df

def SubStringMiddle(df, Col, Start, End):
    '''
    Extracts a substring from a text column using 1-based start and end positions.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name containing the text.
        Start (int): The 1-based starting position (inclusive).
        End (int): The 1-based ending position (exclusive).

    Returns:
        pd.DataFrame: The DataFrame with the specified column modified to contain the substring.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    df[Col] = df[Col].str[Start - 1: End]
    return df

def FindReplace(df, Col, OldString, NewString):
    '''
    Performs find-and-replace operations on a text column.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name containing the text to modify.
        OldString (str): The substring to find and replace.
        NewString (str): The replacement string.

    Returns:
        pd.DataFrame: The DataFrame with the specified replacements made.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    df[Col] = df[Col].str.replace(OldString, NewString)
    return df

def LeftPadZero(df, Col, Len):
    '''
    Left-pads a column with zeros to achieve a specified total length.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name to pad.
        Len (int): The desired total length after padding.

    Returns:
        pd.DataFrame: The DataFrame with the specified column zero-padded.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    df[Col] = df[Col].astype(str)
    df[Col] = df[Col].str.zfill(Len)
    return df

def SmooshColNames(df):
    '''
    Removes all spaces from column names.

    Args:
        df (pd.DataFrame): The source DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with spaces removed from all column names.
    '''
    _ensure_dataframe(df)

    df.columns = df.columns.str.replace(' ', '')
    return df
