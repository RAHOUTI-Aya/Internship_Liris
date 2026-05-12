# app.py

import streamlit as st

st.title("Test Streamlit")

name = st.text_input("Ton nom")

if name:
    st.success(f"Bonjour {name} !")

number = st.slider("Choisis un nombre", 0, 100, 50)

st.write("Valeur choisie :", number)