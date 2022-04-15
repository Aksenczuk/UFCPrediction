from cProfile import label
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
np.random.seed(SEED)
pd.set_option("display.max_columns", 500)
pd.set_option("display.max_rows", 50)

df = pd.read_csv("datasets/ufc-master.csv")
print(df.shape)

df = df[df.columns.drop(list(df.filter(regex="odds")))]
df = df[df.columns.drop(list(df.filter(regex="ev")))]
df = df[df.columns.drop(list(df.filter(regex="_rank")))]
df = df[df.columns.drop(list(df.filter(regex="finish")))]		
df = df[df.columns.drop(list(df.filter(regex="total_fight_time_secs")))]
df = df[df.columns.drop(list(df.filter(regex="dif")))]	
df = df[df.columns.drop(list(df.filter(regex="constant_1")))]	
df = df[df.columns.drop(list(df.filter(regex="empty_arena")))]
df = df[df.columns.drop(list(df.filter(regex="location")))]
df = df[df.columns.drop(list(df.filter(regex="title_bout")))]
df = df[df.columns.drop(list(df.filter(regex="gender")))]
df = df[df.columns.drop(list(df.filter(regex="country")))]
df = df[df.columns.drop(list(df.filter(regex="no_of_rounds")))]	
df = df[df.columns.drop(list(df.filter(regex="weight_class")))]				

df["date"] = pd.to_datetime(df["date"]) # date to datetime

df = df.replace(r'^\s*$', np.nan, regex=True) # replace empty strings with NaN
df = df.fillna(np.nan) # fill empty and Na with NaN

dateColumn = df.pop('date')
df.insert(0, 'date', dateColumn)

df.rename(columns = { "B_win_by_KO/TKO": "B_win_by_KO_TKO", "R_win_by_KO/TKO": "R_win_by_KO_TKO"}, inplace=True)

print(df.describe())

categorical_data = list(df.select_dtypes(include=["object"]))
numeric_data = df.columns.tolist()
for x in categorical_data:
    numeric_data.remove(x)
print(f"\nCategoricals {len(categorical_data)}")
print(f"# Numerics {len(numeric_data)}")

df = df.dropna()

# missing data
missing = round(df.isnull().sum()/df.shape[0]*100,2)
print(f"\n% Missing in {len(missing[missing > 0])} Features:\n{missing[missing > 0]}")

# label encode fighters stances
labelmaker = LabelEncoder()
df["R_Stance"] = labelmaker.fit_transform(df["R_Stance"])
df["B_Stance"] = labelmaker.fit_transform(df["B_Stance"])

# reorder columns
B_age = df.pop("B_age")
df.insert(26, "B_age", B_age)	

df["Winner"] = df["Winner"].replace(["Red", "Blue"], [0,1]).values # 0 = Red Winner | 1 = Blue Winner

# shuffle data
df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

# split 5% from data as test set
test_rows = np.arange(0,0.05*len(df.index))
ufc_test = df.iloc[test_rows].reset_index(drop=True)

# other 95% will be training set for models
ufc_train = df.drop(test_rows, inplace=False, axis=0) # remove test set from dataset
ufc_train.reset_index(drop=1, inplace=True)

print(f"df shape: {df.shape}")
print(f"ufc_test shape: {ufc_test.shape}")
print(f"ufc_train shape: {ufc_train.shape}")
print("--------------------------------")
print(df.info())
print("--------------------------------")
df.head()

# export datasets
df.to_csv("datasets/ufc_processed.csv",index=False)
ufc_test.to_csv("datasets/ufc_test.csv",index=False)
ufc_train.to_csv("datasets/ufc_train.csv",index=False) 