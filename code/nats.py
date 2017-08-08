"""This file contains code used in "Think Stats",
by Allen B. Downey available from greenteapress.com
""" 

from __future__ import print_function, division

import math
import random
import numpy as np
import pandas as pd
from sas7bdat import SAS7BDAT
import thinkstats2 as ts2
import thinkplot as tp
import matplotlib.pyplot as plt

def MakeFrames():
    """
    Reads NATS data and partitions by smoker status.

    returns DataFrames: (everyday, someday, former, never)
    """

    data = SAS7BDAT('nats_09_10.sas7bdat')
    data = data.to_data_frame()
    CleanNats(data)
    assert len(data) == 118581

    everyday = data[data.smokstatus_r==1]
    someday = data[data.smokstatus_r==2]
    former = data[data.smokstatus_r==3]
    never = data[data.smokstatus_r==4]

    assert len(everyday) == 12894
    assert len(someday) == 3648
    assert len(former) == 34327
    assert len(never) == 67272

    return (data, everyday, someday, former, never)

def CleanNats(df):
    """Recodes variables from the NATS frame.

    df: DataFrame
    """

    #Replace the values of 7 and 9 with nan
    na_vals = [7, 9]
    df.EMPLOY2.replace(na_vals, np.nan, inplace=True)
    assert sum(pd.notnull(df.EMPLOY2).astype(int)) == 118278

    df.NOJOBS.replace(na_vals, np.nan, inplace=True)
    assert sum(pd.notnull(df.NOJOBS).astype(int)) == 65689

    df.Worksmokind_r.replace(na_vals, np.nan, inplace=True)
    assert sum(pd.notnull(df.Worksmokind_r).astype(int)) == 59806

    df.Worksmokout_r.replace(na_vals, np.nan, inplace=True)
    assert sum(pd.notnull(df.Worksmokout_r).astype(int)) == 63615
    
    df.HCCOVERAGE.replace(na_vals, np.nan, inplace=True)
    assert sum(pd.isnull(df.HCCOVERAGE).astype(int)) == 745
      
    df.QTMED2.replace(na_vals, np.nan, inplace=True)
    assert sum(pd.isnull(df.QTMED2).astype(int)) == 109444


    #Replace the values of 777, 888, 999 with nan
    df.SMOKWHOLAGE.replace([777, 888, 999], np.nan, inplace=True)
    assert sum(pd.isnull(df.SMOKWHOLAGE).astype(int)) == 54055


    #Replace 9 with nan
    df.Sltever2_r.replace(9, np.nan, inplace=True)
    assert sum(pd.isnull(df.Sltever2_r).astype(int)) == 110

    df.currentslt_r.replace(9, np.nan, inplace=True)
    assert sum(pd.isnull(df.currentslt_r).astype(int)) == 169

    df.Snusever_r.replace(9, np.nan, inplace=True)
    assert sum(pd.isnull(df.Snusever_r).astype(int)) == 226

    df.Cigarever_r.replace(9, np.nan, inplace=True)
    assert sum(pd.isnull(df.Cigarever_r).astype(int)) == 208

    df.smokstatus_r.replace(9, np.nan, inplace=True)
    assert sum(pd.isnull(df.smokstatus_r).astype(int)) == 440

    #Replace 77, 96, 99 with nan
    df.MARITAL2.replace([77, 96, 99], np.nan, inplace=True)
    assert sum(pd.isnull(df.MARITAL2).astype(int)) == 1080

    #Replace 666, 777, 888, 999 with nan
    df.SMOKPERDAY.replace([666, 777, 888, 999], np.nan, inplace=True)
    assert sum(pd.isnull(df.SMOKPERDAY).astype(int)) == 105815

    #Replace 77, 88, 99 with nan
    df.QTATT2.replace([77, 88, 99], np.nan, inplace=True)
    assert sum(pd.isnull(df.QTATT2).astype(int)) == 101428



def MakeHist(series, label, column):
    """Create histograms for variables with numeric values.

    series: pd Series object
    label: string
    column: string
    """
    hist = ts2.Hist(series[column].dropna(), label=label)
    tp.Hist(hist)

