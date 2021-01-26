'''
Data  wrangling functions to supplement pandas
Intention is to cleanly abstract procedures for piping within method chains

Example:
df_new = (df_original
          .pipe(ColKeepie, ColList = ['vendorMasterCode','ElectronicsFlag','TransactionDate'])
          .rename(columns={"vendorMasterCode" : "vendorCode"})
          .query('ElectronicsFlag == 1')
          .pipe(Last90Days, DateColumn = 'TransactionDate')
          )
'''
import pandas as pd

def FilterBetweenDates(df, ColSelectionDate, ColStartDate, ColEndDate):
    # This function doesn't work with int
    df[ColSelectionDate] = df[ColSelectionDate].astype(float)  
    df[ColStartDate] = df[ColStartDate].astype(float)
    df[ColEndDate] = df[ColEndDate].astype(float)   
    df = df[df[ColSelectionDate].between(df[ColStartDate], df[ColEndDate])]   
    return df

def CalcDuration(df, NewColName, ColStartDate, ColEndDate):
    df[ColStartDate] = pd.to_datetime(df[ColStartDate], format='%Y%m%d')
    df[ColEndDate] = pd.to_datetime(df[ColEndDate], format='%Y%m%d')
    df[NewColName] = df[ColEndDate] - df[ColStartDate]
    df[NewColName] = df[NewColName].dt.days
    return df
