'''
Date and time processing functions to supplement pandas.
Intention is to cleanly abstract procedures for temporal data manipulation.

Example:

df_new = (df_original
          .pipe(CalcDaysSinceX, Col='purchase_date', NewCol='days_since_purchase')
          .pipe(DateExtract, ExtractType='month', Col='transaction_date', ColName='month')
          .pipe(FilterBetweenDates, ColSelectionDate='event_date',
                ColStartDate='start_range', ColEndDate='end_range')
          )
'''

import pandas as pd
import datetime

def FilterBetweenDates(df, ColSelectionDate, ColStartDate, ColEndDate):
    '''
    Filters rows to keep only those where a date column falls between start and end date ranges.

    Args:
        df (pd.DataFrame): The source DataFrame.
        ColSelectionDate (str): The column containing dates to filter.
        ColStartDate (str): The column containing start date boundaries.
        ColEndDate (str): The column containing end date boundaries.

    Returns:
        pd.DataFrame: The filtered DataFrame containing only rows where the selection date
            falls between the start and end date ranges.
    '''
    df[ColSelectionDate] = df[ColSelectionDate].astype(float)
    df[ColStartDate] = df[ColStartDate].astype(float)
    df[ColEndDate] = df[ColEndDate].astype(float)
    df = df[df[ColSelectionDate].between(df[ColStartDate], df[ColEndDate])]
    return df

def CalcDuration(df, NewColName, ColStartDate, ColEndDate):
    '''
    Calculates the duration in days between two date columns.

    Args:
        df (pd.DataFrame): The source DataFrame.
        NewColName (str): The name of the new column to contain duration values.
        ColStartDate (str): The column containing start dates.
        ColEndDate (str): The column containing end dates.

    Returns:
        pd.DataFrame: The DataFrame with a new column containing duration in days.
    '''
    df[ColStartDate] = pd.to_datetime(df[ColStartDate], format='%Y%m%d')
    df[ColEndDate] = pd.to_datetime(df[ColEndDate], format='%Y%m%d')
    df[NewColName] = df[ColEndDate] - df[ColStartDate]
    df[NewColName] = df[NewColName].dt.days
    return df

def CalcDaysSinceX(df, Col, NewCol):
    '''
    Calculates the number of days between a date column and today's date.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column containing dates to calculate days since.
        NewCol (str): The name of the new column to contain the day counts.

    Returns:
        pd.DataFrame: The DataFrame with a new column containing days since the specified dates.
    '''
    df[Col] = pd.to_datetime(df[Col])
    df[NewCol] = datetime.datetime.now() - df[Col]
    df[NewCol] = df[NewCol].dt.days
    return df

def DateExtract(df, ExtractType, Col, ColName):
    '''
    Extracts date components (month, day, or day of week) from a datetime column.

    Args:
        df (pd.DataFrame): The source DataFrame.
        ExtractType (str): The component to extract. Must be 'month', 'day', or 'day_of_week'.
        Col (str): The datetime column to extract from.
        ColName (str): The name of the new column to contain the extracted values.

    Returns:
        pd.DataFrame: The DataFrame with a new column containing the extracted date component.
    '''
    if ExtractType == 'month':
        df[ColName] = pd.to_datetime(df[Col], format='%Y%m%d')
        df[ColName] = df[ColName].dt.month
    elif ExtractType == 'day':
        df[ColName] = pd.to_datetime(df[Col], format='%Y%m%d')
        df[ColName] = df[ColName].dt.day
    elif ExtractType == 'day_of_week':
        # Monday = 0; Sunday = 6
        df[ColName] = pd.to_datetime(df[Col], format='%Y%m%d')
        df[ColName] = df[ColName].dt.dayofweek
    else:
        raise ValueError('ExtractType must be "month", "day", or "day_of_week"')
    return df
