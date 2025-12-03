import os
import pandas as pd
from pathlib import Path
import plotly.express as px

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = Path(ROOT_DIR, "data")

if __name__ == "__main__":
    df = pd.read_csv(Path(DATA_DIR, "Crude suicide rates.csv"))
    
    int_col = [' 30to39',' 20to29']
    df.loc[:,'all_suicides'] = df.loc[:,int_col].sum(axis=1)
    df = df.sort_values(by='all_suicides')
    print(df.columns)

    fig = px.bar(df, x="Country", y='all_suicides', color="Sex")
    fig.show()
