import streamlit as st

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.title('Мое первое приложение')
    if st.button('Hello, World!', use_container_width=True):
        st.balloons()
