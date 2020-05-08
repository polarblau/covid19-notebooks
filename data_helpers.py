import pandas as pd
import datetime

from stats_helpers import (growth_factor_for_region, 
                           cfr_for_region, lin_reg_for_time_series)


SUPPORTED_DATA_TYPES = ['confirmed', 'deaths', 'recovered']


def load_data(base_url, types=SUPPORTED_DATA_TYPES):   
    '''
    Load data as CSV file for specified types.
       
    Parameters: 
        base_url (str): Base URL including type placeholder "{}"
        types (array): List of types, optional
    
    Returns:
        raw_dfs (dict): Dict of Pandas dataframes for each type
        
    Example:
        load_data('http://foo.com/bar_{}.csv', ['confirmed', 'deaths'])
    '''
    
    raw_dfs = {}

    for key in types:
        if key not in SUPPORTED_DATA_TYPES:
            raise ValueError('Key "{}" is not a supported data type.'.format(key))
        df = pd.read_csv(base_url.format(key))
        raw_dfs[key] = df
    
    return raw_dfs


def clean_data(raw_df):   
    '''
    Remove unused columns, transpose and group data in dataframe.
       
    Parameters: 
        raw_df (DataFrame): Pandas dataframe to be cleaned
    
    Returns:
        df (DataFrame): Pandas dataframe
    '''
    df = raw_df.drop(columns=['Province/State', 'Lat', 'Long'])
    df = df.groupby(['Country/Region']).sum().T
    df.index = pd.to_datetime(df.index)
    df['Global'] = df.sum(axis=1)
    
    return df



def export_stats(data):
    return data

def export_growth_factor(data):
    return { k: growth_factor_for_region(data, k) for k in data['confirmed'] }
    
def export_cfr(data):
    return { k: cfr_for_region(data, k, t=7) for k in data['confirmed'] }
   
def export_cfr_lin_reg(data):
    out = {}
    for region in data['confirmed']:
        try:
            cfr_df = cfr_for_region(data, region, t=7)
            out[region] = lin_reg_for_time_series(cfr_df)
        except:
            print('Failed to call "export_cfr_lin_reg()" for region "{}".'.format(region))
    return out
    
def export_data(data):
    ts = datetime.date.today().strftime('%Y%m%d')
    
    manifest = ['stats', 'growth_factor', 'cfr', 'cfr_lin_reg']
    
    for key in manifest:
        filename = '{}_{}.json'.format(ts, key)
        out = globals()['export_{}'.format(key)](data)
        pd.Series(out).to_json(filename, orient='columns')
        print('Exported {} [ {} ].'.format(key, filename))

    
    
    
    
    