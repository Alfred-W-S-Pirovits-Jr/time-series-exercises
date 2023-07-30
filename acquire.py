import env
import pandas as pd
import numpy as np
import os

def get_zillow_data():
    filename = 'zillow.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=[0])
    else:
        # read the SQL query into a dataframe
        zillow_db = pd.read_sql('''
                                SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
                                FROM properties_2017
                                WHERE propertylandusetypeid = 261 -- Single Family Residence
                                ''', get_db_url('zillow'))
        
        # Write that dataframe to disk for later.  Called "caching" the data for later.
        zillow_db.to_csv(filename)
        
        return zillow_db
    
def get_store_data():

    filename = 'store_data.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col=[0])
    else:
        # read the SQL query into a dataframe
        store_data = pd.read_sql('''SELECT *
                                    FROM items
                                    JOIN sales USING (item_id)
                                    JOIN stores USING (store_id);
                                 ''', env.get_db_url('tsa_item_demand'))
        # Write that dataframe to disk for laer. "caching"
        store_data.to_csv(filename)