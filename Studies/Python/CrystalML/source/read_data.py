import pandas as pd
from pathlib import Path
from config import N_SG, INPUT_DIR, OUTPUT_DIR, INTERESTING_COLUMNS, CUBIC

def read_xlsx(fpath):
    df = pd.read_excel(fpath)
    return df

def modify_df(df, cubic):
    modified_df = df[INTERESTING_COLUMNS]
    if cubic:
        modified_df = modified_df[modified_df.alpha == 90].reset_index(drop=1)
        modified_df = modified_df[modified_df.beta == 90].reset_index(drop=1)
        modified_df = modified_df[modified_df.gamma == 90].reset_index(drop=1)

    ## take the only top N_SG values
    value_counts = dict(modified_df.sg.value_counts())
    SG_to_model = list(value_counts.keys())[:N_SG]

    modified_df = modified_df[modified_df.sg.isin(SG_to_model)].reset_index(drop=1)
    modified_df.to_excel(Path(OUTPUT_DIR,f'data_to_model_{cubic}_{N_SG}.xlsx'))

if __name__ == "__main__":
    fpath = Path(INPUT_DIR,'Data.xlsx')
    raw_df = read_xlsx(fpath)
    modify_df(raw_df, cubic = CUBIC)