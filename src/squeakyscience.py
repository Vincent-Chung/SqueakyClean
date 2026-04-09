# Functions to help with preparing dataset for analytics, data science, machine learning

#-------------------------------------------

# Packages
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Functions
def OneHotEncode(df, Col):
    temp_df = pd.get_dummies(df[Col],drop_first = True)
    df = df.merge(temp_df, left_index = True, right_index = True)
    df = df.drop([Col], axis = 1)
    return df

def TFIDF_Clusters(df, Col, ColName, K, KeepPct):
    # Converts free text field to a similarity cluster
    # Uses TFIDF and k means
    # This is under construction. Use at your own risk.
    df2 = df.copy()
    df_TFIDFmatrix = df.copy()
    Keep = len(df_TFIDFmatrix) * KeepPct
    
    tfidf = TfidfVectorizer(analyzer='word', stop_words = 'english')
    score = tfidf.fit_transform(df_TFIDFmatrix[Col])
    df_TFIDFmatrix = (pd.DataFrame(score.toarray(), 
                                   columns=tfidf.get_feature_names())    
                        .replace(0, np.nan)
                        .dropna(thresh=Keep, axis = 1)
                        .fillna(0)
                      )
    
    model_KMeans = KMeans(n_clusters = K, random_state = 11).fit(df_TFIDFmatrix)
    df2[ColName] = model_KMeans.labels_
    
    df2 = df2.drop([Col], axis = 1)
    return df2

def CalcQuantile(df, Col, NewCol, Groups):
    '''
    Input Types:
        df = Pandas DataFrame
        Col = Entered as string, defines which column to use for calculating quantiles. Only works on numeric fields!
        NewCol = Entered as string, name of new column that contains quantiles
        Groups = Entered as int, controls amount of equal-sized groups
    Returns:
        Pandas dataframe containing user defined column (Col) converted to discrete equal-sized buckets
    '''
    df[NewCol] = pd.qcut(df[Col].values, Groups).codes + 1
    return df

def CalcMinMaxNorm(df, Col, NewCol):
    '''
    Input Types:
        df = Pandas DataFrame
        Col = Entered as string, defines which column to use for calculating min-max normalization. Only works on numeric fields!
        NewCol = Entered as string, name of new column that contains normalized values
    Returns:
        Pandas dataframe containing user defined column (Col) converted to normalized data
        This uses the min-max normalization method: https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
    '''
    df[NewCol] = (df[Col] - min(df[Col])) / (max(df[Col]) - min(df[Col]))
    return df

def EasyDrop(df, target):
    '''
    Input Types:
    df = Pandas dataFrame
    target = Dependent Variable

    Returns:
    Pandas dataFrame without:
        Variables > 90% missing
        Variables with constants
        Variables with High cardinality (100+ uniqueness)
    '''
    # Split data: target and features
    Target = df[target]
    Features = df.drop(columns = [target])
    
    # Remove Features > 90% missing
    TheList = pd.DataFrame(Features.isna().mean())
    TheList.columns = ['MissingPct']
    TheList = TheList.query('MissingPct > 0.9').index.tolist()
    Features = (Features.drop(columns = TheList))
    
    # Split features into categorical and numeric
    FeatsCat = Features.select_dtypes(include = 'object')
    FeatsNums = Features.select_dtypes(include = np.number)
    
    # Remove Constants
    FeatsCat = FeatsCat.loc[:,df.apply(pd.Series.nunique) != 1]
    FeatsNums = FeatsNums.loc[:,FeatsNums.apply(pd.Series.nunique) != 1]
    
    # Remove categorical fields with over 100 unique variables
    FeatsCat = FeatsCat.loc[:,FeatsCat.apply(pd.Series.nunique) < 100]
    
    # Unite [Target] and [Features] dataframes
    TheOutput = pd.concat([FeatsCat, FeatsNums, Target], axis = 1)
    return TheOutput
