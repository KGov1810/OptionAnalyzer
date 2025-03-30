import streamlit as st
from sidebar import Sidebar
from windows.home import HomePage
from windows.dupire import Dupire
from windows.heston import Heston
from windows.blackscholes import BlackScholes


class Main:
    def __init__(self):
        self.sidebar = Sidebar()

    def run(self):
        """Execute the application and display the selected page"""
        st.set_page_config(
            page_title="Option Analysis",
            page_icon=":chart_with_upwards_trend:",
        )
        selected_page = st.navigation(self.sidebar.page)
        if selected_page.title == "Black Scholes":
            BlackScholes().display()
        elif selected_page.title == "Dupire":
            Dupire.display()
        elif selected_page.title == "Heston":
            Heston.display()
        elif selected_page.title == "Home":
            HomePage.display()


if __name__ == "__main__":
    app = Main()
    app.run()
