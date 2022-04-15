import pandas as pd
import pickle

df = pd.read_csv("datasets/fighter_stats.CSV")
fighters = df["fighter"].tolist()
ensemble_method = pickle.load(open("resources/ensemble_method.sav", 'rb'))

def prediction(sample):
    prediction = ensemble_method.predict(sample)
    return prediction

def createMatch(R, B):
    rFighter = df[df["ID"] == R].iloc[:,3:]
    rFighter.columns = ['R_'+ col for col in rFighter.columns] # concat prefix B_ and rename columns

    bFighter = df[df["ID"] == B].iloc[:,3:]
    bFighter.columns = ['B_'+ col for col in bFighter.columns] 

    rFighter.reset_index(drop=True,inplace=True)
    bFighter.reset_index(drop=True,inplace=True)

    fight = pd.concat([rFighter,bFighter],axis=1).values
    return (fight)

r_fighter = "Israel Adesanya"
b_fighter = "Livinha Souza"

r_id = df["ID"][df["fighter"]==r_fighter].values[0]
b_id = df["ID"][df["fighter"]==b_fighter].values[0]

sample = createMatch(r_id, b_id)
prediction = prediction(sample).tolist()[0]

print(prediction)