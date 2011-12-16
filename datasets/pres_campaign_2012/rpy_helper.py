# From git://gist.github.com/853885.git gist-853885

import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
import numpy as np
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import Matrix
R = robjects.r

def rhelp(fn_name, utils=importr("utils")):
    str(utils.help(fn_name))

def pify(rthing):
    """
    turn an r thing into a python thing
    >>> pify(R("2 * 2"))
    4.0

    >>> pify(R("c(1, 2, 3)"))
    [1.0, 2.0, 3.0]

    >>> pify(R("t.test(1:4, 1:4)"))
    {'null.value': {'difference in means': 0.0}, 'data.name': '1:4 and 1:4', 'method': 'Welch Two Sample t-test', 'p.value': 1.0, 'statistic': {'t': 0.0}, 'estimate': {'mean of y': 2.5, 'mean of x': 2.5}, 'conf.int': [-2.2337146951647044, 2.2337146951647044], 'parameter': {'df': 5.9999999999999982}, 'alternative': 'two.sided'}


    >>> a = np.arange(10)
    >>> b = np.array([2, 12, 4, 6, 1, 8, 9, 1, 3, 1])
    >>> ttest = R['t.test']

    >>> pify(ttest(a, b, alternative="two.sided"))["p.value"]
    0.89939605650576726

    >>> pify(ttest(a, b, alternative="less"))["p.value"]
    0.44969802825288363

    >>> chisquare = R['chisq.test']
    >>> A = [122, 14, 28, 11]
    >>> kwargs = {'simulate.p.value':True}
    >>> pify(chisquare(robjects.IntVector(A)))
    {'observed': [122, 14, 28, 11], 'residuals': [11.830288005188812, -4.4977772288098041, -2.3811761799581315, -4.9513345964208764], 'p.value': 5.0742757901326037e-41, 'statistic': {'X-squared': 190.37142857142857}, 'expected': [43.75, 43.75, 43.75, 43.75], 'data.name': 'c(122L, 14L, 28L, 11L)', 'parameter': {'df': 3.0}, 'method': 'Chi-squared test for given probabilities'}

    >>> df = R('data.frame(acol=1:4, bcol=letters[1:4])')
    >>> pify(df)
    rec.array([(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd')], 
          dtype=[('acol', '<i4'), ('bcol', '|S1')])


    """
    if isinstance(rthing, robjects.vectors.DataFrame):
        _r_unfactor(rthing)
        return np.rec.fromarrays(rthing, names=tuple(rthing.colnames))
    if hasattr(rthing, "nrow"):
        m = np.array(list(rthing)).reshape(rthing.nrow, rthing.ncol)
        return m

    if not hasattr(rthing, "iteritems"): 
        return rthing
    d = {}
    l = []
    for k, v in rthing.iteritems():
        if k is None:
            l.append(pify(v))
        else:
            d[k] = pify(v)
    if d and len(d) == 1 and None in d:
        return d[None]
    if l and len(l) == 1:
        # could be a list of length 1, but cant tell...
        return l[0]
    return d or l

def _r_unfactor(rdf):
    """
    convert factor vectors back to string
    """
    for i, col in enumerate(rdf.colnames):
        if R['is.factor'](rdf[i])[0]:
            rdf[i] = R['as.character'](rdf[i])


if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose=0)
