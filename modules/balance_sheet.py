import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def demonstrate_balance_sheet(loss_ratio=0.65, return_fig=False):
    """
    Demonstrates the components of an insurance company balance sheet

    Parameters:
    -----------
    loss_ratio : float
        The loss ratio (losses/premium)
    return_fig : bool
        If True, returns the figure and stats for Shiny integration

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The figure object (if return_fig is True)
    stats : dict
        Key statistics (if return_fig is True)
    """
    # Base values for a small insurance company (in millions)
    premium_revenue = 100  # $100M in premium

    # Calculate components based on loss ratio
    # Loss ratio = losses/premium
    expected_losses = premium_revenue * loss_ratio
    expenses = premium_revenue * 0.25  # Fixed expense ratio of 25%
    required_capital = premium_revenue * 0.5  # Regulatory minimum capital

    # Define the minimum capital ratio
    min_capital_ratio = 0.5  # Matches the required_capital calculation above

    # Calculate underwriting profit/loss
    underwriting_result = premium_revenue - expected_losses - expenses

    # Calculate investment income (5% return on invested premium+capital)
    investable_assets = premium_revenue + required_capital
    investment_return_rate = 0.05
    investment_income = investable_assets * investment_return_rate

    # Total profit/loss
    total_profit = underwriting_result + investment_income

    # Balance sheet components
    assets = {
        'Premiums Receivable': premium_revenue * 0.1,  # 10% of premium not yet collected
        'Cash & Investments': investable_assets
    }

    liabilities = {
        'Loss Reserves': expected_losses,
        'Unearned Premium': premium_revenue * 0.5  # Assume 50% of premiums unearned
    }

    # Total assets and liabilities
    total_assets = sum(assets.values())
    total_liabilities = sum(liabilities.values())

    # Capital (equity) = assets - liabilities
    capital = total_assets - total_liabilities

    # Capital ratio = capital / premium
    capital_ratio = capital / premium_revenue

    # For Shiny integration
    if return_fig:
        # Create figure with three vertically stacked subplots
        fig = Figure(figsize=(12, 15))

        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)

        # Plot 1: Balance Sheet
        # Create x positions for the two groups of bars
        x_pos = [0.3, 1.7]

        # Create the stacked bar for Assets side
        asset_values = list(assets.values())
        asset_bottom = 0
        asset_colors = ['cornflowerblue', 'skyblue']
        for i, value in enumerate(asset_values):
            ax1.bar(x_pos[0], value, bottom=asset_bottom, width=0.8, color=asset_colors[i], alpha=0.7)
            ax1.text(x_pos[0], asset_bottom + value / 2, f'{list(assets.keys())[i]}\n${value:.1f}M',
                     ha='center', va='center', fontsize=11)
            asset_bottom += value

        # Create the stacked bar for Liabilities & Capital side
        liab_capital_values = list(liabilities.values()) + [capital]
        liab_capital_colors = ['lightgreen', 'mediumseagreen', 'gold']
        liab_bottom = 0
        for i, value in enumerate(liab_capital_values):
            color = liab_capital_colors[i]
            name = list(liabilities.keys())[i] if i < len(liabilities) else 'Capital (Equity)'
            ax1.bar(x_pos[1], value, bottom=liab_bottom, width=0.8, color=color, alpha=0.7)
            ax1.text(x_pos[1], liab_bottom + value / 2, f'{name}\n${value:.1f}M',
                     ha='center', va='center', fontsize=11)
            liab_bottom += value

        # Set x-axis labels properly
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(['Assets', 'Liabilities & Capital'])

        ax1.set_title('Balance Sheet (in $ millions)')
        ax1.set_ylabel('Amount ($ millions)')

        # Add totals adjacent to the bars
        ax1.text(0.35, total_assets * 0.95, f'Total: ${total_assets:.1f}M', ha='left', fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
        ax1.text(1.35, (total_liabilities + capital) * 0.95, f'Total: ${total_liabilities + capital:.1f}M', ha='left',
                 fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

        # Set limits to make room for the labels
        ax1.set_ylim(0, total_assets * 1.1)
        ax1.set_xlim(-0.5, 2.5)

        # Plot 2: Income components
        income_components = {
            'Premium': premium_revenue,
            'Losses': -expected_losses,
            'Expenses': -expenses,
            'Investment Income': investment_income,
            'Profit/Loss': total_profit
        }

        # Calculate positions for waterfall chart
        cumulative = 0
        bottoms = []
        heights = []

        for name, value in income_components.items():
            if name == 'Profit/Loss':
                bottoms.append(0)
                heights.append(total_profit)
            else:
                bottoms.append(cumulative if value > 0 else cumulative + value)
                heights.append(abs(value))
                cumulative += value

        # Colors based on positive/negative values
        colors = ['blue', 'red', 'red', 'green', 'purple' if total_profit >= 0 else 'red']

        # Create waterfall chart
        bars = ax2.bar(income_components.keys(), heights, bottom=bottoms, color=colors, alpha=0.7)

        # Add values
        for i, (name, value) in enumerate(income_components.items()):
            if name == 'Profit/Loss':
                ax2.text(i, total_profit / 2 if total_profit >= 0 else total_profit / 2,
                         f'${value:.1f}M', ha='center', va='center', color='white' if abs(value) > 10 else 'black')
            else:
                position = bottoms[i] + heights[i] / 2
                ax2.text(i, position, f'${value:.1f}M', ha='center', va='center',
                         color='white' if abs(value) > 10 else 'black')

        ax2.set_title('Income Statement (in $ millions)')
        ax2.set_ylabel('Amount ($ millions)')
        ax2.grid(axis='y', alpha=0.3)

        # Plot 3: Capital in absolute dollars instead of as a ratio
        min_capital = premium_revenue * 0.5  # Regulatory minimum capital (50% of premium)

        # Create horizontal bar for capital
        ax3.barh(['Current Capital'], [capital], color='green' if capital >= min_capital else 'red',
                 alpha=0.7)
        ax3.barh(['Minimum Required'], [min_capital], color='red', alpha=0.3)

        ax3.set_title('Capital Requirements (in $ millions)')
        ax3.set_xlabel('Amount ($ millions)')
        ax3.set_xlim(0, max(min_capital, capital) * 1.2)

        # Add annotations
        ax3.text(capital, 0, f'${capital:.1f}M', va='center')
        ax3.text(min_capital, 1, f'${min_capital:.1f}M (Minimum)', va='center')

        # Add interpretation text
        status = "ADEQUATE" if capital >= min_capital else "INADEQUATE"
        color = "green" if capital >= min_capital else "red"

        ax3.text(0.5, 0.5, f"Capital Status: {status}", transform=ax3.transAxes,
                 ha='center', va='center', fontsize=16, color=color,
                 bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

        # Adjust spacing between subplots
        fig.subplots_adjust(hspace=0.4)

        # Key statistics to return
        stats = {
            'expected_losses': expected_losses,
            'expenses': expenses,
            'underwriting_result': underwriting_result,
            'investment_income': investment_income,
            'total_profit': total_profit,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'capital': capital,
            'capital_ratio': capital_ratio
        }

        return fig, stats

    # Original function for compatibility
    else:
        # Create figure with three vertically stacked subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

        # Plot 1: Balance Sheet - FIXED VERSION
        # Create x positions for the two groups of bars - wider spacing for better readability
        x_pos = [0.3, 1.7]

        # Create the stacked bar for Assets side
        asset_values = list(assets.values())
        asset_bottom = 0
        asset_colors = ['cornflowerblue', 'skyblue']  # Reversed colors for reversed order
        for i, value in enumerate(asset_values):
            ax1.bar(x_pos[0], value, bottom=asset_bottom, width=0.8, color=asset_colors[i], alpha=0.7)
            ax1.text(x_pos[0], asset_bottom + value / 2, f'{list(assets.keys())[i]}\n${value:.1f}M',
                     ha='center', va='center', fontsize=11)
            asset_bottom += value

        # Create the stacked bar for Liabilities & Capital side
        liab_capital_values = list(liabilities.values()) + [capital]
        liab_capital_colors = ['lightgreen', 'mediumseagreen', 'gold']  # Distinct greens + gold for capital
        liab_bottom = 0
        for i, value in enumerate(liab_capital_values):
            color = liab_capital_colors[i]
            name = list(liabilities.keys())[i] if i < len(liabilities) else 'Capital (Equity)'
            ax1.bar(x_pos[1], value, bottom=liab_bottom, width=0.8, color=color, alpha=0.7)
            ax1.text(x_pos[1], liab_bottom + value / 2, f'{name}\n${value:.1f}M',
                     ha='center', va='center', fontsize=11)
            liab_bottom += value

        # Set x-axis labels properly
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(['Assets', 'Liabilities & Capital'])

        ax1.set_title('Balance Sheet (in $ millions)')
        ax1.set_ylabel('Amount ($ millions)')

        # Add totals adjacent to the bars instead of on top
        ax1.text(0.35, total_assets * 0.95, f'Total: ${total_assets:.1f}M', ha='left', fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
        ax1.text(1.35, (total_liabilities + capital) * 0.95, f'Total: ${total_liabilities + capital:.1f}M', ha='left',
                 fontsize=12,
                 bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

        # Set limits to make room for the labels
        ax1.set_ylim(0, total_assets * 1.1)
        ax1.set_xlim(-0.5, 2.5)

        # Plot 2: Income components
        income_components = {
            'Premium': premium_revenue,
            'Losses': -expected_losses,
            'Expenses': -expenses,
            'Investment Income': investment_income,
            'Profit/Loss': total_profit
        }

        # Calculate positions for waterfall chart
        cumulative = 0
        bottoms = []
        heights = []

        for name, value in income_components.items():
            if name == 'Profit/Loss':
                bottoms.append(0)
                heights.append(total_profit)
            else:
                bottoms.append(cumulative if value > 0 else cumulative + value)
                heights.append(abs(value))
                cumulative += value

        # Colors based on positive/negative values
        colors = ['blue', 'red', 'red', 'green', 'purple' if total_profit >= 0 else 'red']

        # Create waterfall chart
        bars = ax2.bar(income_components.keys(), heights, bottom=bottoms, color=colors, alpha=0.7)

        # Add values
        for i, (name, value) in enumerate(income_components.items()):
            if name == 'Profit/Loss':
                ax2.text(i, total_profit / 2 if total_profit >= 0 else total_profit / 2,
                         f'${value:.1f}M', ha='center', va='center', color='white' if abs(value) > 10 else 'black')
            else:
                position = bottoms[i] + heights[i] / 2
                ax2.text(i, position, f'${value:.1f}M', ha='center', va='center',
                         color='white' if abs(value) > 10 else 'black')

        ax2.set_title('Income Statement (in $ millions)')
        ax2.set_ylabel('Amount ($ millions)')
        ax2.grid(axis='y', alpha=0.3)

        # Plot 3: Capital in absolute dollars instead of as a ratio
        min_capital = premium_revenue * 0.5  # Regulatory minimum capital (50% of premium)

        # Create horizontal bar for capital
        ax3.barh(['Current Capital'], [capital], color='green' if capital >= min_capital else 'red',
                 alpha=0.7)
        ax3.barh(['Minimum Required'], [min_capital], color='red', alpha=0.3)

        ax3.set_title('Capital Requirements (in $ millions)')
        ax3.set_xlabel('Amount ($ millions)')
        ax3.set_xlim(0, max(min_capital, capital) * 1.2)

        # Add annotations
        ax3.text(capital, 0, f'${capital:.1f}M', va='center')
        ax3.text(min_capital, 1, f'${min_capital:.1f}M (Minimum)', va='center')

        # Add interpretation text
        status = "ADEQUATE" if capital >= min_capital else "INADEQUATE"
        color = "green" if capital >= min_capital else "red"

        ax3.text(0.5, 0.5, f"Capital Status: {status}", transform=ax3.transAxes,
                 ha='center', va='center', fontsize=16, color=color,
                 bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))

        # Adjust spacing between subplots for better layout
        plt.subplots_adjust(hspace=0.4)
        plt.tight_layout()
        plt.show()

        # Display insurance interpretation
        print("\nInsurance Interpretation:")
        print(
            f"• Loss Ratio: {loss_ratio:.2f} (${expected_losses:.1f}M in losses per ${premium_revenue:.1f}M in premium)")
        print(f"• Underwriting Result: ${underwriting_result:.1f}M")
        print(f"• Investment Income: ${investment_income:.1f}M")
        print(f"• Total Profit: ${total_profit:.1f}M")
        print(f"• Capital: ${capital:.1f}M (Capital Ratio: {capital_ratio:.2f})")

        if capital_ratio < min_capital_ratio:
            print(f"• ALERT: Capital ratio is below the regulatory minimum of {min_capital_ratio:.2f}!")
            print(
                f"• The company needs at least ${(min_capital_ratio * premium_revenue - capital):.1f}M more capital to meet minimum requirements.")
        else:
            surplus = capital - (min_capital_ratio * premium_revenue)
            print(f"• The company has ${surplus:.1f}M of capital surplus above the regulatory minimum.")