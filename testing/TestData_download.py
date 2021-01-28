# Data from ACS (american community survey data) used for testing code in this package

import pandas as pd
import numpy as np
import census

# https://api.census.gov/data/key_signup.html
c = census.Census("Request API key from link presented on line 7")

# Functions
def GetData(Variable, Geography):
    df = pd.DataFrame(c.acs5.get(Variable, {'for': Geography}))
    return df

# List of all tables
List_ACStables = c.acs5.tables()


# Available geography hierarchies
# https://api.census.gov/data/2016/acs/acs5/geography.html
Geo_AllStates = 'state:*'
Geo_AllZIPs = 'zip code tabulation area:*'


# Variables pulled
# https://api.census.gov/data/2019/acs/acs5/variables.html
# https://censusreporter.org/
# https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2019_ACSSubjectDefinitions.pdf
Pop_CountAll = 'B01001_001E'
Pop_CountMale = 'B01001_002E'
Pop_CountFemale = 'B01001_026E'
Pop_Undergrad25p = 'B15003_022E'
Pop_Masters25p = 'B15003_023E'
Pop_Doctor25p = 'B15003_025E'

Pop_CountMedicareMale = 'C27006_010E'
Pop_CountMedicareFemale = 'C27006_020E'
Pop_CountPrivHealthcare = 'B27002_001E'


Pop_Unemployed = 'B23025_005E'
Pop_Labor = 'B23025_003E'

Household_TotalCount = 'B28001_001E'
Household_MedianIncome = 'B19013_001E'
Household_MedianGrossRent = 'B25064_001E'
Household_FoodStamp = 'B22003_002E'
Household_withComputingDevice = 'B28001_002E' #B28008_002E
Household_withInternet = 'B28002_002E'
Household_VehicleZero = 'B08201_002E'
Household_VehicleOne = 'B08201_003E'
Household_VehicleTwo = 'B08201_004E'
Household_VehicleThree = 'B08201_005E'
Household_VehicleFour = 'B08201_006E'
Household_BedroomOne = 'B25042_004E'
Household_BedroomTwo = 'B25042_005E'
Household_BedroomThree = 'B25042_006E'
Household_BedroomFour = 'B25042_007E'
Household_BedroomFive = 'B25042_008E'

# Spot checked median age https://www.unitedstateszipcodes.org/61112/
MedianAge = 'B01002_001E'

# Pull Data
df = (
      # Population Counts
      GetData(Pop_CountAll, Geo_AllZIPs)     
      .merge(GetData(Pop_CountMale, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Pop_CountFemale, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')  
      .merge(GetData(Pop_Undergrad25p, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')  
      .merge(GetData(Pop_Masters25p, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Pop_Doctor25p, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      
      # Age
      .merge(GetData(MedianAge, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      
      # Health Insurance
      .merge(GetData(Pop_CountMedicareMale, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Pop_CountMedicareFemale, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Pop_CountPrivHealthcare, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      
      # Finances
      .merge(GetData(Pop_Unemployed, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Pop_Labor, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      
      # Household
      .merge(GetData(Household_TotalCount, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Household_MedianIncome, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Household_MedianGrossRent, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Household_FoodStamp, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Household_withComputingDevice, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Household_withInternet, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area') 
      .merge(GetData(Household_VehicleZero, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_VehicleOne, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_VehicleTwo, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_VehicleThree, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_VehicleFour, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_BedroomOne, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_BedroomTwo, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_BedroomThree, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_BedroomFour, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      .merge(GetData(Household_BedroomFive, Geo_AllZIPs), how = 'inner', on = 'zip code tabulation area')
      
      # Change names from Census codes to English
      .rename(columns={'zip code tabulation area': 'ZIP',
                       Pop_CountAll: 'Pop_Count', 
                       Pop_CountMale: 'Pop_CountMale',
                       Pop_CountFemale: 'Pop_CountFemale',
                       
                       MedianAge: 'MedianAge',
                       
                       Pop_Undergrad25p: 'Pop_Undergrad25p',
                       Pop_Masters25p: 'Pop_Masters25p',
                       Pop_Doctor25p: 'Pop_Doctor25p',
                       
                       Pop_CountMedicareMale: 'Pop_CountMedicareMale',
                       Pop_CountMedicareFemale: 'Pop_CountMedicareFemale',  
                       Pop_CountPrivHealthcare: 'Pop_CountPrivHealthcare',
                       
                       Pop_Unemployed: 'Pop_Unemployed',
                       Pop_Labor: 'Pop_Labor',
                       
                       Household_TotalCount: 'Household_TotalCount',
                       Household_MedianIncome: 'Household_MedianIncome',
                       Household_MedianGrossRent: 'Household_MedianGrossRent',
                       Household_FoodStamp: 'Household_FoodStamp',
                       Household_withComputingDevice: 'Household_withComputingDevice',
                       Household_withInternet: 'Household_withInternet',
                       Household_VehicleZero: 'Household_VehicleZero',
                       Household_VehicleOne: 'Household_VehicleOne',
                       Household_VehicleTwo: 'Household_VehicleTwo',
                       Household_VehicleThree: 'Household_VehicleThree',
                       Household_VehicleFour: 'Household_VehicleFour',
                       Household_BedroomOne: 'Household_BedroomOne',
                       Household_BedroomTwo: 'Household_BedroomTwo',
                       Household_BedroomThree: 'Household_BedroomThree',
                       Household_BedroomFour: 'Household_BedroomFour',
                       Household_BedroomFive: 'Household_BedroomFive',
                       })
         

      # Data Cleanup
      # Need to concat "ZIP" pre-fix or leading zeros will be lost
      .assign(ZIP = lambda x: 'ZIP ' + x.ZIP)
      # Reorder Fields
      .iloc[:, np.r_[1,0,2:29]]
      )

# Calculated Fields
df_calc = (df
           .assign(UnemployRate = lambda x: x.Pop_Unemployed / x.Pop_Labor)
           .assign(Pop_CollegeAbove = lambda x: x.Pop_Undergrad25p + x.Pop_Masters25p + x.Pop_Doctor25p)
           .assign(Pop_MedicareTotal = lambda x: x.Pop_CountMedicareMale + x.Pop_CountMedicareFemale)
           )

# Save
path = 'xxxxxxxxxxx'
df_calc.to_csv(path + 'CensusDataOutput.csv', index = False)
