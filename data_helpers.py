import pandas as pd


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
