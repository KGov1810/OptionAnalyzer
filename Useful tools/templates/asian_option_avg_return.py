import numpy as np

class AsianOptionAverageReturn:
    def __init__(self, returns, averaging_days, strike_start, strike_end):
        """
        Initialize the Asian option based on cumulative returns.
        
        :param returns: List or numpy array of daily returns.
        :param averaging_days: Number of days used for averaging the spot return.
        :param strike_start: Start day for strike return calculation.
        :param strike_end: End day for strike return calculation.
        """
        self.returns = np.array(returns)
        self.averaging_days = averaging_days
        self.strike_start = strike_start
        self.strike_end = strike_end
        
        if len(self.returns) < max(self.averaging_days, self.strike_end):
            raise ValueError("Not enough data to compute the required averages.")
    
    def compute_average_return(self, start, end):
        """Compute the average return over the specified period."""
        return np.mean(self.returns[start:end])
    
    def compute_payoff(self):
        """Compute the Asian option payoff comparing spot and strike average returns."""
        avg_spot_return = self.compute_average_return(-self.averaging_days, None)
        avg_strike_return = self.compute_average_return(self.strike_start, self.strike_end)
        return max(avg_spot_return - avg_strike_return, 0)

# Random return simulation
def simulate_returns(days, volatility=1, drift=0):
    """Generate simulated daily returns using a normal distribution."""
    return np.random.normal(drift, volatility / 100, days)

# Example Usage
np.random.seed(42)  # For reproducibility
returns = simulate_returns(60, volatility=2, drift=0.05)  # Simulated daily returns
asian_option = AsianOptionAverageReturn(returns, averaging_days=30, strike_start=10, strike_end=20)
print("Asian Option Payoff (Average Return):", asian_option.compute_payoff())
