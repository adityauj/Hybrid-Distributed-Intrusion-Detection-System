#converts the 


import pandas as pd
import requests
import json

'''
csv_file = pd.DataFrame(pd.read_csv("/home/rahul/module/bin/data/daily/2019-04-04_Flow.csv", sep = ",", header = 0, index_col = False))
cols = list(csv_file.columns.values)
csv_file.to_json("parsed.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)

#data = pd.read_json("parsed.json")
with open('parsed.json') as json_file:  
    data = json.load(json_file)


data = data[:15]

df = pd.DataFrame(data)
df = df.reindex(columns=cols)

data.append(cols)
'''
data = {
    "IP": "192.168.15.1", 
    "message": "ATTACK DETECTED",
    
}

r = requests.post(url = "http://127.0.0.1:8002/log/logs", json = data) 

dataset = pd.read_csv('reduced.csv', low_memory=False, skipinitialspace=True)
dataset = dataset[0:15]
cols = list(dataset.columns.values)
dataset.to_json("parsed.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)

with open('parsed.json') as json_file:  
    data = json.load(json_file)


data.append(cols)
r = requests.post(url = "http://127.0.0.1:8002/detect/attack", json = data) 

if r:
    print("True")

dataframe = pd.DataFrame(data)
dataframe = dataframe.reindex(columns=cols)



