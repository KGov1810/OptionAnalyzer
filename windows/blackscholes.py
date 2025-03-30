import numpy as np
import streamlit as st
from scipy.stats import norm
from config import CONFIG


class BlackScholes:
    """Black Scholes page display"""
    def __init__(self):
        self.s0 = np.nan
        self.sigma = np.nan
        self.k = np.nan
        self.r = np.nan
        self.t = np.nan
        self.d1 = np.nan
        self.d2 = np.nan
        self.option_type = ""
        self.option_position = ""

    def display(self):
        st.title("Black Scholes")

        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                self.s0 = st.number_input("Spot ($)", value=100)
                self.sigma = st.number_input("Implied Volatility (%)", value=20.0)
            with col2:
                self.k = st.number_input("Strike ($)", value=110)
            with col3:
                self.r = st.number_input("Risk-free Rate (%)", value=5.0)
                self.t = st.number_input("Maturity (Years)", value=1.0)

        with st.container(border=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                self.option_type = st.segmented_control("Option Type",
                                                        options=CONFIG.OPTION_TYPE.keys(),
                                                        format_func=lambda option: CONFIG.OPTION_TYPE[option],
                                                        selection_mode="single")
            with col2:
                self.option_position = st.segmented_control("Option Position",
                                                            options=CONFIG.OPTION_POSITION.keys(),
                                                            format_func=lambda option: CONFIG.OPTION_POSITION[option],
                                                            selection_mode="single")

        if ((self.t is not None) & (self.s0 is not None) & (self.sigma is not None) & (self.k is not None) &
                (self.r is not None)):
            self.calculate_d1_d2()

        if st.button("Calculate"):
            if CONFIG.OPTION_TYPE[self.option_type] == "CALL":
                price = self.calculate_call_price()
                if CONFIG.OPTION_POSITION[self.option_position] == "SHORT":
                    price = -price
                st.write(price)
            elif CONFIG.OPTION_TYPE[self.option_type] == "PUT":
                price = self.calculate_put_price()
                if CONFIG.OPTION_POSITION[self.option_position] == "SHORT":
                    price = -price
                st.write(price)


    def calculate_d1_d2(self):
        """
        Function to calculate d1 and d2 in the black scholes formula
        """
        if self.t > 0:
            self.d1 = (np.log(self.s0 / self.k) +
                       (self.r + 0.5 * self.sigma**2) * self.t) / (self.sigma * np.sqrt(self.t))
            self.d2 = self.d1 - self.sigma * np.sqrt(self.t)

    def calculate_call_price(self):
        """
        Function to calculate the price of the call
        """
        if np.isnan(self.d1):
            return max(0.0, self.s0 - self.k)

        return self.s0 * norm.cdf(self.d1) - self.k * np.exp(-self.r * self.t) * norm.cdf(self.d2)

    def calculate_put_price(self):
        """
        Function to calculate the price of the put
        """
        if np.isnan(self.d1):
            return max(0.0, self.k - self.s0)

        return self.k * np.exp(-self.r * self.t) * norm.cdf(-self.d2) - self.s0 * norm.cdf(-self.d1)
