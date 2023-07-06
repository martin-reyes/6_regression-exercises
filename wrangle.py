import pandas as pd

import sys
import os

home_directory_path = os.path.expanduser('~')
sys.path.append(home_directory_path +'/utils')

from acquire_utils import get_connection

def wrangle_zillow_data():
    '''
    Acquire zillow data from MySQL database
    Prepare data by handling missing values and duplicates
    Save wrangled data into a csv
    '''
    filename = "data/zillow_data.csv"

    # Read the csv file if it exists
    if os.path.isfile(filename):
        return pd.read_csv(filename)
   
    else:
        # acquire MySQL data
        df = pd.read_sql('''SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet,
                                    taxvaluedollarcnt, yearbuilt, taxamount, fips 
                            FROM properties_2017 as p
                            WHERE p.propertylandusetypeid = 261;''',
                           get_connection('zillow'))
        
        # rename columns
        df.columns = ['bedrooms', 'bathrooms', 'sqft', 'property_value',
                      'year_built', 'property_tax', 'county']

        # filtering data to have "normal" number of bedrooms and bathrooms
        # 1 to 6 bedrooms
        df = df[(df['bedrooms'] >= 1) & (df['bedrooms'] <= 6)]
        # 1 to 6 bathrooms, not including 1.75
        df = df[(df['bathrooms'] >= 1) & (df['bathrooms'] <= 6) 
                & (df['bathrooms'] != 1.75)]

        # handle missing values
        df = df.dropna()

        # drop duplicates
        df = df.drop_duplicates()

        # Removing outliers
        df = df[(df['sqft'] <= 7_000) &
            (df['year_built'] >= 1900) &
            (df['property_tax'] <= 30_000)]

        # giving data appropriate types and values
        df[['bedrooms', 'sqft', 'property_value', 'year_built']] = \
            df[['bedrooms', 'sqft', 'property_value', 'year_built']].astype(int)
        # assigning county codes their respective names
        df['county'] = df['county'].replace({6037: 'LA', 6059: 'Orange', 6111: 'Ventura'})

        # cache data
        df.to_csv('data/zillow_data.csv', index=False)

    return df