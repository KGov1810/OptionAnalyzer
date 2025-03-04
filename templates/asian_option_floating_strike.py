import numpy as np

class OptionAsianFloatingStrike:
    def __init__(self, prices, window, avg_type='arithmetic'):
        """
        Initialize the option with price data and the moving average window.

        :param prices: List or numpy array of underlying asset prices over time.
        :param window: Lookback period for the strike calculation (floating strike).
        :param avg_type: Type of average to use ('arithmetic', 'geometric', 'harmonic', 'quadratic', 'median', 'trimmed', 'ema', 'weighted').
        """
        self.prices = np.array(prices)
        self.window = min(window, len(self.prices))  # Handle cases where window > number of observations
        self.avg_type = avg_type
    
    def calculate_floating_strike(self):
        """
        Compute the floating strike using the specified averaging method.
        
        :return: The computed strike price.
        """
        prices_window = self.prices[-self.window:]
        
        if self.avg_type == 'arithmetic':
            return np.mean(prices_window)
        elif self.avg_type == 'geometric':
            return np.exp(np.mean(np.log(prices_window)))
        elif self.avg_type == 'harmonic':
            return len(prices_window) / np.sum(1.0 / prices_window)
        elif self.avg_type == 'quadratic':
            return np.sqrt(np.mean(np.square(prices_window)))
        elif self.avg_type == 'median':
            return np.median(prices_window)
        elif self.avg_type == 'trimmed':
            return np.mean(prices_window[int(0.1 * len(prices_window)):int(0.9 * len(prices_window))])
        elif self.avg_type == 'ema':
            alpha = 2 / (self.window + 1)  # Standard EMA smoothing factor
            ema = prices_window[0]
            for price in prices_window[1:]:
                ema = alpha * price + (1 - alpha) * ema
            return ema
        elif self.avg_type == 'weighted':
            weights = np.arange(1, len(prices_window) + 1)
            return np.average(prices_window, weights=weights)
        else:
            raise ValueError("Invalid average type. Choose 'arithmetic', 'geometric', 'harmonic', 'quadratic', 'median', 'trimmed', 'ema', or 'weighted'.")
    
    def payoff(self):
        """
        Compute the option payoff based on the floating strike.
        
        :return: The payoff value.
        """
        floating_strike = self.calculate_floating_strike()
        spot_final = self.prices[-1]  # Last spot price
        return max(spot_final - floating_strike, 0)

# Example usage
prices = [100, 102, 101, 103, 105, 107, 106, 108, 110, 109]
option = OptionAsianFloatingStrike(prices, window=30, avg_type='median')
print("Payoff:", option.payoff())



