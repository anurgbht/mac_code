# %%
import matplotlib.pylab as plt
import numpy as np
import os
import pandas as pd
import ptitprince as pt
import seaborn as sns
sns.set(style="whitegrid",font_scale=2)

# %%
N_size = 250
sce1 = [int(np.random.normal(loc=40, scale=5)) for x in range(N_size)]
sce2 = [int(np.random.normal(loc=32, scale=5)) for x in range(N_size)]
df = {
    "Scenario": ['1' for x in sce1] + ['2' for x in sce2],
    "Casualities": sce1 + sce2
}

df = pd.DataFrame(df)
df.head()


# %%
# plotting the clouds
f, ax = plt.subplots(figsize=(7, 5))
dy = "Scenario"
dx = "Casualities"
ort = "h"
pal = sns.color_palette(n_colors=1)
ax = pt.half_violinplot(x=dx,
                        y=dy,
                        data=df,
                        palette=pal,
                        bw=.2,
                        cut=0.,
                        scale="area",
                        width=.6,
                        inner=None,
                        orient=ort)
plt.title("Figure P2\n Basic Rainclouds")

# %%
# adding the rain
f, ax = plt.subplots(figsize=(7, 5))
ax = pt.half_violinplot(x=dx,
                        y=dy,
                        data=df,
                        palette=pal,
                        bw=.2,
                        cut=0.,
                        scale="area",
                        width=.6,
                        inner=None,
                        orient=ort)
ax = sns.stripplot(x=dx,
                   y=dy,
                   data=df,
                   palette=pal,
                   edgecolor="white",
                   size=3,
                   jitter=0,
                   zorder=0,
                   orient=ort)
plt.title("Figure P3\n Raincloud Without Jitter")

# %%
# adding jitter to the rain
f, ax = plt.subplots(figsize=(7, 5))
ax = pt.half_violinplot(x=dx,
                        y=dy,
                        data=df,
                        palette=pal,
                        bw=.2,
                        cut=0.,
                        scale="area",
                        width=.6,
                        inner=None,
                        orient=ort)
ax = sns.stripplot(x=dx,
                   y=dy,
                   data=df,
                   palette=pal,
                   edgecolor="white",
                   size=3,
                   jitter=1,
                   zorder=0,
                   orient=ort)
plt.title("Figure P4\n Raincloud with Jittered Data")

# %%
#adding the boxplot with quartiles
f, ax = plt.subplots(figsize=(7, 5))
ax = pt.half_violinplot(x=dx,
                        y=dy,
                        data=df,
                        palette=pal,
                        bw=.2,
                        cut=0.,
                        scale="area",
                        width=.6,
                        inner=None,
                        orient=ort)
ax = sns.stripplot(x=dx,
                   y=dy,
                   data=df,
                   palette=pal,
                   edgecolor="white",
                   size=3,
                   jitter=1,
                   zorder=0,
                   orient=ort)
ax = sns.boxplot(x=dx,
                 y=dy,
                 data=df,
                 color="black",
                 width=.15,
                 zorder=10,
                 showcaps=True,
                 boxprops={
                     'facecolor': 'none',
                     "zorder": 10
                 },
                 showfliers=True,
                 whiskerprops={
                     'linewidth': 2,
                     "zorder": 10
                 },
                 saturation=1,
                 orient=ort)
plt.title("Figure P5\n Raincloud with Boxplot")

# %%
#adding color
pal = "Set2"
f, ax = plt.subplots(figsize=(7, 5))
ax = pt.half_violinplot(x=dx,
                        y=dy,
                        data=df,
                        palette=pal,
                        bw=.2,
                        cut=0.,
                        scale="area",
                        width=.6,
                        inner=None,
                        orient=ort)
ax = sns.stripplot(x=dx,
                   y=dy,
                   data=df,
                   palette=pal,
                   edgecolor="white",
                   size=3,
                   jitter=1,
                   zorder=0,
                   orient=ort)
ax = sns.boxplot(x=dx,
                 y=dy,
                 data=df,
                 color="black",
                 width=.15,
                 zorder=10,
                 showcaps=True,
                 boxprops={
                     'facecolor': 'none',
                     "zorder": 10
                 },
                 showfliers=True,
                 whiskerprops={
                     'linewidth': 2,
                     "zorder": 10
                 },
                 saturation=1,
                 orient=ort)
plt.title("Comparision of casualities")

# %%
import plotly.express as px
# This dataframe has 244 lines, but 4 distinct values for `day`
df = px.data.tips()
fig = px.pie(df, values='tip', names='day')
fig.show()

# %%



