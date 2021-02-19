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
import datetime

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

def CalcDaysSinceX(df, Col, NewCol):
    '''
    Parameters:
        df = pandas dataframe
        Col = column of dates to use for date delta calc, enter as string  
        NewCol = name of new column, enter as string
        
    Returns:
        df = pandas dataframe with new column (NewCol) containing date delta
    '''
    df[Col] = pd.to_datetime(df[Col])
    df[NewCol] = datetime.datetime.now() - df[Col]
    df[NewCol] = df[NewCol].dt.days
    return df

def DateExtract(df, ExtractType, Col, ColName):
    '''
    Input Types:
        df = Pandas DataFrame
        ExtractType = Input as string, this parameter defines element of date for extraction. Parameter must be "month" or "day" or "day_of_week"
        Col = Date column targeted for element extraction
        ColName = New column that contains extracted date element
        
    Returns:
        Pandas dataframe containing new column with extracted element of targeted date column
    '''        
    if SplitType == 'month':
        df[ColName] = pd.to_datetime(df[Col], format='%Y%m%d')
        df[ColName] = df[ColName].dt.month                
    elif SplitType == 'day':
        df[ColName] = pd.to_datetime(df[Col], format='%Y%m%d')
        df[ColName] = df[ColName].dt.day          
    elif SplitType == 'day_of_week':
        # Monday = 0; Sunday = 6
        df[ColName] = pd.to_datetime(df[Col], format='%Y%m%d')
        df[ColName] = df[ColName].dt.dayofweek 
    else:
        print('ERROR in SplitType. Value must be "month" or "day" or "day_of_week"')      
    return df
