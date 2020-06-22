
"""--------------------------------------------------Pre-Processing Functions-------------------------------------------------"""
def ColumnKeep(df, ColList):
    df = df[ColList]
    return df 

def ColumnTypeChange(df, Col, DataType):
    # This function changes data types.
    # Converts this from a method into a function for easier data transformation piping    
    df[Col] = df[Col].astype(DataType)
    return df

def SubString_Middle(df, Col, Start, End):
    # Returns substring based on defined start and end positions
    # Use true counting for both Start and End positions, i.e. count 1, 2, 3, 4 etc... for both start and end positions
    df[Col] = df[Col].str[Start - 1 : End]
    return df

def PriceTypeCategory(df, ColPriceType):
    # This function takes the substring left of the hyphen
    # Price Type has two levels within the same string variable. Structure: "Level 1 - Level 2"
    # Example: "Bountiful Bargain - System Gen" ; "Bountiful Bargain - User Gen"
    
    # Dependent package
    import numpy as np
    
    new = df[ColPriceType].str.split(" - ", n = 1, expand = True) 
    df['PriceTypeLevel1'] = new[0]
    df['PriceTypeLevel1'] = df['PriceTypeLevel1'].str.strip() # Remove White Spaces
    
    # Fix spelling issues
    df['PriceTypeLevel1'] = np.where(df['PriceTypeLevel1'] == 'Healthly Savings', 'Healthy Savings', df['PriceTypeLevel1'])
    df['PriceTypeLevel1'] = np.where(df['PriceTypeLevel1'] == 'Price Reduction EDLP', 'EDLP Price', df['PriceTypeLevel1'])
    df.drop(columns = [ColPriceType], inplace = True)
    df.PriceTypeLevel1.value_counts()
    return df

def MakeML_Layers(df, InputLayerMap, Layer):
    df = (df
          .merge(InputLayerMap, how = 'left', on = 'Store_Code')
          .query('ML_Layer == Layer')
          .drop(columns = ['ML_Layer'])                  
          )
    return df

def Join(df, DF_add, JoinType, ColLeft, ColRight):
    import pandas as pd
    df = pd.merge(df, 
                  DF_add, 
                  how = JoinType,
                  left_on = ColLeft,
                  right_on = ColRight)
    return df

def SplitDate(df, SplitType, Col, ColName):
    import pandas as pd
    
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

def BetweenDateFilter(df, ColSelectionDate, ColStartDate, ColEndDate):
    # This function doesn't work with int
    df[ColSelectionDate] = df[ColSelectionDate].astype(float)  
    df[ColStartDate] = df[ColStartDate].astype(float)
    df[ColEndDate] = df[ColEndDate].astype(float)   
    df = df[df[ColSelectionDate].between(df[ColStartDate], df[ColEndDate])]   
    return df

def CalcEventLength(df, NewColName, ColStartDate, ColEndDate):
    import pandas as pd
    
    df[ColStartDate] = pd.to_datetime(df[ColStartDate], format='%Y%m%d')
    df[ColEndDate] = pd.to_datetime(df[ColEndDate], format='%Y%m%d')
    df[NewColName] = df[ColEndDate] - df[ColStartDate]
    df[NewColName] = df[NewColName].dt.days
    return df

def DateFormat(df, Col):
    import pandas as pd
    
    df[Col] = pd.to_datetime(df[Col], format='%Y%m%d')
    return df

def DataTypeChange(df, Col, Type):
    df[Col] = df[Col].astype(Type)
    return df

def DropDupes(df):
    df = df.drop_duplicates()
    return df

def LeftPadZero(df, Col, Len):
    df[Col] = df[Col].astype(str)
    df[Col] = df[Col].str.zfill(Len)
    return df

def DropCol(df,Col):
    df = df.drop([Col], axis = 1)
    return df   

def LeftChars(df, Col, Chars):
    df[Col] = df[Col].astype(str).str[0:Chars]
    return df

def FirstRowGroup(df, UniqueCol):
    df = df.groupby(UniqueCol) \
           .first() \
           .reset_index()
    return df

def RenameCol(df, Col, NewName):
    df = df.rename(columns={Col:NewName})
    return df

