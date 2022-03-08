from MyUtils.dataprocessing import DataProcessor
import pandas as pd
import numpy as np

# TODO- create better structure  + use unittest

path = 'MyUtils/Testing/Data'
##########
# test  .to (dynamic) method
##########
# create DataFrame


def create_df(rows=10, columns=5):
    return pd.DataFrame(np.random.rand(rows, columns), columns=range(columns))


df = create_df()
data = DataProcessor(path)

# df.to_csv(f'{path}/test_csv.csv')

# test writing
data.to_csv(df, 'test_csv', index=False)
data.to_pickle(df, 'test_pickle')
data.to_excel(df, 'test_excel', index=False)

# test opening
df = data.read_csv('test_csv')
df = data.read_pickle('test_pickle')
df = data.read_excel('test_excel')
