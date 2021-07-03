import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm

df = pd.read_csv("prices250.txt", sep='\s+', header=None, index_col=None)
#corr_matrix = df.corr()
#print(corr_matrix)

# The following lines are to determine the p-values for cointegration of pairs of stocks
'''for j in range(50, 100):
    for i in range(0, 100):
        coint_result = ts.coint(df[j], df[i])
        if coint_result[1] < 0.01:
            print("{} and {}: ".format(j, i) + str(coint_result[1]))'''

# Estimate the beta term using linear regression OLS
ols_result = sm.OLS(df[51], df[70]).fit()
print(ols_result.summary())

# Portfolio is Stock Y = beta * Stock X
Y = 51
X = 70
beta = 0.6005

plt.title("Cointegration between stocks {} and {}".format(Y, X))
df[Y].plot()
(df[X]*beta).plot()
plt.legend(["Stock {}".format(Y), "{} * Stock {}".format(beta, X)])
plt.show()

plt.title("Stock {} - {} * Stock {}".format(Y, beta, X))
(df[Y] - df[X]*beta).plot()
plt.show()

'''plot_acf(df[51])
plot_pacf(df[51])
plt.show()'''


