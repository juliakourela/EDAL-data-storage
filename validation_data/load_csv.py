import pandas as pd

filename = 'dpfcgroundtruth_massachusetts.csv'

def to_dataframe(filename):
    return pd.read_csv(filename)


df = to_dataframe(filename)
print(df)

print(df.columns)

