import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, Dropdown, fixed

class BlackScholes:
    """
    A class for pricing options using the Black-Scholes model and calculating Greeks.
    
    Attributes:
        S0 (float): Current stock price (spot)
        K (float): Strike price
        r (float): Risk-free interest rate (annual)
        sigma (float): Implied volatility (annualized)
        T (float): Time to maturity (in years)
    """
    
    def __init__(self, S0, K, r, sigma, T):
        """
        Initialize Black-Scholes model with option parameters.
        
        Args:
            S0 (float): Current stock price (spot)
            K (float): Strike price
            r (float): Risk-free interest rate (annual)
            sigma (float): Implied volatility (annualized)
            T (float): Time to maturity (in years)
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.sigma = sigma
        self.T = T
        
        # Calculate d1 and d2 (used in many formulas)
        self._update_d1_d2()
        
    def _update_d1_d2(self):
        """Update d1 and d2 values after any parameter change."""
        if self.T <= 0:
            self.d1 = np.nan
            self.d2 = np.nan
        else:
            self.d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
            self.d2 = self.d1 - self.sigma * np.sqrt(self.T)
    
    def update_params(self, S0=None, K=None, r=None, sigma=None, T=None):
        """
        Update any of the model parameters.
        
        Args:
            S0 (float, optional): Current stock price
            K (float, optional): Strike price
            r (float, optional): Risk-free interest rate
            sigma (float, optional): Implied volatility
            T (float, optional): Time to maturity
        """
        if S0 is not None:
            self.S0 = S0
        if K is not None:
            self.K = K
        if r is not None:
            self.r = r
        if sigma is not None:
            self.sigma = sigma
        if T is not None:
            self.T = T
        
        self._update_d1_d2()
    
    def call_price(self):
        """Calculate the price of a call option."""
        if np.isnan(self.d1):
            return max(0, self.S0 - self.K)  # Intrinsic value at expiration
        
        return self.S0 * norm.cdf(self.d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
    
    def put_price(self):
        """Calculate the price of a put option."""
        if np.isnan(self.d1):
            return max(0, self.K - self.S0)  # Intrinsic value at expiration
        
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S0 * norm.cdf(-self.d1)
    
    def price(self, option_type, option_position='long'):
        """
        Calculate the price of an option.
        
        Args:
            option_type (str): 'call' or 'put'
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Option price (positive for long, negative for short)
        """
        if option_type.lower() == 'call':
            price = self.call_price()
        elif option_type.lower() == 'put':
            price = self.put_price()
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        
        if option_position.lower() == 'long':
            return price
        elif option_position.lower() == 'short':
            return -price
        else:
            raise ValueError("option_position must be 'long' or 'short'")
    
    # First-order Greeks
    
    def delta(self, option_type, option_position='long'):
        """
        Calculate the delta of an option (first derivative with respect to spot price).
        
        Args:
            option_type (str): 'call' or 'put'
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Delta value
        """
        if np.isnan(self.d1):
            # At expiration, delta is either 0 or 1 (or -1 for short)
            if option_type.lower() == 'call':
                delta = 1 if self.S0 > self.K else 0
            else:  # put
                delta = -1 if self.S0 < self.K else 0
        else:
            if option_type.lower() == 'call':
                delta = norm.cdf(self.d1)
            elif option_type.lower() == 'put':
                delta = norm.cdf(self.d1) - 1
            else:
                raise ValueError("option_type must be 'call' or 'put'")
        
        if option_position.lower() == 'short':
            delta = -delta
            
        return delta
    
    def gamma(self, option_position='long'):
        """
        Calculate the gamma of an option (second derivative with respect to spot price).
        Same for both calls and puts.
        
        Args:
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Gamma value
        """
        if np.isnan(self.d1):
            return 0  # Gamma is 0 at expiration
            
        gamma = norm.pdf(self.d1) / (self.S0 * self.sigma * np.sqrt(self.T))
        
        if option_position.lower() == 'short':
            gamma = -gamma
            
        return gamma
    
    def theta(self, option_type, option_position='long'):
        """
        Calculate the theta of an option (derivative with respect to time).
        
        Args:
            option_type (str): 'call' or 'put'
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Theta value (daily)
        """
        if np.isnan(self.d1):
            return 0  # Theta is 0 at expiration
            
        # Common term for both call and put
        common_term = -(self.S0 * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        
        if option_type.lower() == 'call':
            theta = common_term - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        elif option_type.lower() == 'put':
            theta = common_term + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        
        # Convert from yearly to daily theta
        theta = theta / 365.0
        
        if option_position.lower() == 'short':
            theta = -theta
            
        return theta
    
    def vega(self, option_position='long'):
        """
        Calculate the vega of an option (derivative with respect to volatility).
        Same for both calls and puts.
        
        Args:
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Vega value (for 1% change in volatility)
        """
        if np.isnan(self.d1):
            return 0  # Vega is 0 at expiration
            
        vega = self.S0 * np.sqrt(self.T) * norm.pdf(self.d1) * 0.01
        
        if option_position.lower() == 'short':
            vega = -vega
            
        return vega
    
    def rho(self, option_type, option_position='long'):
        """
        Calculate the rho of an option (derivative with respect to interest rate).
        
        Args:
            option_type (str): 'call' or 'put'
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Rho value (for 1% change in interest rate)
        """
        if np.isnan(self.d1):
            return 0  # Rho is 0 at expiration
            
        if option_type.lower() == 'call':
            rho = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) * 0.01
        elif option_type.lower() == 'put':
            rho = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) * 0.01
        else:
            raise ValueError("option_type must be 'call' or 'put'")
        
        if option_position.lower() == 'short':
            rho = -rho
            
        return rho
    
    # Second-order Greeks
    
    def charm(self, option_type, option_position='long'):
        """
        Calculate the charm of an option (derivative of delta with respect to time).
        Also known as delta decay.
        
        Args:
            option_type (str): 'call' or 'put'
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Charm value (daily)
        """
        if np.isnan(self.d1):
            return 0  # Charm is 0 at expiration
            
        d_pdf = norm.pdf(self.d1)
        
        charm = -d_pdf * ((self.r - self.d1 * self.sigma / (2 * np.sqrt(self.T))) / 
                         (self.sigma * np.sqrt(self.T)))
        
        if option_type.lower() == 'put':
            charm = -charm
        
        # Convert from yearly to daily
        charm = charm / 365.0
        
        if option_position.lower() == 'short':
            charm = -charm
            
        return charm
    
    def vanna(self, option_position='long'):
        """
        Calculate the vanna of an option (derivative of delta with respect to volatility).
        Or derivative of vega with respect to spot price.
        Same for both calls and puts.
        
        Args:
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Vanna value
        """
        if np.isnan(self.d1):
            return 0  # Vanna is 0 at expiration
            
        vanna = -norm.pdf(self.d1) * (self.d2 / self.sigma)
        
        if option_position.lower() == 'short':
            vanna = -vanna
            
        return vanna
    
    def volga(self, option_position='long'):
        """
        Calculate the volga of an option (second derivative with respect to volatility).
        Also known as vomma. Same for both calls and puts.
        
        Args:
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Volga value
        """
        if np.isnan(self.d1):
            return 0  # Volga is 0 at expiration
            
        vega = self.vega(option_position='long') * 100  # Vega for 1 point change (not %)
        volga = vega * (self.d1 * self.d2 / self.sigma)
        
        if option_position.lower() == 'short':
            volga = -volga
            
        return volga
    
    def veta(self, option_position='long'):
        """
        Calculate the veta of an option (derivative of vega with respect to time).
        Same for both calls and puts.
        
        Args:
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Veta value (daily)
        """
        if np.isnan(self.d1):
            return 0  # Veta is 0 at expiration
            
        veta = -self.S0 * norm.pdf(self.d1) * np.sqrt(self.T) * (
            (self.r - self.d1 * self.sigma / (2 * np.sqrt(self.T))) /
            (self.sigma * np.sqrt(self.T))
        ) * 0.01
        
        # Convert from yearly to daily
        veta = veta / 365.0
        
        if option_position.lower() == 'short':
            veta = -veta
            
        return veta
    
    def get_greek(self, greek_name, option_type=None, option_position='long'):
        """
        Get a specific Greek value.
        
        Args:
            greek_name (str): Name of the Greek ('delta', 'gamma', etc.)
            option_type (str, optional): 'call' or 'put' (not needed for gamma, vega, vanna, volga)
            option_position (str): 'long' or 'short'
            
        Returns:
            float: Value of the specified Greek
        """
        greek_name = greek_name.lower()
        
        if greek_name in ['gamma', 'vega', 'vanna', 'volga', 'veta']:
            return getattr(self, greek_name)(option_position=option_position)
        elif greek_name in ['delta', 'theta', 'rho', 'charm']:
            if option_type is None:
                raise ValueError(f"{greek_name} requires option_type to be specified")
            return getattr(self, greek_name)(option_type=option_type, option_position=option_position)
        else:
            raise ValueError(f"Unknown greek: {greek_name}")
    
    def get_all_greeks(self, option_type, option_position='long'):
        """
        Get all Greeks for a specific option type and position.
        
        Args:
            option_type (str): 'call' or 'put'
            option_position (str): 'long' or 'short'
            
        Returns:
            dict: Dictionary with all Greek values
        """
        return {
            'delta': self.delta(option_type, option_position),
            'gamma': self.gamma(option_position),
            'theta': self.theta(option_type, option_position),
            'vega': self.vega(option_position),
            'rho': self.rho(option_type, option_position),
            'charm': self.charm(option_type, option_position),
            'vanna': self.vanna(option_position),
            'volga': self.volga(option_position),
            'veta': self.veta(option_position)
        }

def plot_greek_vs_parameter(
    greek, param_name, option_type, option_position='long',
    S0=100, K=100, r=0.05, sigma=0.2, T=1,
    param_range=None
):
    """
    Plot a Greek against a changing parameter.
    
    Args:
        greek (str): Name of the Greek to plot
        param_name (str): Name of the parameter to vary ('S0', 'K', 'r', 'sigma', 'T')
        option_type (str): 'call' or 'put'
        option_position (str): 'long' or 'short'
        S0, K, r, sigma, T: Default values for the Black-Scholes parameters
        param_range (tuple, optional): Range for the parameter (min, max, steps)
    """
    # Default ranges for parameters
    default_ranges = {
        'S0': (50, 150, 100),  # 50 to 150, 100 steps
        'K': (50, 150, 100),
        'r': (0, 0.1, 100),    # 0% to 10%, 100 steps
        'sigma': (0.05, 0.5, 100), # 5% to 50%, 100 steps
        'T': (0.01, 2, 100)    # 0.01 to 2 years, 100 steps
    }
    
    # Use provided range or default
    if param_range is None:
        param_range = default_ranges[param_name]
    
    min_val, max_val, steps = param_range
    x_values = np.linspace(min_val, max_val, steps)
    y_values = []
    
    for x in x_values:
        # Create BS model with the current parameter value
        params = {'S0': S0, 'K': K, 'r': r, 'sigma': sigma, 'T': T}
        params[param_name] = x
        
        bs = BlackScholes(**params)
        
        # Get the Greek value
        if greek in ['gamma', 'vega', 'vanna', 'volga', 'veta']:
            y = bs.get_greek(greek, option_position=option_position)
        else:
            y = bs.get_greek(greek, option_type=option_type, option_position=option_position)
        
        y_values.append(y)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values)
    
    # Parameter-specific formatting
    param_labels = {
        'S0': 'Spot Price',
        'K': 'Strike Price',
        'r': 'Risk-Free Rate',
        'sigma': 'Implied Volatility',
        'T': 'Time to Maturity (years)'
    }
    
    greeks_labels = {
        'delta': 'Delta',
        'gamma': 'Gamma',
        'theta': 'Theta (daily)',
        'vega': 'Vega (1% change)',
        'rho': 'Rho (1% change)',
        'charm': 'Charm (daily)',
        'vanna': 'Vanna',
        'volga': 'Volga',
        'veta': 'Veta (daily)'
    }
    
    plt.title(f'{greeks_labels[greek]} vs {param_labels[param_name]} for {option_position} {option_type}')
    plt.xlabel(param_labels[param_name])
    plt.ylabel(greeks_labels[greek])
    plt.grid(True)
    
    # Add vertical line at the current parameter value
    current_value = {'S0': S0, 'K': K, 'r': r, 'sigma': sigma, 'T': T}[param_name]
    if min_val <= current_value <= max_val:
        plt.axvline(x=current_value, color='r', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def interactive_greek_analysis():
    """Create an interactive widget to explore Greeks vs parameters."""
    
    def update_plot(greek, param, option_type, option_position, S0, K, r, sigma, T):
        plot_greek_vs_parameter(
            greek, param, option_type, option_position, 
            S0, K, r, sigma, T
        )
    
    # Define the widgets
    greek_dropdown = Dropdown(
        options=['delta', 'gamma', 'theta', 'vega', 'rho', 'charm', 'vanna', 'volga', 'veta'],
        value='delta',
        description='Greek:'
    )
    
    param_dropdown = Dropdown(
        options=['S0', 'K', 'r', 'sigma', 'T'],
        value='S0',
        description='Parameter:'
    )
    
    option_type_dropdown = Dropdown(
        options=['call', 'put'],
        value='call',
        description='Option Type:'
    )
    
    option_position_dropdown = Dropdown(
        options=['long', 'short'],
        value='long',
        description='Position:'
    )
    
    S0_slider = FloatSlider(
        value=100.0, min=50.0, max=150.0, step=1.0,
        description='Spot Price:',
        continuous_update=False
    )
    
    K_slider = FloatSlider(
        value=100.0, min=50.0, max=150.0, step=1.0,
        description='Strike:',
        continuous_update=False
    )
    
    r_slider = FloatSlider(
        value=0.05, min=0.0, max=0.1, step=0.005,
        description='Rate:',
        continuous_update=False
    )
    
    sigma_slider = FloatSlider(
        value=0.2, min=0.05, max=0.5, step=0.01,
        description='Volatility:',
        continuous_update=False
    )
    
    T_slider = FloatSlider(
        value=1.0, min=0.01, max=2.0, step=0.01,
        description='Maturity:',
        continuous_update=False
    )
    
    # Create the interactive plot
    interact(
        update_plot,
        greek=greek_dropdown,
        param=param_dropdown,
        option_type=option_type_dropdown,
        option_position=option_position_dropdown,
        S0=S0_slider,
        K=K_slider,
        r=r_slider,
        sigma=sigma_slider,
        T=T_slider
    )

def option_price_calculator():
    """Interactive widget to calculate option prices and Greeks."""
    
    def update_calculation(option_type, option_position, S0, K, r, sigma, T):
        bs = BlackScholes(S0, K, r, sigma, T)
        price = bs.price(option_type, option_position)
        greeks = bs.get_all_greeks(option_type, option_position)
        
        print(f"Option: {option_position} {option_type}")
        print(f"Price: {price:.4f}")
        print("\nFirst-order Greeks:")
        print(f"Delta: {greeks['delta']:.4f}")
        print(f"Gamma: {greeks['gamma']:.4f}")
        print(f"Theta: {greeks['theta']:.4f} (daily)")
        print(f"Vega: {greeks['vega']:.4f} (for 1% change)")
        print(f"Rho: {greeks['rho']:.4f} (for 1% change)")
        print("\nSecond-order Greeks:")
        print(f"Charm: {greeks['charm']:.4f} (daily)")
        print(f"Vanna: {greeks['vanna']:.4f}")
        print(f"Volga: {greeks['volga']:.4f}")
        print(f"Veta: {greeks['veta']:.4f} (daily)")
    
    # Define the widgets
    option_type_dropdown = Dropdown(
        options=['call', 'put'],
        value='call',
        description='Option Type:'
    )
    
    option_position_dropdown = Dropdown(
        options=['long', 'short'],
        value='long',
        description='Position:'
    )
    
    S0_slider = FloatSlider(
        value=100.0, min=50.0, max=150.0, step=1.0,
        description='Spot Price:',
        continuous_update=False
    )
    
    K_slider = FloatSlider(
        value=100.0, min=50.0, max=150.0, step=1.0,
        description='Strike:',
        continuous_update=False
    )
    
    r_slider = FloatSlider(
        value=0.05, min=0.0, max=0.1, step=0.005,
        description='Rate:',
        continuous_update=False
    )
    
    sigma_slider = FloatSlider(
        value=0.2, min=0.05, max=0.5, step=0.01,
        description='Volatility:',
        continuous_update=False
    )
    
    T_slider = FloatSlider(
        value=1.0, min=0.01, max=2.0, step=0.01,
        description='Maturity:',
        continuous_update=False
    )
    
    # Create the interactive calculator
    interact(
        update_calculation,
        option_type=option_type_dropdown,
        option_position=option_position_dropdown,
        S0=S0_slider,
        K=K_slider,
        r=r_slider,
        sigma=sigma_slider,
        T=T_slider
    )

# Example usage
if __name__ == "__main__":
    # Create an instance with default parameters
    bs = BlackScholes(S0=100, K=100, r=0.05, sigma=0.2, T=1)
    
    # Calculate prices for different options
    call_price = bs.price('call', 'long')
    put_price = bs.price('put', 'long')
    short_call_price = bs.price('call', 'short')
    
    print(f"Long Call Price: {call_price:.4f}")
    print(f"Long Put Price: {put_price:.4f}")
    print(f"Short Call Price: {short_call_price:.4f}")
    
    # Calculate Greeks for a long call
    long_call_greeks = bs.get_all_greeks('call', 'long')
    print("\nLong Call Greeks:")
    for greek, value in long_call_greeks.items():
        print(f"{greek}: {value:.4f}")
    
    # Plot delta vs spot price for a long call
    plot_greek_vs_parameter('delta', 'S0', 'call', 'long')