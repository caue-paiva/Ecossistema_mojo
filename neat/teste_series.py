import pandas as pd 

Se= pd.read_json("teste.json", typ= pd.Series, dtype=int)

#Se["index3"] = Se["index3"] +1
#Se = pd.read_csv("series.csv")

#Se = pd.Series(Se)

print(8 in Se)

"""if "index3" in Se:
    Se["index3"] = (Se["index3"] +8)/2
else:
    Se["index3"] = 8
Se["index1"] = (Se["index1"] + 10)/2"""


print(Se)

Se.to_json("teste.json")