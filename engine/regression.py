import statsmodels.api as sm
from sklearn import linear_model


def regression(y, x):
    y = y.interpolate()
    x = sm.add_constant(x)
    res = sm.OLS(y, x).fit()
    return res


def sk_regression(y, x):
    y = y.interpolate()
    x = sm.add_constant(x)
    res = linear_model.LinearRegression().fit(x, y)
    return res


# def CAMPs(portfolios, factors):
#     res = []
#     for portfolio in portfolios:
#         res += [linregress(portfolio, factors)]
#     return res