def MakeCdfPlot(series, label, column, units):
    """Creates a CDF plot for a series.

    series: pd Series object
    label: string
    column: string
    """
    cdf = ts2.Cdf(series[column], label=label)
    tp.Cdf(cdf)
    upper = cdf.Value(0.99)
    tp.Plot([upper, upper], [0, 1], color='gray', linewidth=3)
    median = cdf.Value(0.5)
    print('%s: \n99th %%-ile: %d %s' % (label, cdf.Value(0.99), units))
    print('Median: %0.2f %s' % (median, units))

def Summarize(everyday, someday, former, column, units, flag=False):
    """Print various summary statistics for a given column."""

    mean = everyday[column].dropna().mean()
    var = everyday[column].dropna().var()
    std = everyday[column].dropna().std()

    print('Daily Smokers:')
    print('Mean: %.3f %s' % (mean, units))
    print('Variance: %.3f %s ^ 2' % (var, units))
    print('Standard Deviation: %.3f %s\n' % (std, units))
    
    if flag==True:
        mean = someday[column].dropna().mean()
        var = someday[column].dropna().var()
        std = someday[column].dropna().std()

        print('Non-Daily Smokers:')
        print('Mean: %.3f %s' % (mean, units))
        print('Variance: %.3f %s ^ 2' % (var, units))
        print('Standard Deviation: %.3f %s\n' % (std, units))
    
    if flag==True:
        mean = former[column].dropna().mean()
        var = former[column].dropna().var()
        std = former[column].dropna().std()

        print('Daily Smokers:')
        print('Mean: %.3f %s' % (mean, units))
        print('Variance: %.3f %s ^ 2' % (var, units))
        print('Standard Deviation: %.3f %s\n' % (std, units))

def SampleMeanVarWeighted(xs, weights):
    xbar = sum(weights * xs)/sum(weights)
    
    v1 = sum(weights)
    v2 = sum(weights**2)
    dev = xs - xbar
    var = v1 / (v1**2 - v2)*sum(weights*dev**2)
    return xbar, var

def SampleMeanVWeighted(xs, weights):
    xbar = sum(weights * xs)/sum(weights)
    return xbar

def SummarizeWeighted(everyday, someday, former, column, units, flag=False):
    """Print various weighted summary statistics for a given column."""
    df = everyday.dropna(subset=[column, 'WT_national'])
    mean, var = SampleMeanVarWeighted(df[column], df.WT_national)
    std = math.sqrt(var)

    print('Daily Smokers:')
    print('Mean: %.3f %s' % (mean, units))
    print('Variance: %.3f %s ^ 2' % (var, units))
    print('Standard Deviation: %.3f %s\n' % (std, units))
    
    if flag==True:
        df = someday.dropna(subset=[column, 'WT_national'])
        mean, var = SampleMeanVarWeighted(df[column], df.WT_national)
        std = math.sqrt(var)
        print('Non-Daily Smokers:')
        print('Mean: %.3f %s' % (mean, units))
        print('Variance: %.3f %s ^ 2' % (var, units))
        print('Standard Deviation: %.3f %s\n' % (std, units))
    
    if flag==True:
        df = former.dropna(subset=[column, 'WT_national'])
        mean, var = SampleMeanVarWeighted(df[column], df.WT_national)
        std = math.sqrt(var)
        print('Former Smokers:')
        print('Mean: %.3f %s' % (mean, units))
        print('Variance: %.3f %s ^ 2' % (var, units))
        print('Standard Deviation: %.3f %s\n' % (std, units))

class HypothesisTest(object):
    """Represents a hypothesis test."""
    
    def __init__(self, data):
        """Initializes.
        
        data: data in whatever form is relevant
        """
        self.data = data
        self.MakeModel()
        self.actual = self.TestStatistic(data)
        self.test_stats = None
        self.Cdf = None

    def PValue(self, iters=1000):
        """Computes the distribution of the test statistic and p-value.
        
        iters: number of iterations
        returns: float p-value
        """
        self.test_stats = [self.TestStatistic(self.RunModel()) for _ in range(iters)]
        self.test_cdf = ts2.Cdf(self.test_stats)
        
        count = sum(1 for x in self.test_stats if x >= self.actual)
        return count / iters
    
    def MaxTestStat(self):
        """Returns the largest test statistic seen during simulations.
        """
        return max(self.test_stats)

    def PlotCdf(self, label=None):
        """Draws a Cdf with vertical lines at the observed test stat.
        """
        def VertLine(x):
            """Draws a vertical line at x."""
            tp.Plot([x, x], [0, 1], color='0.8')

        VertLine(self.actual)
        tp.Cdf(self.test_cdf, label=label)

    def TestStatistic(self, data):
        """Computes the test statistic.

        data: data in whatever form is relevant
        """
        raise UnimplementedMethodException()

    def MakeModel(self):
        """Build a model of the null hypothesis.
        """
        pass

    def RunModel(self):
        """Run the model of the null hypothesis.

        returns: simulated data
        """
        raise UnimplementedMethodException()

