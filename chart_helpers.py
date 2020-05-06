import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from stats_helpers import growth_factor_for_region, cfr_for_region, lin_reg_for_time_series


def ax_plot_region_set(ax, data, region='Global'):
    '''
    Plot all three data types for a region for a given plot.
       
    Parameters: 
        ax (axis): matplotlib axis
        data (dict): clean data set including all types and regions
        region (str): region string, optional
    '''
    ax.plot(data['confirmed'][region], label='Confirmed')
    ax.plot(data['recovered'][region], label='Recovered')
    ax.plot(data['deaths'][region], label='Deaths')
    

def plot_for_region(data, region='Global'):
    '''
    Plot both lin and log space line charts for all three 
    data types for a given region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string
    '''
    fig, (ax_lin, ax_log) = plt.subplots(1, 2, figsize=(15, 6))

    ax_lin.set_title('Summary (lin)', loc='left')
    ax_plot_region_set(ax_lin, data, region)
    ax_lin.legend(loc='upper left')
    ax_lin.set_ylabel('Cases', fontsize=12)

    ax_log.set_title('Summary (log)', loc='left')
    ax_log.set_yscale('log')
    ax_plot_region_set(ax_log, data, region)
    ax_log.legend(loc='upper left')
    
    fig.autofmt_xdate()
    plt.show()

    
def plot_growth_factor_for_region(data, region='Global'):
    '''
    Plot growth factor over time for region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string
    '''
    df = growth_factor_for_region(data, region)
    ax = df.plot()
    plt.axhline(y=1, color='black', linestyle='-')
    plt.axhline(y=df.mean(), color='r', linestyle='--')
    
    
def plot_cfr_for_region(data, region='Global', t=7):
    '''
    Plot current fatality rate over time for region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
        t (int): time, optional
    '''
    df = cfr_for_region(data, region, t)
    ax = df.plot()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.axhline(y=df.mean(), color='r', linestyle='--')

    
def plot_lin_reg_for_cfr_for_region(data, region='Global', t=7):
    '''
    Plot linear regression for current fatality rate over time for region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
        t (int): time, optional
    '''
    cfr_df = cfr_for_region(data, region, t)
    lf_df = lin_reg_for_time_series(cfr_df)
    
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))

    if lf_df is not None: 
        ax.plot(lf_df, color='red')
    else:
        print('Could not calculate CFR Linear Regression for this region.')
    ax.plot(cfr_df, color='gray')

    fig.autofmt_xdate()
    plt.show()

    
def stats_for_region(data, region='Global'):
    '''
    Print stats for all three data types for a given region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
        
    Returns:
        output (DataFrame): Pandas DataFrame
    '''
    out = [[
        '{:,}'.format(data['confirmed'][region][-1]),
        '{:,}'.format(data['recovered'][region][-1]),
        '{:,}'.format(data['deaths'][region][-1])
    ]]
    
    return pd.DataFrame(out, columns=['Confirmed', 'Recovered', 'Deaths'], index=[region])


def growth_factor_stats_for_region(data, region='Global'):
    '''
    Print stats for growth factor for a given region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
    
    Returns:
        output (DataFrame): Pandas DataFrame, current and mean growth factor
    '''
    df = growth_factor_for_region(data, region)
    out = [[df[-1], df.mean()]]
    
    return pd.DataFrame(out, columns=['Current', 'Mean'], index=[region])


def cfr_stats_for_region(data, region='Global', t=7):
    '''
    Print stats current fatality rate for a given region.
       
    Parameters: 
        data (dict): clean data set including all types and regions
        region (str): region string, optional
        t (int): time, optional
    
    Returns:
        output (DataFrame): Pandas DataFrame, current and mean fatality rate
    '''
    df = cfr_for_region(data, region, t)
    out = [['{:.2%}'.format(df[-1]), '{:.2%}'.format(df.mean())]]
    
    return pd.DataFrame(out, columns=['Current', 'Mean'], index=[region])
