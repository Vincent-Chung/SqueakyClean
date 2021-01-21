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
# General
#
def ColKeepie(df, ColList):
    '''
    Input Types:
        df = Pandas DataFrame
        ColList = list type ['a','b','c','d']
    Returns:
        Pandas dataframe containing only columns of dataframe as defined with ColList arg
    '''
    return df[ColList]

def ColDroppie(df,ColList):
    '''
    Input Types:
        df = Pandas DataFrame
        ColList = list type ['a','b','c','d']
    Returns:
        Pandas dataframe removing all columns of dataframe as defined with ColList arg
    '''
    return df.drop([ColList], axis = 1)

def DataTypeSwitcheroo(df, Col, Type):
    '''
    Input Types:
        df = Pandas DataFrame
        Col = column name, as string
        Type = 
               If datetype desired, must enter "datetime" as string
               Else takes built-in python types: int, float, str
    Returns:
        Pandas dataframe with type converted as defined with Col and Type args
    '''
    if Type == "datetime":
        df[Col] = pd.to_datetime(df[Col])
    else:
        df[Col] = df[Col].astype(Type)
    return df
