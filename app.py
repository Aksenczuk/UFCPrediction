import streamlit as st
import resources.utility as util
from views import home, stats

util.injectCustomCSS()
util.navigationbarComponent()

def navigation():
    route = util.getCurrentRoute()
    if route == "statistics":
        stats.load_view()
    else:
        home.load_view()

navigation()

# background image
st.markdown('''
    <style>
        .stApp {
            background-image: url("https://i.pinimg.com/originals/56/13/94/56139409e837dd8d8319d6f39e6bf6d3.jpg");
            background-size: cover;
        }
    </style>
''', unsafe_allow_html=True)

hide_footer = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_footer, unsafe_allow_html=True)