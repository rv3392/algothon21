import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Cointegration_Results.csv", index_col=None)
df = 10 ** df

plt.title("Cointegration Between Pairs")
ax = sns.heatmap(data=df)
plt.show()

