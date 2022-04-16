import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 100)

df = pd.read_csv("datasets/UFC_processed.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.drop(columns = "Winner")

# move gender so it dosnt affect slicing
gender = df.pop("gender")
df.insert(1, "gender", gender)	

features = ["date","gender", "fighter"]
for name in df.columns[4:27]: # slice to get rid of R_ & B_
    features.append(name[2:])

# separate fighters
rFighter = pd.concat([df.iloc[:,[0,1,2]],df.iloc[:,27:]],axis=1)
bFighter = pd.concat([df.iloc[:,[0,1,3]],df.iloc[:,4:27]],axis=1)

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

fighter_gender = fighter_stat[["fighter", "gender"]]

# drop gender
fighter_stat = fighter_stat[fighter_stat.columns.drop(list(fighter_stat.filter(regex="gender")))]

# export dataset
fighter_gender.to_csv("datasets/fighter_gender.csv",index=False)
fighter_stat.to_csv("datasets/fighter_stats.csv",index=False)