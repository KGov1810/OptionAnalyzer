import numpy as np

class OptionAsianMovingAverage:
    def __init__(self, prices, short_window, long_window):
        """
        Initialize the option with price data and moving average windows.

        :param prices: List or numpy array of underlying asset prices over time.
        :param short_window: Lookback period for the short moving average.
        :param long_window: Lookback period for the long moving average.
        """
        self.prices = np.array(prices)
        self.short_window = short_window
        self.long_window = long_window
        self.short_ma = self.calculate_moving_average(short_window)
        self.long_ma = self.calculate_moving_average(long_window)

        # Align both moving averages to the same length
        min_length = min(len(self.short_ma), len(self.long_ma))
        self.short_ma = self.short_ma[-min_length:]
        self.long_ma = self.long_ma[-min_length:]

    def calculate_moving_average(self, window):
        """
        Calculate the moving average with the given window size.

        :param window: The number of periods for moving average.
        :return: Numpy array of moving average values.
        """
        return np.convolve(self.prices, np.ones(window)/window, mode='valid')

    def check_crossing(self):
        """
        Check if the short MA crosses the long MA before maturity.

        :return: True if a crossing occurs, False otherwise.
        """
        cross = np.sign(self.short_ma[:-1] - self.long_ma[:-1]) != np.sign(self.short_ma[1:] - self.long_ma[1:])
        return np.any(cross)

    def payoff(self):
        """
        Compute the option payoff based on the moving average cross.

        :return: The payoff value.
        """
        if self.check_crossing():
            return abs(self.short_ma[-1] - self.long_ma[-1])
        return 0.0

# Example usage
prices = [100, 102, 101, 103, 105, 107, 106, 108, 65, 85]
option = OptionAsianMovingAverage(prices, short_window=3, long_window=5)
print("Payoff:", option.payoff())
