import numpy as np

class MonthlyAveragePayoff:
    def __init__(self, spot_prices, days_per_month):
        """
        Initialize the payoff calculation based on monthly averages.
        
        :param spot_prices: List or numpy array of spot prices over time.
        :param days_per_month: Number of days considered as one month.
        """
        self.spot_prices = np.array(spot_prices)
        self.days_per_month = days_per_month
        
        if len(self.spot_prices) < 2 * self.days_per_month:
            raise ValueError("Not enough data to compute two full months of averages.")
    
    def compute_average(self, start_day, end_day):
        """Compute the average price over the specified period."""
        return np.mean(self.spot_prices[start_day:end_day])
    
    def compute_payoff(self):
        """Compute the difference between the current month's average and the last month's average."""
        last_month_avg = self.compute_average(-2 * self.days_per_month, -self.days_per_month)
        current_month_avg = self.compute_average(-self.days_per_month, None)
        
        return max(current_month_avg - last_month_avg, 0)
        
# Random price simulation
def simulate_prices(initial_price, days, volatility=1, drift=0):
    """Generate simulated price data using a simple random walk."""
    prices = [initial_price]
    for _ in range(days - 1):
        prices.append(prices[-1] * (1 + np.random.normal(drift, volatility / 100)))
    return prices

# Example Usage
np.random.seed(48)  # For reproducibility
spot_prices = simulate_prices(100, 60, volatility=0.2, drift=0.05)  # Simulated price data
payoff_calc = MonthlyAveragePayoff(spot_prices, days_per_month=30)
print("Monthly Average Payoff:", payoff_calc.compute_payoff())

