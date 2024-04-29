import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

POLLUTANTS = []
ERRORS = []

LIMITS = dict()


def get_data():
    global POLLUTANTS, ERRORS
    df = pd.read_csv("xrf_data.csv")

    # Parse out sampling codes
    df["site"] = df["info"].str.split("_").str[0]
    df["coordinate"] = df["info"].str.split("_").str[1]
    df["depth"] = df["info"].str.split("_").str[2]

    # Grab relevant data
    cols = df.columns.astype(str).tolist()
    POLLUTANTS = [c for c in cols if "Concentration" in c]
    ERRORS = [c for c in cols if "Error1s" in c]
    col_filter = POLLUTANTS + ERRORS
    df[col_filter] = df[col_filter].apply(pd.to_numeric, errors="coerce")  # cast to int

    df = df.sort_values(by=["site", "depth", "coordinate"])

    code_cols = [" Units", "site", "coordinate", "depth", "info"]

    col_filter.extend(code_cols)
    df_filtered = df[col_filter]

    return df_filtered


def generate_plots(df: pd.DataFrame, debug=False):
    """
    Plot contaminant concentrations for all pollutants. Includes 1SD error bars.
    """
    sites = df["info"]

    for p, err in zip(POLLUTANTS, ERRORS):
        plt.figure()
        plt.rcParams["figure.figsize"] = (20, 10)

        # Plot data and error bars
        plt.bar(sites, df[p])
        plt.errorbar(
            sites, df[p], df[err], ecolor="r", barsabove=True, fmt="r.", markersize=1
        )

        # Add an hline for EPA limits if specified
        try:
            lim = LIMITS[p]
            plt.axhline(y=lim)
        except KeyError:
            pass

        # Style plot
        plt.title(str(p))
        plt.xlabel("Site Code")
        plt.ylabel("Concentration (ppm)")
        plt.xticks(rotation=90)

        if debug:
            plt.show()
        else:
            # Save plot
            plt.savefig(f"out/{p.replace(' ', '_')}.png", bbox_inches="tight", dpi=300)
            plt.close()


def main():
    data = get_data()
    generate_plots(data)


if __name__ == "__main__":
    main()
