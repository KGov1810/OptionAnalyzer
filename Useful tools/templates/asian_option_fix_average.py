import numpy as np

class AsianOptionPayoff:
    def __init__(self, spot_prices, start_day, end_day, option_type='call', strike_type='floating_strike'):
        """
        Initialize the Asian option.
        
        :param spot_prices: List or numpy array of spot prices over time.
        :param start_day: The first day included in the averaging period.
        :param end_day: The last day included in the averaging period (before maturity).
        :param option_type: 'call' or 'put'.
        :param strike_type: 'floating_strike' (strike is averaged) or 'floating_spot' (spot is averaged)
        """
        self.spot_prices = np.array(spot_prices)
        self.start_day = start_day
        self.end_day = end_day
        self.option_type = option_type.lower()
        self.strike_type = strike_type.lower()
        
        if self.option_type not in ['call', 'put']:
            raise ValueError("Invalid option type. Must be 'call' or 'put'.")
        if self.strike_type not in ['floating_strike', 'floating_spot']:
            raise ValueError("Invalid strike type. Must be 'floating_strike' or 'floating_spot'.")
        if not (0 <= self.start_day < self.end_day <= len(self.spot_prices)):
            raise ValueError("Invalid start and end day range.")
    
    def compute_average(self):
        """Compute the average price over the specified period."""
        return np.mean(self.spot_prices[self.start_day:self.end_day])
    
    def compute_payoff(self):
        """Compute the option payoff based on the strike price and averaging method."""
        average_price = self.compute_average()
        
        if self.strike_type == 'floating_strike':
            strike = average_price
            spot = self.spot_prices[-1]  # Final spot price
        else:  # 'floating_spot'
            strike = self.spot_prices[-1]  # Final spot price
            spot = average_price
        
        if self.option_type == 'call':
            return max(spot - strike, 0)
        elif self.option_type == 'put':
            return max(strike - spot, 0)