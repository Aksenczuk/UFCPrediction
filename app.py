import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import pickle

# style CSS
st.markdown('''
    <style>
        .stApp {
            background-image: url("https://i.pinimg.com/originals/56/13/94/56139409e837dd8d8319d6f39e6bf6d3.jpg");
            background-size: cover;
        }
    </style>
''', unsafe_allow_html=True)

# title
st.markdown('''
    <h1 style='text-align: center; color: white;'>UFC Predictions</h1>
''', unsafe_allow_html=True)

# subheader
st.markdown('''
    <h3 style='text-align: center; color: white;'>Welcome to the UFC predictions app, please select 2 distinct fighters and select FIGHT!</h3>
''', unsafe_allow_html=True)

# spacer
st.markdown('#')

df = pd.read_csv("datasets/fighter_stats.csv")
fighter_gender = pd.read_csv("datasets/fighter_gender.csv")
ensemble = pickle.load(open("resources/ensemble_method.sav", 'rb'))

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

def main():
    st.text("")
    weight_class = st.selectbox("Weight Class", ('Heavyweight', 'Light Heavyweight', 'Middleweight', 'Welterweight', 'Lightweight', 'Featherweight', 'Bantamweight', 'Flyweight', "Women's Featherweight", "Women's Bantamweight", "Women's Flyweight", "Women's Strawweight"))
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

    st.text("")

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
            match_fighters = {
                0:str(r_fighter),
                1:str(b_fighter)
            }

            r_id = df["ID"][df["fighter"]==r_fighter].values[0]
            b_id = df["ID"][df["fighter"]==b_fighter].values[0]

            sample = createMatch(r_id, b_id)
            winner = prediction(sample).tolist()[0]
            winner_message = f"{r_fighter} has {round(winner[0],2)}% & {b_fighter} has {round(winner[1],2)}% chances to win"
            
            st.success(winner_message)

    st.write(" ")
    st.write(" ")

    # pseudo footer
    st.markdown('''
        <h3 style='text-align: center; color: white;'>View upcoming UFC events <a href="https://www.ufc.com/events">here</a></h3>
    ''', unsafe_allow_html=True)

# hide top part
#MainMenu {visibility: hidden;}
hide_footer = """
<style>
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()