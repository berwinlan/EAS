import pandas as pd
import numpy as np

def get_data():
    df = pd.read_csv('xrf_data.csv')

    # Parse out sampling codes
    df['site'] = df['info'].str.split('_').str[0]
    df['coordinate'] = df['info'].str.split('_').str[1]
    df['depth'] = df['info'].str.split('_').str[2]

    # Grab relevant data
    cols = df.columns.astype(str).tolist()
    col_filter = [c for c in cols if 'Concentration' in c or 'Error1s' in c]

    code_cols = [' Units', 'site', 'coordinate', 'depth', 'info']

    cols = df.columns.astype(str).tolist()
    df_filtered = df[col_filter.extend(code_cols)]
    df_filtered.head()

    return df

def main():
    data = get_data()
    print(data.head())

if __name__ == '__main__':
    main()
