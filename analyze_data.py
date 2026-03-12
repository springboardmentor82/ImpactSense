import pandas as pd
import numpy as np

def analyze_data():
    df = pd.read_csv('data/clean_earthquake_data.csv')
    
    # Print overall distribution
    print("--- Distribution ---")
    print(df['alert'].value_counts())
    print("\n")

    # Print representative values for each alert level
    for alert in ['green', 'yellow', 'orange', 'red']:
        print(f"--- {alert.upper()} STATS ---")
        subset = df[df['alert'] == alert]
        if not subset.empty:
            print(subset[['magnitude', 'depth', 'cdi', 'mmi', 'sig']].describe().loc[['min', 'mean', 'max']])
        else:
            print("No data available.")
        print("\n")

if __name__ == "__main__":
    analyze_data()
