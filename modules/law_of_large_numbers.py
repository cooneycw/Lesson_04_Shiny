import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def demonstrate_law_of_large_numbers(true_probability=0.05, seed=42, return_fig=False):
    """
    Demonstrates the Law of Large Numbers using an insurance claims example

    Parameters:
    -----------
    true_probability : float
        The true probability of an accident
    seed : int
        Random seed for reproducibility
    return_fig : bool
        If True, returns the figure and stats for Shiny integration

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Create sample sizes (increasing exponentially)
    sample_sizes = [10, 50, 100, 500, 1000, 5000, 10000, 50000]

    # Run experiment - simulate accidents for each sample size
    results = []

    # Set the seed using the provided value
    np.random.seed(seed)

    for size in sample_sizes:
        # Generate random accidents (1 = accident, 0 = no accident)
        accidents = np.random.random(size) < true_probability
        observed_probability = np.mean(accidents)
        results.append({
            'sample_size': size,
            'observed_probability': observed_probability,
            'true_probability': true_probability,
            'error': abs(observed_probability - true_probability)
        })

    # For Shiny integration, create a figure without displaying it
    if return_fig:
        # Create the plot
        fig = Figure(figsize=(14, 6))

        # Create subplots
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # DataFrame from results
        df = pd.DataFrame(results)

        # Plot 1: Observed probability vs sample size
        ax1.semilogx(df['sample_size'], df['observed_probability'], 'bo-', linewidth=2, markersize=8)
        ax1.axhline(true_probability, color='red', linestyle='--', label=f'True probability: {true_probability:.1%}')
        ax1.set_xlabel('Number of Drivers')
        ax1.set_ylabel('Observed Accident Rate')
        ax1.set_title(f'Observed Accident Rate vs. Sample Size')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Format x-tick labels to avoid scientific notation and use commas
        from matplotlib.ticker import ScalarFormatter, FuncFormatter

        def format_number(x, pos):
            if x >= 1000:
                return f'{x:,.0f}'  # Use commas for thousands
            return f'{x:.0f}'

        ax1.xaxis.set_major_formatter(FuncFormatter(format_number))

        # Set fixed y-axis scale based on 90% confidence interval for the smallest sample (10 drivers)
        # Using normal approximation to binomial with continuity correction
        smallest_sample = sample_sizes[0]  # 10 drivers
        p = true_probability
        # Z-score for 90% confidence is 1.645
        z_score = 1.645

        # Calculate confidence interval bounds for the smallest sample
        # Formula: p ± z * sqrt(p(1-p)/n)
        ci_width = z_score * np.sqrt(p * (1 - p) / smallest_sample)
        lower_bound = max(0, p - ci_width)
        upper_bound = min(1, p + ci_width)

        # Set y-axis with some padding to ensure all points are visible
        padding = 0.05  # 5% padding
        y_min = max(0, lower_bound - padding)
        y_max = min(1, upper_bound + padding)

        # Ensure the y-axis always includes the true probability
        y_min = min(y_min, true_probability * 0.5)
        y_max = max(y_max, true_probability * 1.5)

        # Set y-axis limits
        ax1.set_ylim(y_min, y_max)

        # Format x-tick labels to avoid scientific notation
        def format_number(x, pos):
            if x >= 1000000:
                return f'{x / 1000000:.0f}M'
            return f'{x:.0f}'

        # Add text annotations for each point
        for i, row in df.iterrows():
            ax1.annotate(f"{row['observed_probability']:.1%}",
                         (row['sample_size'], row['observed_probability']),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        # Plot 2: Error vs sample size - using semilogx (log scale for x, linear for y)
        # This allows us to include 0 on the y-axis
        ax2.semilogx(df['sample_size'], df['error'], 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('Number of Drivers')
        ax2.set_ylabel('Error (|Observed - True|)')
        ax2.set_title(f'Error vs. Sample Size')
        ax2.grid(True, alpha=0.3)

        # Format x-tick labels to avoid scientific notation and use commas
        ax2.xaxis.set_major_formatter(FuncFormatter(format_number))

        # Format y-tick labels to show more decimal places for small values
        def format_error_value(y, pos):
            if y < 0.001:
                return f'{y:.4f}'
            elif y < 0.01:
                return f'{y:.3f}'
            else:
                return f'{y:.2f}'

        ax2.yaxis.set_major_formatter(FuncFormatter(format_error_value))

        # Set y-axis to start from 0
        y_max = max(df['error']) * 1.2  # Add 20% to the max for clarity
        ax2.set_ylim(0, y_max)

        # Add text annotations for each point
        for i, row in df.iterrows():
            ax2.annotate(f"{row['error']:.3f}",
                         (row['sample_size'], row['error']),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        fig.tight_layout()

        # Remove seed text from figure
        # fig.text(0.5, 0.01, f"Simulation Seed: {seed}", ha='center',
        #          fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))

        # Return the figure and key statistics
        stats = {
            'small_sample': results[0]['observed_probability'],
            'medium_sample': results[5]['observed_probability'],
            'large_sample': results[7]['observed_probability'],
            'small_error': results[0]['error'],
            'medium_error': results[5]['error'],
            'large_error': results[7]['error'],
            'seed': seed  # Include seed in stats
        }

        return fig, stats

    # Original function for Jupyter notebook compatibility
    else:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Plot 1: Observed probability vs sample size
        df = pd.DataFrame(results)
        ax1.semilogx(df['sample_size'], df['observed_probability'], 'bo-', linewidth=2, markersize=8)
        ax1.axhline(true_probability, color='red', linestyle='--', label=f'True probability: {true_probability:.1%}')
        ax1.set_xlabel('Number of Drivers')
        ax1.set_ylabel('Observed Accident Rate')
        ax1.set_title(f'Observed Accident Rate vs. Sample Size (Seed: {seed})')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Format x-tick labels to avoid scientific notation
        def format_number(x, pos):
            if x >= 1000000:
                return f'{x / 1000000:.0f}M'
            return f'{x:.0f}'

        from matplotlib.ticker import FuncFormatter
        ax1.xaxis.set_major_formatter(FuncFormatter(format_number))

        # Add text annotations for each point
        for i, row in df.iterrows():
            ax1.annotate(f"{row['observed_probability']:.1%}",
                         (row['sample_size'], row['observed_probability']),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        # Plot 2: Error vs sample size
        ax2.loglog(df['sample_size'], df['error'], 'ro-', linewidth=2, markersize=8)
        ax2.set_xlabel('Number of Drivers')
        ax2.set_ylabel('Error (|Observed - True|)')
        ax2.set_title(f'Error vs. Sample Size (Seed: {seed})')
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(FuncFormatter(format_number))

        # Add text annotations for each point
        for i, row in df.iterrows():
            ax2.annotate(f"{row['error']:.3f}",
                         (row['sample_size'], row['error']),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center')

        # Add a text annotation with the seed value
        fig.text(0.5, 0.01, f"Simulation Seed: {seed}", ha='center',
                 fontsize=12, bbox=dict(facecolor='lightgray', alpha=0.5))

        plt.tight_layout()
        plt.show()

        # Display insurance interpretation
        print("\nInsurance Interpretation:")
        print(f"• Simulation Seed: {seed}")
        print(f"• With only 10 drivers, the observed accident rate was {results[0]['observed_probability']:.1%}, " +
              f"which is {results[0]['error'] * 100:.1f} percentage points away from the true rate of {true_probability:.1%}")
        print(f"• With 50,000 drivers, the observed accident rate was {results[7]['observed_probability']:.1%}, " +
              f"which is {results[7]['error'] * 100:.1f} percentage points away from the true rate")
        print("\nInsurance companies rely on large numbers of policyholders to make accurate predictions!")