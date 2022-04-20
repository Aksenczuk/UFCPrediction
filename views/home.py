import streamlit as st
import pandas as pd
from PIL import Image
import pickle
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/fighter_stats.csv")
fighter_gender = pd.read_csv("datasets/fighter_gender.csv")
ensemble = pickle.load(open("resources/ensemble_model.pickle", 'rb'))

def load_view():
    # title
    st.markdown('''
        <h1 style='text-align: center; color: white;'>UFC Predictions</h1>
    ''', unsafe_allow_html=True )

    # subheader
    st.markdown('''
        <h3 style='text-align: center; color: white;'>Welcome to the UFC predictions app, please select 2 distinct fighters and select FIGHT!</h3>
    ''', unsafe_allow_html=True )

    main()

def weight_switch(weight_class):
   if weight_class == 'Heavyweight':
       return 205, 265
   elif weight_class == 'Light Heavyweight':
       return 185, 205
   elif weight_class == 'Middleweight':
       return 170, 185
   elif weight_class == 'Welterweight':
       return 155, 170
   elif weight_class == 'Lightweight':
       return 145, 155
   elif weight_class == 'Featherweight':
       return 135, 145
   elif weight_class == 'Bantamweight':
       return 125, 135
   elif weight_class == 'Flyweight':
       return 115, 125
   elif weight_class == "Women's Featherweight":
       return 135, 145
   elif weight_class == "Women's Bantamweight":
       return 125, 135
   elif weight_class == "Women's Flyweight":
       return 115, 125
   elif weight_class == "Women's Strawweight":
       return 0, 115

def prediction(sample):
     prediction = ensemble.predict_proba(sample)
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

def tale_of_the_tape(R, B):
    # values for tale of the tape
    r_wins = int(df.query(f'fighter == "{R}"')[["wins"]].iloc[0])
    b_wins = int(df.query(f'fighter == "{B}"')[["wins"]].iloc[0])
    r_losses = int(df.query(f'fighter == "{R}"')[["losses"]].iloc[0])
    b_losses = int(df.query(f'fighter == "{B}"')[["losses"]].iloc[0])
    r_height = round(float(df.query(f'fighter == "{R}"')[["Height_cms"]].iloc[0]), 2)
    b_height = round(float(df.query(f'fighter == "{B}"')[["Height_cms"]].iloc[0]), 2)
    r_reach = float(df.query(f'fighter == "{R}"')[["Reach_cms"]].iloc[0])
    b_reach = float(df.query(f'fighter == "{B}"')[["Reach_cms"]].iloc[0])
    r_weight = float(df.query(f'fighter == "{R}"')[["Weight_lbs"]].iloc[0])
    b_weight = float(df.query(f'fighter == "{B}"')[["Weight_lbs"]].iloc[0])
    r_age = int(df.query(f'fighter == "{R}"')[["age"]].iloc[0])
    b_age = int(df.query(f'fighter == "{B}"')[["age"]].iloc[0])

    # df creation
    new_data = {f"{r_wins}": [r_losses, r_height, r_reach, r_weight, r_age], 
    "Wins": ["Losses", "Height (cm)", "Reach (cm)", "Weight (lbs)", "Age"],
    f"{b_wins}": [b_losses, b_height, b_reach, b_weight, b_age]}

    taleOfTheTapeDF = pd.DataFrame(new_data)
        
    st.markdown('''<style> 
    tbody th {display:none}
    .blank {display:none}
    tbody td,th,table {background: black; color: white; text-align: center;}
    </style>''', unsafe_allow_html=True)

    fig, ax = plt.subplots() 
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight') 
    ax.table(cellText=taleOfTheTapeDF.values, colLabels=taleOfTheTapeDF.columns, loc='center', cellLoc="center") 
    fig.tight_layout()
    st.pyplot(fig)

def main():
    weight_class = st.selectbox("Weight Class", ('Heavyweight', 'Light Heavyweight', 'Middleweight', 'Welterweight', 
    'Lightweight', 'Featherweight', 'Bantamweight', 'Flyweight', "Women's Featherweight", "Women's Bantamweight", 
    "Women's Flyweight", "Women's Strawweight"))
    st.text("")

    # weight_class filter
    min_weight, max_weight = weight_switch(weight_class)
    fighters = df.query(f"Weight_lbs > {min_weight} & Weight_lbs <= {max_weight}")[["fighter"]]

    # gender filter
    for fighter in fighters["fighter"]:
        gender = str(fighter_gender.query(f'fighter == "{fighter}"')[["gender"]].iloc[0])
        if "Women" in weight_class:
            if "FEMALE" not in gender:
                fighters.drop(fighters.loc[fighters["fighter"] == fighter].index, inplace=True)
        else:
            if "FEMALE" in gender:
                fighters.drop(fighters.loc[fighters["fighter"] == fighter].index, inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        r_fighter = st.selectbox("Red Fighter", fighters)
        st.text("")
        img = Image.open('img/fighter_left_new.png')
        st.image(img, use_column_width=True)
    with col2:
        b_fighter = st.selectbox("Blue Fighter", fighters)
        st.text("")
        img = Image.open('img/fighter_right_new.png')
        st.image(img, use_column_width=True)

    if r_fighter != b_fighter:
        tale_of_the_tape(r_fighter, b_fighter)

    col1,col2,col3=st.columns([0.2,1.8,0.2])
    with col1:
        st.empty()
    with col2:
        st.markdown(''' <style> .stButton>button {background-color: #FF3030;color:white;font-size:20px;height:3em;width:30em;border-radius:10px 10px 10px 10px; .center {display: block; margin-left: auto;margin-right: auto;}} </style>
        ''', unsafe_allow_html=True) 
        submitBtn = st.button("FIGHT!")
    with col3:
        st.empty()
  
    if(submitBtn):
        if r_fighter == b_fighter:
            st.error("Please select 2 different fighters")
      
        else:
            r_id = df["ID"][df["fighter"]==r_fighter].values[0]
            b_id = df["ID"][df["fighter"]==b_fighter].values[0]
            fight = createMatch(r_id, b_id)
            winner = prediction(fight).tolist()[0]
            r_proba = round(winner[0],2) * 100
            b_proba = round(winner[1],2) * 100
            winner_message = f"{r_fighter} has {r_proba}% & {b_fighter} has {b_proba}% chances to win"
            st.success(winner_message)

    # pseudo footer
    st.markdown('''
        <h3 style='text-align: center; color: white;'>View upcoming UFC events <a href="https://www.ufc.com/events">here</a></h3>
    ''', unsafe_allow_html=True)