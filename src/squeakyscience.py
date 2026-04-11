# Functions to help with preparing dataset for analytics, data science, machine learning

#-------------------------------------------

# Packages
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def _ensure_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df must be a pandas DataFrame')


def _ensure_columns_exist(df, columns):
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise KeyError(f"Columns not found in DataFrame: {missing}")


def _ensure_numeric_column(df, col):
    if not pd.api.types.is_numeric_dtype(df[col]):
        raise TypeError(f'Column {col!r} must contain numeric data')


def _ensure_positive_int(value, name):
    if not isinstance(value, int) or value < 1:
        raise ValueError(f'{name} must be a positive integer')


def _ensure_keep_pct(value):
    if not isinstance(value, (int, float)):
        raise TypeError('KeepPct must be a number between 0 and 1')
    if not 0 < value <= 1:
        raise ValueError('KeepPct must be greater than 0 and less than or equal to 1')


def one_hot_encode(df, Col):
    '''
    Converts a single categorical column into one-hot encoded indicator columns.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The column name to encode.

    Returns:
        pd.DataFrame: A new DataFrame with the encoded columns added and the original column removed.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])

    return pd.get_dummies(df, columns=[Col], drop_first=True)


def tfidf_clusters(df, Col, ColName, K, KeepPct):
    '''
    Converts a text column into KMeans cluster labels using TF-IDF features.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The text column to analyze.
        ColName (str): The name of the cluster label column.
        K (int): The number of clusters.
        KeepPct (float): The fraction of rows a term must appear in to keep the feature.

    Returns:
        pd.DataFrame: A DataFrame containing the new cluster label column.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])
    _ensure_positive_int(K, 'K')
    _ensure_keep_pct(KeepPct)

    text_series = df[Col].astype(str).fillna('')
    vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    score = vectorizer.fit_transform(text_series)

    feature_names = vectorizer.get_feature_names_out()
    term_matrix = (
        pd.DataFrame(score.toarray(), columns=feature_names)
          .replace(0, np.nan)
          .dropna(thresh=max(1, int(np.ceil(len(df) * KeepPct))), axis=1)
          .fillna(0)
    )

    if term_matrix.shape[1] == 0:
        raise ValueError('No TF-IDF features remain after applying KeepPct')

    if K > len(term_matrix):
        raise ValueError('K must be less than or equal to the number of rows in df')

    model = KMeans(n_clusters=K, random_state=11)
    df_out = df.copy()
    df_out[ColName] = model.fit_predict(term_matrix)
    return df_out.drop(columns=[Col])


def calc_quantile(df, Col, NewCol, Groups):
    '''
    Creates a new column containing quantile bucket labels for a numeric column.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The numeric column to bucket.
        NewCol (str): The name of the new quantile bucket column.
        Groups (int): The number of equal-sized buckets.

    Returns:
        pd.DataFrame: The DataFrame with the new quantile bucket column.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])
    _ensure_numeric_column(df, Col)
    _ensure_positive_int(Groups, 'Groups')

    labels = pd.qcut(df[Col], Groups, labels=False, duplicates='drop')
    if labels.isna().any() or labels.nunique(dropna=True) < Groups:
        raise ValueError('Groups must be smaller than or equal to the number of unique values in the column')

    df[NewCol] = labels + 1
    return df


def calc_min_max_norm(df, Col, NewCol):
    '''
    Scales a numeric column to the [0, 1] range using min-max normalization.

    Args:
        df (pd.DataFrame): The source DataFrame.
        Col (str): The numeric column to normalize.
        NewCol (str): The name of the new normalized column.

    Returns:
        pd.DataFrame: The DataFrame with the normalized column added.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [Col])
    _ensure_numeric_column(df, Col)

    series = df[Col]
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        df[NewCol] = 0.0
        return df

    df[NewCol] = (series - min_val) / (max_val - min_val)
    return df


def easy_drop(df, target):
    '''
    Drops unhelpful feature columns before modeling.

    Args:
        df (pd.DataFrame): The source DataFrame.
        target (str): The target column to keep.

    Returns:
        pd.DataFrame: The DataFrame containing the filtered feature columns and target column.
    '''
    _ensure_dataframe(df)
    _ensure_columns_exist(df, [target])

    target_series = df[target].copy()
    features = df.drop(columns=[target])

    missing_pct = features.isna().mean()
    features = features.drop(columns=missing_pct[missing_pct > 0.9].index.tolist())

    cat_features = features.select_dtypes(include=['object', 'category'])
    num_features = features.select_dtypes(include=np.number)

    cat_features = cat_features.loc[:, cat_features.nunique(dropna=False) != 1]
    num_features = num_features.loc[:, num_features.nunique(dropna=False) != 1]

    cat_features = cat_features.loc[:, cat_features.nunique(dropna=False) < 100]

    result = pd.concat([cat_features, num_features, target_series], axis=1)
    return result
