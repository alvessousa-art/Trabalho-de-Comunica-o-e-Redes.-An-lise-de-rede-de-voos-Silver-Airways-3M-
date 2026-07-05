import pandas as pd 
air = pd.read_csv("airlines.csv")
routes = pd.read_csv("routes.csv")

silverAirlines = air[air[air.columns[1]] == "Silver Airways (3M)"]
silverAirlinesIATA = silverAirlines.iloc[0, 3] 


print(air[air[air.columns[0]] == silverAirlinesIATA])