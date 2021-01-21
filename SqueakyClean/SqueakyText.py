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
# Text
#
def SubstringLeft(df, Col, SplitChar):
    '''
    Input Types:
        df = Pandas Dataframe
        Col = column name, as string
        SplitChar = character used as boundary for trimming text, as string
    Returns: 
        Pandas dataframe with text column limited to left of defined boundary, as defined with Col and SplitChar args

    '''
    new = df[Col].str.split(SplitChar, n = 1, expand = True) 
    df[Col] = new[0]
    df[Col] = df[Col].str.strip() # Remove White Spaces
    return df

def SubstringRight(df, Col, SplitChar):
    '''
    Input Types:
        df = Pandas Dataframe
        Col = column name, as string
        SplitChar = character used as boundary for trimming text, as string
    Returns: 
        Pandas dataframe with text column limited to right of defined boundary, as defined with Col and SplitChar args
    '''
    new = df[Col].str.split(SplitChar, n = 1, expand = True) 
    df[Col] = new[1]
    df[Col] = df[Col].str.strip() # Remove White Spaces
    return df

def FindReplace(df, Col, OldString, NewString):
    '''
    Input Types:
        df = Pandas DataFrame
        Col = Column Name, as string
        OldString = String to target, as string
        NewString = Replacement string, as string
    Returns:
        Pandas dataframe with text replaced, as defined with Col, OldString, and NewString
    '''
    df[Col] = df[Col].str.replace(OldString, NewString)
    return df

def LeftPadZero(df, Col, Len):
    '''
    Input Types:
        df = Pandas DataFrame
        Col = Column Name, as string
        Len = amount of zeros desired for padding
    Returns:
        Pandas dataframe with targeted column padded with zeros, as defined with Col and Len
    '''
    df[Col] = df[Col].astype(str)
    df[Col] = df[Col].str.zfill(Len)
    return df