class UnimplementedMethodException(Exception):
    """Exception if someone calls a method that should be overridden."""

class DiffMeansPermute(HypothesisTest):
    """Tests a difference in means by permutation."""

    def TestStatistic(self, data):
        """Computes the test statistic.

        data: data in whatever form is relevant
        """
        group1, group2 = data
        test_stat = abs(group1.mean() - group2.mean())
        return test_stat

    def MakeModel(self):
        """Build a model of the null hypothesis.
        """
        group1, group2 = self.data
        self.n, self.m = len(group1), len(group2)
        self.pool = np.hstack((group1, group2))

    def RunModel(self):
        """Run the model of the null hypothesis/

        returns: simulated data
        """
        np.random.shuffle(self.pool)
        data = self.pool[:self.n], self.pool[self.n:]
        return data

class DiffMeansOneSided(DiffMeansPermute):
    """Tests a one-sided difference in means by permutation."""

    def TestStatistic(self, data):
        """Computes the test statistic.

        data: data in whatever form is relevant
        """
        group1, group2 = data
        test_stat = group1.mean() - group2.mean()
        return test_stat
class DiffStdPermute(DiffMeansPermute):
    """Tests a one-sided difference in standard deviation by permutation."""

    def TestStatistic(self, data):
        """Computes the test statistic.

        data: data in whatever form is relevant
        """
        group1, group2 = data
        test_stat = group1.std() - group2.std()


class CorrelationPermute(HypothesisTest):
    """Tests correlations by permutation."""

    def TestStatistic(self, data):
        """Computes the test statistic.

        data: tuple of xs and ys
        """
        xs, ys = data
        test_stat = abs(ts2.Corr(xs, ys))
        return test_stat

    def RunModel(self):
        """Run the model of the null hypothesis.
        
        returns: simulated data
        """
        xs, ys = self.data
        xs = np.random.permutation(xs)
        return xs, ys


def FalseNegRate(data, num_runs=1000):
    """Computes the chance of a false negative rate based on resampling.
    data: pair of sequences
    num_runs = how many experiments to simulate

    returns: float false negative rate
    """
    group1, group2 = data
    count = 0

    for i in range(num_runs):
        sample1 = ts2.Resample(group1)
        sample2 = ts2.Resample(group2)
        ht = DiffMeansPermute((sample1, sample2))
        p_value = ht.PValue(iters=101)
        if p_value > 0.05:
            count += 1

    return count / num_runs


##Resampling

def Resample(xs, n=None):
    """Draw a sample from xs with the same length as xs.

    xs: sequence
    n: sample size (default: len(xs))

    returns: NumPy array
    """
    if n is None:
        n = len(xs)
    return np.random.choice(xs, n, replace=True)

def SampleRows(df, nrows, replace=False):
    """Choose a sample of rows from a DataFrame.

    df: DataFrame
    nrows: number of rows
    replace: whether to sample with replacement
    """
    indices = np.random.choice(df.index, nrows, replace=replace)
    sample = df.loc[indices]
    return sample

def ResampleRows(df):
    """Resamples rows from a DataFrame.
    df: DataFrame

    returns: DataFrame
    """
    return SampleRows(df, len(df), replace=True)

def ResampleRowsWeighted(df, column='WT_national'):
    """Resamples a DataFrame using probabilities proportional to given column.
    
    df: DataFrame
    column: string column name to use as weights

    returns: DataFrame
    """
    weights = df[column].copy()
    weights /= sum(weights)
    indices = np.random.choice(df.index, len(df), replace=True, p=weights)
    sample = df.loc[indices]
    return sample

def VertLine(x):
    """Draws a vertical line at x."""
    tp.Plot([x, x], [0, 1], color='0.8')
