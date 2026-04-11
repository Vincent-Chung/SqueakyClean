'''
Data  wrangling functions to supplement pandas
Intention is to cleanly abstract procedures for piping within method chains

Example:

df_new = (df_original
          .pipe(ColKeepie, ColList = ['vendorMasterCode','ElectronicsFlag','TransactionDate'])
          .rename(columns={"vendorMasterCode" : "vendorCode"})
          .query('ElectronicsFlag == 1')
          .pipe(ColDroppie, ColList = ['ElectronicsFlag'])
          )
'''

# External dependencies
import pandas as pd


def _ensure_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df must be a pandas DataFrame')


def _ensure_columns_exist(df, columns):
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise KeyError(f"Columns not found in DataFrame: {missing}")


def ColKeepie(df, ColList):
    '''
    Filters the DataFrame to keep only the specified columns.

    Args:
        df (pd.DataFrame): The source DataFrame.
        ColList (list): A list of column names to retain.

    Returns:
        pd.DataFrame: A DataFrame containing only the selected columns.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, ColList)
    return df[ColList]

def ColDroppie(df, ColList):
    '''
    Filters the DataFrame to remove the specified columns.

    Args:
        df (pd.DataFrame): The source DataFrame.
        ColList (list): A list of column names to remove.

    Returns:
        pd.DataFrame: A DataFrame with the specified columns removed.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, ColList)
    return df.drop(ColList, axis=1)

def DataTypeSwitcheroo(df, Col, Type):
    '''
    Converts a column in the DataFrame to a specified data type.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name to convert.
        Type (str or type): The target data type. Use "datetime" for datetime conversion,
            or built-in Python types (int, float, str).

    Returns:
        pd.DataFrame: The DataFrame with the specified column converted to the new type.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    if Type == 'datetime':
        df[Col] = df[Col].astype(str)
        df[Col] = pd.to_datetime(df[Col])
    elif Type in {int, float, str} or isinstance(Type, type):
        df[Col] = df[Col].astype(Type)
    else:
        raise TypeError(
            'Type must be "datetime" or a valid Python type like int, float, or str'
        )

    return df

def DeleteRowsContains(df, Col, Contains):
    '''
    Removes rows from the DataFrame where a column contains the specified substring.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name to search.
        Contains (str): The substring to search for.

    Returns:
        pd.DataFrame: The DataFrame with rows containing the substring removed.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    mask = df[Col].astype(str).str.contains(Contains, na=False)
    return df.loc[~mask].copy()

def KeepRowsContains(df, Col, Contains):
    '''
    Keeps only rows from the DataFrame where a column contains the specified substring.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name to search.
        Contains (str): The substring to search for.

    Returns:
        pd.DataFrame: The DataFrame with only rows containing the substring retained.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    mask = df[Col].astype(str).str.contains(Contains, na=False)
    return df.loc[mask].copy()
