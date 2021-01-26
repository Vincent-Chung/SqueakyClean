# Functions to help with preparing dataset for ML

import pandas as pd
from sklearn.preprocessing import LabelEncoder

def OneHotEncode(df, Col):
    temp_df = pd.get_dummies(df[Col],drop_first = True)
    df = df.merge(temp_df, left_index = True, right_index = True)
    df = df.drop([Col], axis = 1)
    return df
