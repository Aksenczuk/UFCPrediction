import streamlit as st
from streamlit.components.v1 import html
from resources.paths import NAVIGATION

def injectCustomCSS():
    with open('resources/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def getCurrentRoute():
    try:
        return st.experimental_get_query_params()['nav'][0]
    except:
        return None

def navigationbarComponent():
    navigationbarItems = ''
    for key, value in NAVIGATION.items():
        navigationbarItems += f'<a class="navitem" href="/?nav={value}">{key}</a>'
    
    component = rf'''
            <nav class="container navbar" id="navbar">
                <ul class="navlist">
                    {navigationbarItems}
                </ul>
            </nav>
            '''

    st.markdown(component, unsafe_allow_html=True)

    js = '''
    <script>
        var navigationTabs = window.parent.document.getElementsByClassName("navitem");
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target')}
        
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);}
    </script>'''
    html(js)