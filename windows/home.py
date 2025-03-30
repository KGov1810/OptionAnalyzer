import streamlit as st


class HomePage:
    """Home page display"""
    @staticmethod
    def display():
        st.title("Option Analysis")

        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Black-Scholes Model", type="primary", use_container_width=True):
                    st.switch_page("windows/blackscholes.py")
            with col2:
                with st.container(border=True):
                    st.write("The Black-Scholes model is a formula for pricing European options based on asset price, "
                             "volatility, time, and risk-free rate.")

        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Dupire Model", type="primary", use_container_width=True):
                    st.switch_page("windows/dupire.py")
            with col2:
                with st.container(border=True):
                    st.write("The Dupire model is a local volatility model that extends Black-Scholes by allowing "
                             "volatility to vary with both time and asset price, improving option pricing accuracy.")

        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Heston Model", type="primary", use_container_width=True):
                    st.switch_page("windows/heston.py")
            with col2:
                with st.container(border=True):
                    st.write("The Heston model is a stochastic volatility model that extends Black-Scholes by "
                             "allowing volatility to be random and mean-reverting, improving option pricing accuracy.")