

"""

 module to calculate welch t-statistics
 see copyright below

"""

import warnings;
warnings.simplefilter("ignore",DeprecationWarning)

from math import log;
from scipy import std;
from scipy import mean;
from math import sqrt;
from sys import stderr

def stddev(arr):
	N=len(arr);
	return sqrt((std(arr)**2)*N/(N-1));


import numpy as n;
import scipy;
import scipy.stats;
#from numpy.testing import NumpyTest, NumpyTestCase


def welchs_approximate_ttest(n1, mean1, sem1, \
                            n2, mean2, sem2):  #, alpha
#    '''Welch''s approximate t-test for the difference of two means of
#heteroscedasctic populations.

#Implemented from Biometry, Sokal and Rohlf, 3rd ed., 1995, Box 13.4

#:Parameters:
#    n1 : int
#        number of variates in sample 1
#    n2 : int
#        number of variates in sample 2
#    mean1 : float
#        mean of sample 1
#    mean2 : float
#        mean of sample 2
#    sem1 : float
#        standard error of mean1
#    sem2 : float
#        standard error of mean2
#    alpha : float
#        desired level of significance of test

#:Returns:
#    significant : bool
#        True if means are significantly different, else False
#    t_s_prime : float
#        t_prime value for difference of means
#    t_alpha_prime : float
#        critical value of t_prime at given level of significance

#Copyright (c) 2007, Angus McMorland

#All rights reserved.

#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:

 #   * Redistributions of source code must retain the above copyright
 #   notice, this list of conditions and the following disclaimer.
 #   * Redistributions in binary form must reproduce the above copyright
 #   notice, this list of conditions and the following disclaimer in the
 #   documentation and/or other materials provided with the distribution.
 #   * Neither the name of the University of Auckland, New Zealand nor
 #   the names of its contributors may be used to endorse or promote
 #   products derived from this software without specific prior written
 #   permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#SPECIAL,EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.'''
    svm1 = sem1**2 * n1
    svm2 = sem2**2 * n2
    meandiff=mean1-mean2;
    t_s_prime = meandiff/n.sqrt(svm1/n1+svm2/n2)
    sv1=sem1**2;
    sv2=sem2**2;
    upper=(sv1+sv2)**2
    lower=(sv1**2)/(n1-1)+(sv2**2)/(n2-1)
   
    df=int(upper/lower);

    pval=scipy.stats.t.cdf(t_s_prime, df);
    if(pval>0.5):
	pval=1.0-pval;
    #t_alpha_df1 = scipy.stats.t.ppf(1-alpha/2, n1 - 1)
    #t_alpha_df2 = scipy.stats.t.ppf(1-alpha/2, n2 - 1)
    #t_alpha_prime = (t_alpha_df1 * sem1**2 + t_alpha_df2 * sem2**2) / \
     #               (sem1**2 + sem2**2)
    return meandiff, df, t_s_prime, pval*2#, t_alpha_prime, abs(t_s_prime) > t_alpha_prime

#and a test class as well...

def welchs_approximate_ttest_sd(n1, mean1, sd1,\
                            n2, mean2, sd2): #, alpha
	return welchs_approximate_ttest(n1, mean1, sd1/n.sqrt(n1), \
                            n2, mean2, sd2/n.sqrt(n2)); #, alpha


def welchs_approximate_ttest_arr(arr1,arr2): #,alpha
	n1=len(arr1);
	n2=len(arr2);
	mean1=mean(arr1);
	mean2=mean(arr2);
	sd1=stddev(arr1);
	sd2=stddev(arr2);
	return welchs_approximate_ttest_sd(n1,mean1,sd1,n2,mean2,sd2); #,alpha

def ttest(arr1, arr2):
    return welchs_approximate_ttest_arr(arr1, arr2)[3]




