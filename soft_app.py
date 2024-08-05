import streamlit as st
from soft_predict import show_predict_page
from soft_explore import show_explore_page

page = st.sidebar.selectbox('Explore Or Predict', ("Predict", "Explore"))

if page == 'Predict':
    show_predict_page()
else:
    show_explore_page()
