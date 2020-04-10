import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def drawMatrix(name):
    obj = pd.read_csv(name)
    obj = obj.dropna()
    plt.figure(figsize=(12.8, 7.2), dpi=600)
    tmap_plot = sns.heatmap(obj.drop(
        ['Tags/Difficult '], 1), yticklabels=obj['Tags/Difficult '], annot=True, annot_kws={"size": 4}, linewidths=0.05, fmt='d', cmap="YlGnBu",)
    tmap_plot.set_title(name)
    plt.savefig('./%s.png' % name, bbox_inches='tight')


drawMatrix('./Matrix_AC_Tags.csv')
drawMatrix('./Matrix_Count_Tags.csv')
