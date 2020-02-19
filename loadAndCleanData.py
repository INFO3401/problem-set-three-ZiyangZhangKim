import pandas as pd
def loadAndCleanData():
    item = pd.read_csv("creditData.csv")
    data = item.fillna(0)
    print(data)
loadAndCleanData()

