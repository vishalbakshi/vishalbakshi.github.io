from __future__ import print_function, division
import pandas as pd
import numpy as np
import math
import random
import imp
import matplotlib.pyplot as plt
import mysql.connector
import nflqueries
from scipy import stats

def NflTtest(df1, df2, colname, values, title):
    '''NFLTEST outputs the distribution of p-values for 1000 iterations.
    p-values are for a difference of means two-sided t-test.
    
    inputs: df1, df2 (DataFrames), colname (string), values (list of strings), title (string)
    output: CDF plots of p-values
    '''
    p_vals = {}
    cdfs = []
    for value in values:
        for i in range(1000):
            np.random.seed(i)
            allteams_df = df1.query(str(colname) + " == " + "'" + value + "'")
            phi_df = df2.query(str(colname) + " == " + "'" + value + "'")
            sample1 = np.random.choice(np.asarray(allteams_df.YardsGained), len(phi_df))
            sample2 = np.random.choice(np.asarray(phi_df.YardsGained), len(phi_df))
            mu = allteams_df.YardsGained.mean() - phi_df.YardsGained.mean()
            p_value = stats.ttest_ind(sample1, sample2)[1]
            p_vals.setdefault(value, []).append(p_value)
            #Print out the p-value for one iteration
            if i == 5:
                print(title  + ':' + '\n')
                print('\t{:<18}\t{:<8}\t{:<8}'.format('Difference in Means', 'p-value', 'seed'))
                print('\t{:<18}\t{:<8}\t{:<8}'.format(mu, p_value, i))

    for key in p_vals.keys():
        p_vals[key] = np.asarray(p_vals[key])
        p_vals[key].sort()
        cdfs.append((key, p_vals[key], np.cumsum(p_vals[key]) / np.sum(p_vals[key])))
    #return cdfs    
    fig, axs = plt.subplots(nrows=len(values), ncols=1, figsize=(10,5*len(values)))
    
    if len(values) > 1:
        for i, ax in enumerate(axs):
            ax.plot(cdfs[i][1], cdfs[i][2])
            ax.set_xlabel('p-value', fontsize=12)
            ax.set_ylabel('CDF', fontsize=12)
            ax.set_title(title + ': ' + cdfs[i][0], fontsize=14)
    else:
        axs.plot(cdfs[0][1], cdfs[0][2])
        axs.set_xlabel('p-value', fontsize=12)
        axs.set_ylabel('CDF', fontsize=12)
        axs.set_title(title, fontsize=14)        
    plt.show()

def PlotCDF(t, xlabel, title):
    ''' PLOTCDF creates a CDF plot of a given series
    inputs: t (sequence), xlabel (string), values (sequence of strings)
    outputs: CDF plot
    '''
    cdfs = []
    t = np.asarray(t)
    t.sort()
    cdf = np.cumsum(t) / np.sum(t)

    fig, ax = plt.subplots(1, 1, figsize=(10,5))


    ax.plot(t, cdf)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('CDF', fontsize=12)
    ax.set_title(title, fontsize=14)        
    plt.show()
