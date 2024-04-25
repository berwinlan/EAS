import pandas as pd
import numpy as np

def get_data():
    data = pd.read_csv('xrf_data.csv')
    data['site'] = data['info'].str.split('_').str[0]
    data['coordinate'] = data['info'].str.split('_').str[1]
    data['depth'] = data['info'].str.split('_').str[2]
    return data

def main():
    data = get_data()
    print(data.head())

if __name__ == '__main__':
    main()
