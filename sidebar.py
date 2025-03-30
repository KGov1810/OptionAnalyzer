import streamlit as st


class Sidebar:
    """Sidebar management"""
    def __init__(self):
        self.page = {
            "Option Analyzer": [
                st.Page("windows/home.py", title="Home"),
            ],
            "Models": [
                st.Page("windows/blackscholes.py", title="Black Scholes"),
                st.Page("windows/dupire.py", title="Dupire"),
                st.Page("windows/heston.py", title="Heston"),
            ],
        }