import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 100)

df = pd.read_csv("datasets/UFC_processed.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.drop(columns = "Winner")

features = ["date","fighter"]
for name in df.columns[3:26]: # slice to get rid of R_ & B_
    features.append(name[2:])

# separate fighters
rFighter = pd.concat([df.iloc[:,[0,1]],df.iloc[:,26:]],axis=1)
bFighter = pd.concat([df.iloc[:,[0,2]],df.iloc[:,3:26]],axis=1)

# apply slicing
rFighter.columns = features
bFighter.columns = features

# rFighter & bFighter concat in one dataframe
fighters = pd.concat([rFighter,bFighter],axis=0,).reset_index(drop=True)

# group to get details from fighters latest fight
groupedFighter = fighters.groupby("fighter")

# create list which only contains each fighters latest fight statistics
fighters_detail = []
for fighter in fighters["fighter"].unique(): 
    fighters_detail.append(groupedFighter.get_group(fighter).sort_values(by=["date"],ascending=False).iloc[0])

fighter_stat = pd.DataFrame(fighters_detail).sort_values(by="fighter")
fighter_stat.insert(0, 'ID', np.arange(1,len(fighter_stat.index)+1))
fighter_stat.reset_index(drop=True, inplace=True)

# export dataset
fighter_stat.to_csv("datasets/fighter_stats.csv",index=False)