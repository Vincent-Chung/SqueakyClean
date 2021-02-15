'''
Data  wrangling functions to supplement pandas
Intention is to cleanly abstract procedures for piping within method chains

Example:

df_new = (df_original
          .pipe(ColKeepie, ColList = ['vendorMasterCode','ElectronicsFlag','TransactionDate'])
          .rename(columns={"vendorMasterCode" : "vendorCode"})
          .query('ElectronicsFlag == 1')
          .pipe(ColDroppie, ColList = ['ElectronicsFlag','TransactionDatet'])
          )
'''

# External dependencies
import pandas as pd


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
    df = df.drop(ColList, axis = 1)
    return df

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
        df[Col] = df[Col].astype(str)
        df[Col] = pd.to_datetime(df[Col])
    else:
        df[Col] = df[Col].astype(Type)
    return df

def DeleteRowsContains(df, Col, Contains):
    df['ContainsFlag'] = df[Col].str.contains(Contains)
    df = df[df.ContainsFlag != True]
    df = df.drop(['ContainsFlag'], axis = 1)
    return df

def KeepRowsContains(df, Col, Contains):
    df['ContainsFlag'] = df[Col].str.contains(Contains)
    df = df[df.ContainsFlag == True]
    df = df.drop(['ContainsFlag'], axis = 1)
    return df
