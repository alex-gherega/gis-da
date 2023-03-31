import numpy as np

# stats
from scipy import stats
from scipy.stats import shapiro, kstest 
from statsmodels.tsa.seasonal import seasonal_decompose, STL, MSTL, DecomposeResult
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

zivot_andrews.__name__ = 'Zivot-Andrews' # due to the terrible incosistencies in the statsmodels API

# stationarity tests
def _compile_msg(colname, title, stats, full=True):
    t_stat, p_value, critical_values = stats
    message = f'{colname} {title} Statistic: {t_stat:.2f}'

    message = message +\
              ''.join([f'\nCritial Values:\n   {key}, {value:.2f}' for key,value in critical_values.items()]) +\
              f'\np-value: {p_value:.2f}\n'\
              if full else message

    return message


def do_sugar(stationarity_fn=adfuller, selectors=[0,1,4], hypothesis_fn=lambda p_value: not p_value):

    return lambda x, **kwargs: np.concatenate([[stationarity_fn, hypothesis_fn],
                                               np.array(stationarity_fn(x, **kwargs))[selectors]])

sugars = dict([(test_fn.__name__.title(), do_sugar(test_fn, selectors, hypo_fn))

               for test_fn, selectors, hypo_fn in

               [(adfuller, [0,1,4], lambda p_value: p_value < 0.05),
                (kpss, [0,1,3], lambda p_value: p_value > 0.05),
                (zivot_andrews, [0,1,2], lambda p_value: p_value < 0.05)]])

def check_stationarity(df, column,
                       test_fn=do_sugar(),
                       withmsg=False,
                       **kwargs):#={autolags='AIC'}):
    """data is a 1-D np.array
    test_fn = lambda x, **kwargs: np.concatenate([[kpss],
                                               np.array(kpss(x, **kwargs))[0,1,3]]) 
            
    test_fn = lambda x, **kwards: np.concatenate([[kpss],
                                               np.array(kpss(x, **kwargs))[0,1,2]])"""
    
    test_fn, test_hypo, t_stat, p_value, critical_values = test_fn(df[column].dropna().values, **kwargs)

    message = _compile_msg(column, test_fn.__name__.title(), [t_stat, p_value, critical_values], withmsg) 

    result = {'stationary': test_hypo(p_value)}
    
    print(f'{message}\n{result}\n')
    return result
