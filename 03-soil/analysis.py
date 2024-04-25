import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

POLLUTANTS = []

def get_data():
    global POLLUTANTS
    df = pd.read_csv('xrf_data.csv')

    # Parse out sampling codes
    df['site'] = df['info'].str.split('_').str[0]
    df['coordinate'] = df['info'].str.split('_').str[1]
    df['depth'] = df['info'].str.split('_').str[2]

    # Grab relevant data
    cols = df.columns.astype(str).tolist()
    POLLUTANTS = [c for c in cols if 'Concentration' in c]
    col_filter = [c for c in cols if 'Concentration' in c or 'Error1s' in c]
    df[col_filter] = df[col_filter].apply(pd.to_numeric, errors='coerce') #cast to int

    df = df.sort_values(by=['site', 'depth', 'coordinate'])

    code_cols = [' Units', 'site', 'coordinate', 'depth', 'info']

    col_filter.extend(code_cols)
    df_filtered = df[col_filter]

    return df_filtered

def get_concentrations(df: pd.DataFrame):
    """
    Return a df with only concentrations.
    """
    cols = df.columns.astype(str).tolist()
    cols = [c for c in cols if 'Concentration' in c] + ['info']

    return df[cols]

def generate_plots(df: pd.DataFrame):
    """
    df has concentrations
    """
    sites = df['info']
    for p in POLLUTANTS:
        plt.figure()
        plt.rcParams["figure.figsize"] = (20, 10)
        plt.bar(sites, df[p])
        plt.title("{}".format(p))
        plt.xlabel("Site Code")
        plt.ylabel("Concentration (ppm)")
        plt.xticks(rotation=90)
        plt.savefig(f"out/{p.replace(' ', '_')}.png", bbox_inches='tight', dpi=300)
        plt.close()


def main():
    data = get_data()
    generate_plots(data)

if __name__ == '__main__':
    main()
