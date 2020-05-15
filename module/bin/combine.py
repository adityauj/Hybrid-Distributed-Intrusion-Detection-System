import numpy as np
import pandas as pd

np.seterr(divide='ignore', invalid='ignore')

benign = pd.read_csv("Benign.csv",low_memory=False,skipinitialspace=True, index_col=False)
goldeneye = pd.read_csv("GoldenEye.csv",low_memory=False,skipinitialspace=True, index_col=False)
hulk = pd.read_csv("Hulk.csv",low_memory=False,skipinitialspace=True, index_col=False)
heartbleed = pd.read_csv("Heartbleed.csv",low_memory=False,skipinitialspace=True, index_col=False)

dataset = pd.DataFrame()

dataset = pd.concat([benign, goldeneye, hulk, heartbleed], axis = 0)

dataset = dataset.reset_index()

dataset.to_csv('dataset.csv', index = False, sep=',')