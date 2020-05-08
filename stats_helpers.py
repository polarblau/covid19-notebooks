import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics


def growth_factor_for_region(data, region='Global'):
    '''
    Calculate growth factor over time for region.
    Algorithm used: (Day+0 - Day-1) / (Day-1 - Day-2)
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
        
    Returns:
        df (DataFrame): Pandas Dataframe for growth factor 
    '''
    df = data['confirmed'][region]
    # (Day+0 - Day-1) / (Day-1 - Day-2)
    df = df.rolling(3).apply(lambda x: (x[0] - x[1]) / (x[1] - x[2]), raw=True)
    # Clean data, replace NaN and values <= 0 with 0
    df = df.fillna(0)
    df[df <= 0] = 0
    # Skip first two as we are using a rolling window of 3
    df = df[2:]
    
    return df


def cfr_for_region(data, region='Global', t=7):
    '''
    Calculate case fatality rate 
    Algorithm used: CFR = deaths at day.x / cases at day.x-{T}
    (where T = average time period from case confirmation to death)
    https://www.worldometers.info/coronavirus/coronavirus-death-rate/
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
        time (int): time, optional
        
    Returns:
        series (Series): Pandas Series for CFR or None
    '''
    c = data['confirmed'][region]
    d = data['deaths'][region]

    raw = [0 if c[i-t] == 0 else d[i]/c[i-t] for i in range(t, len(d))]
    
    return pd.Series(raw, index=d[t:].index)


def lin_reg_for_time_series(df):
    '''
    Calculate linear regression model for time series.
       
    Parameters: 
        data (DataFrame): Time series data
        
    Returns:
        series (DataFrame): Pandas Series for prediction
    '''
    df = df[df.values > 0]
    
    if len(df.index) <= 0:
        return None
    
    labels, uniques = df.index.factorize()

    X = labels.reshape(-1,1)
    y = df.values.reshape(-1, 1)
    
    regressor = LinearRegression().fit(X, y)
    
    return pd.DataFrame(regressor.predict(X), index=uniques)[0]


def new_cases_per_region(data, region='Global'):
    '''
    Calculate new cases count per region.
       
    Parameters: 
        data (DataFrame): Time series data
        region (str): region string, optional
        
    Returns:
        series (DataFrame): Pandas Series
    '''
    df = data['confirmed'][region].rolling(2).apply(lambda x: x[1] - x[0], raw=True)
    df = df.fillna(0.0)
    
    return df