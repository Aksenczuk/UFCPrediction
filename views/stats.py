import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/fighter_stats.csv")

def load_view():
    # title
    st.markdown('''
        <h1 style='text-align: center; color: white;'>Fighter Statistics</h1>
    ''', unsafe_allow_html=True )

    # subheader
    st.markdown('''
        <h3 style='text-align: center; color: white;'>Select a fighter to view their statistics in the UFC</h3>
    ''', unsafe_allow_html=True )

    main()

def createStatistics(colNames, colValues):
    for x in range(len(colNames)):
        colNames[x] = colNames[x].replace("_", " ").capitalize()

    newData = {colNames[0]: [colNames[1],colNames[2],colNames[3],colNames[4],colNames[5],
    colNames[6],colNames[7],colNames[8],colNames[9],colNames[10],colNames[11],colNames[12],colNames[13],
    colNames[14],colNames[15],colNames[16],colNames[17],colNames[18],colNames[19],colNames[20],colNames[21],
    colNames[22],colNames[23]], colValues[0]: [colValues[1],colValues[2],colValues[3],colValues[4],colValues[5],
    colValues[6],colValues[7],colValues[8],colValues[9],colValues[10],colValues[11],colValues[12],colValues[13],
    colValues[14],colValues[15],colValues[16],colValues[17],colValues[18],colValues[19],colValues[20],colValues[21],
    colValues[22],colValues[23]]}
    newDF = pd.DataFrame(newData)
    st.markdown('''<style> 
    tbody th {display:none}
    .blank {display:none}
    </style>''', unsafe_allow_html=True)

    fig, ax = plt.subplots() 
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight') 
    
    ax.table(cellText=newDF.values, colLabels=newDF.columns, loc='center', cellLoc="center") 
    fig.tight_layout()
    st.pyplot(fig)

def updateStance(stance):
    if stance == 1:
        return "Orthodox"
    elif stance == 2:
        return "Southpaw"
    elif stance == 3:
        return "Swtich"
    else:
        return "N/A"

def main():
    fighter = st.selectbox("Fighter", df["fighter"])
    fighterData = df.query(f"fighter == '{fighter}'")

    colNames = fighterData.columns.tolist()[2:]
    colValues = fighterData.values[0].tolist()[2:]
    colValues[19] = updateStance(colValues[19])
    createStatistics(colNames, colValues)