import streamlit as st

def get_pic(selected):
    st.image(f'https://lil.noun.pics/{selected}.jpg')