def ImputePromo(df, ColImpute):
    import numpy as np
    import math
    
    # Missing price calculated using discount pct; Missing pct calculated using price
    # Price = retail price
    if ColImpute == 'Promo_Price':
        df[ColImpute] = (df['Price'] - (df['Price'] * (df['Discount_Percent']/100))).where(df[ColImpute].isnull(), df[ColImpute])
    elif ColImpute == 'Discount_Percent':
        df[ColImpute] = (df['Promo_Price'] / df['Price']).where(df[ColImpute].isnull(), df[ColImpute])
        df = (df
              .assign(Discount_Percent = lambda x: np.where(x.Promo_Price == 0, 0, x.Discount_Percent))
              .assign(Discount_Percent = lambda x: np.where(x.Discount_Percent == math.inf, 99999 , x.Discount_Percent))
              .query('Discount_Percent != 99999')
              )
    else:
        print('ERROR: ColImpute must equal either Promo_Price or Discount_Percent')      
    return df

def DelRowzStringContain(df, Col, Contains):
    df['ContainsFlag'] = df[Col].str.contains(Contains)
    df = df[df.ContainsFlag != True]
    df = df.drop(['ContainsFlag'], axis = 1)
    return df

def StringContainKeep(df, Col, Contains):
    df['ContainsFlag'] = df[Col].str.contains(Contains)
    df = df[df.ContainsFlag == True]
    df = df.drop(['ContainsFlag'], axis = 1)
    return df

def DeleteInf(df):
    import numpy as np
    
    df = df[np.isfinite(df).all(1)]
    return df

def EncodeCatCol(df, Col):
    from sklearn.preprocessing import LabelEncoder
    
    df[Col] = LabelEncoder().fit_transform(df[Col])
    return df

def OHEcategoricals(df, Col):
    import pandas as pd
    
    temp_df = pd.get_dummies(df[Col],drop_first = True)
    df = df.merge(temp_df, left_index = True, right_index = True)
    df = df.drop([Col], axis = 1)
    return df

def Format_ProductCode(df):
    import pandas as pd
    # Sales Layers Product_Code formatting
    
    df = (df
          .pipe(DataTypeChange, Col = 'Product_Code', Type = str)
          .pipe(LeftPadZero, Col = 'Product_Code', Len = 11))
    return df


"""--------------------------------------------------ML Functions-------------------------------------------------"""


def TFIDF_2_Clusters(df, Col, ColName, K, KeepPct):
    from sklearn.feature_extraction.text import TfidfVectorizer
    import pandas as pd
    import numpy as np
    from sklearn.cluster import KMeans
    
    df2 = df.copy()
    df_TFIDFmatrix = df.copy()
    Keep = len(df_TFIDFmatrix) * KeepPct # keep columns >0.2% populated. This trims term matrix columns by roughly 50%
    
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

def MakeMLBuildingBlock(InputSales, InputProduct, InputAds, InputStore, InputUPC_Map):
    df = InputSales.copy()
    df = (df
          # Map Product_Code (UPC 11) to UPC 12
          .pipe(Join, DF_add = InputUPC_Map, # NOTE: Only 6,799 UPCs match between Movement file and UPCMAP file's UPC11 field
                      JoinType = 'inner',
                      ColLeft = 'Product_Code',
                      ColRight = 'UPC 11')
          .pipe(DropCol, Col = 'Product_Code')
    
          # Join remaining Sprouts Files: Product, Print Ads, Store
          .pipe(Join, DF_add = InputProduct, 
                      JoinType = 'inner', 
                      ColLeft = 'UPC 11',
                      ColRight = 'Product_Code')
          .pipe(DropCol, Col = 'Product_Code')
          .pipe(Join, DF_add = InputAds,
                      JoinType = 'inner', 
                      ColLeft = 'UPC 11',
                      ColRight = 'Product_Code')
          .pipe(DropCol, Col = 'Product_Code')
          .pipe(Join, DF_add = InputStore, 
                      JoinType = 'inner',
                      ColLeft = 'Store_Code',
                      ColRight = 'Store_Code')    
          .pipe(BetweenDateFilter, ColSelectionDate = 'Fiscal_Date',
                                   ColStartDate = 'Ad_Start_Date_ID',
                                   ColEndDate = 'Ad_End_Date_ID')
          
           # Impute missing promo prices
           .pipe(ImputePromo, ColImpute = 'Promo_Price')
           .pipe(ImputePromo, ColImpute = 'Discount_Percent')
          
          # Additional data wrangling
           .pipe(LeftChars, Col = 'Zip', Chars = 3)
           .pipe(DropCol, Col = 'Store_Address').pipe(DropCol, Col = 'City').pipe(DropCol, Col = 'Store_Size')
          )
    return df

