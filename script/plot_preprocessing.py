# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy import stats

# Morph_1 = pd.read_csv("preprocessing.csv", sep=',')
# print(Morph_1)
# print(Morph_1.columns)

# rice_varieties = Morph_1['Group_NJ'].value_counts().index[:3]

# def plot_qqplots(data, column_names):
#     num_plots = len(column_names)
#     rows = num_plots // 2 if num_plots % 2 == 0 else (num_plots // 2) + 1
#     cols = 2

#     fig, axes = plt.subplots(rows, cols, figsize=(14, 10))
#     fig.suptitle('Q-Q Plots', fontsize=16)
#     axes = axes.flatten()
    
#     for i, column in enumerate(column_names):
#         stats.probplot(data[column], dist="norm", plot=axes[i])
#         axes[i].set_title(f'Q-Q plot of {column}')
#         axes[i].grid(True)

#     for j in range(i+1, rows*cols):
#         fig.delaxes(axes[j])

#     plt.tight_layout(rect=[0, 0, 1, 0.96])
#     plt.show()

# def plot_boxplot(data, x, y, xlabel, ylabel, title):
#     plt.figure(figsize=(10, 6))
#     sns.boxplot(x=x, y=y, data=data, palette=["#00AFBB", "#E7B800", "#FC4E07"])
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     plt.xticks(fontsize=12)
#     plt.yticks(fontsize=12)
#     plt.tight_layout()
#     plt.show()

# rice_varieties = Morph_1['Group_NJ'].value_counts().index[:3]

# qq_columns = ['RTW', 'SHW', 'SHL', 'TTW', 'rSi_2508', 'rSi_0510']
# plot_qqplots(Morph_1, qq_columns)

# for variety in rice_varieties:
#     subset = Morph_1[Morph_1['Group_NJ'] == variety]

#     plot_boxplot(subset, 'Group_NJ', 'RTW', 'Group', 'Relative Root weight', f'Boxplot of RTW for {variety}')
#     plot_boxplot(subset, 'Group_NJ', 'SHW', 'Group', 'Relative Shoot weight', f'Boxplot of SHW for {variety}')
#     plot_boxplot(subset, 'Group_NJ', 'SHL', 'Group', 'Relative Shoot length', f'Boxplot of SHL for {variety}')
#     plot_boxplot(subset, 'Group_NJ', 'TTW', 'Group', 'Relative Total weight', f'Boxplot of TTW for {variety}')
#     plot_boxplot(subset, 'Group_NJ', 'rSi_2508', 'Group', 'rSi in 1st sampling', f'Boxplot of rSi_2508 for {variety}')
#     plot_boxplot(subset, 'Group_NJ', 'rSi_0510', 'Group', 'rSi in 2nd sampling', f'Boxplot of rSi_0510 for {variety}')
