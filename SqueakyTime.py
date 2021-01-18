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

#################
#
# Time
#
def FilterBetweenDates(df, ColSelectionDate, ColStartDate, ColEndDate):
    # This function doesn't work with int
    df[ColSelectionDate] = df[ColSelectionDate].astype(float)  
    df[ColStartDate] = df[ColStartDate].astype(float)
    df[ColEndDate] = df[ColEndDate].astype(float)   
    df = df[df[ColSelectionDate].between(df[ColStartDate], df[ColEndDate])]   
    return df