def MakeBaseML(InputTrainX, InputTrainY):
    from sklearn.ensemble import GradientBoostingRegressor
    
    model = (GradientBoostingRegressor(n_estimators=1000, 
                                       learning_rate=0.1, 
                                       max_depth=100, 
                                       random_state=11, 
                                       loss='ls')
             .fit(InputTrainX, InputTrainY)
             )
    return model

def FilterBeforeDate(df, DateCol, YearStop, MonthStop, DayStop):
    import datetime
    
    df = df[(df[DateCol] < datetime.date(YearStop, MonthStop, DayStop))]
    return df

def FeatureEngineeringLayerSpecificMLInput(df):
    import pandas as pd
    
    TheOutput = df.copy()
    TheOutput = (TheOutput
                 # Extract Month, Day, and Day Of Week from date fields 
                 .pipe(SplitDate, SplitType = 'month',
                       Col = 'Ad_Start_Date_ID',
                       ColName = 'AdStartMonth')
                 .pipe(SplitDate, SplitType = 'day',
                       Col = 'Ad_Start_Date_ID',
                       ColName = 'AdStartDay')
                 .pipe(SplitDate, SplitType = 'day_of_week',
                       Col = 'Ad_Start_Date_ID',
                       ColName = 'AdStart_DOW')

                 # Calculate age of events
                 .pipe(CalcEventLength, NewColName = 'AdAgeAtPurchase',
                       ColStartDate = 'Ad_Start_Date_ID',
                       ColEndDate = 'Fiscal_Date')
                 .pipe(CalcEventLength, NewColName = 'AdDuration', 
                       ColStartDate = 'Ad_Start_Date_ID', 
                       ColEndDate = 'Ad_End_Date_ID')

                 # Assign text values to cluster using TF-IDF + KMeans
                 .pipe(TFIDF_2_Clusters, Col = 'Product_Description', 
                       ColName = 'ProductDescript_Cluster', 
                       K = 20, 
                       KeepPct = 0.002)
                 #.pipe(TFIDF_2_Clusters, Col = 'Category_Description', ColName = 'CatDescript_Cluster') # May not need this. Depends on full data's cardinality

                # Label Encoder for categorical fields where appropriate
                ################################################################### May have to dummy encode some of these when shifting from shell to actual########
                .pipe(EncodeCatCol, Col = 'Category_Description')
                .pipe(EncodeCatCol, Col = 'State')
                .pipe(EncodeCatCol, Col = 'Zip')
                .pipe(EncodeCatCol, Col = 'Ad_Event_Type')
                .pipe(EncodeCatCol, Col = 'Zone')
                .pipe(EncodeCatCol, Col = 'Ad_Price_Type')

                # One Hot Encoding for categorical fields where appropriate
                .pipe(OHEcategoricals, Col = 'PriceTypeLevel1') # formerly price_type

                # Final Drops
                .pipe(DropCol, Col = 'Ad_Start_Date_ID').pipe(DropCol, Col = 'Ad_End_Date_ID').pipe(DropCol, Col = 'Fiscal_Date')
                .pipe(DropCol, Col = "UPC 11").pipe(DropCol, Col = 'UPC 12')  # DROP IDs
                .drop(columns=['Size',
                               'Zip']) 

                # Tuned Drops
                .drop(columns=['Store_Code',
                               'Gluten_Free',
                               'No_GMO',
                               'AdDuration',
                               'Quantity',
                               'AdAgeAtPurchase',
                               'AdStart_DOW',
                               'State',
                               'Quantity',
                               'Ad_Price_Type',
                               'Zone',
                               'Page',
                               'Ad_Event_Type',
                               'Organic'])
                .pipe(DeleteInf)
                )
    return TheOutput

def MakeLayerResidualTable(InputLayerBase, InputPredicted, InputActual, InputTest):
    import pandas as pd
    
    TheOutput = (InputLayerBase
                 .pipe(ColumnKeep, ColList = ['Fiscal_Date','Store_Code','Movement','UPC 12'])
                 .pipe(DataTypeChange, Col = 'Store_Code', Type = str)
                 .merge((InputTest
                         .assign(Predicted = InputPredicted)
                         .assign(Actual = InputActual)
                         .pipe(ColumnKeep, ColList = ['Predicted','Actual'])), 
                        left_index = True, 
                        right_index = True
                        )
                 .reindex(columns = ['Fiscal_Date','Store_Code', 'UPC 12', 'Actual', 'Predicted'])
                 .assign(Residual = lambda x: x.Predicted - x.Actual)
                 )
    
    return TheOutput
