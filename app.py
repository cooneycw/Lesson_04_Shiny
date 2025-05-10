from shiny import App, ui, render, reactive
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import random
import time

# Import the demonstration modules
from modules.law_of_large_numbers import demonstrate_law_of_large_numbers
from modules.risk_pooling import demonstrate_risk_pooling
from modules.balance_sheet import demonstrate_balance_sheet
from modules.premium_calculation import demonstrate_premium_calculation
from modules.capital_role import demonstrate_capital_role

# Define CSS for better styling
custom_css = """
.title-box {
    text-align: center;
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 15px;
}

.module-description {
    text-align: center;
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 0;
    color: #2C3E50;
}

.plot-title {
    text-align: center;
    font-weight: bold;
    font-size: 20px;
    margin-bottom: 15px;
    color: #2C3E50;
}

.plot-container {
    margin-bottom: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    padding: 15px;
    background-color: #ffffff;
}

.interpretation-box {
    margin-top: 20px;
    background-color: #E8F4FD;
    border-radius: 5px;
    padding: 15px;
    border-left: 5px solid #3498DB;
}

.interpretation-box pre {
    font-family: inherit;
    white-space: pre-wrap;
    margin: 0;
    font-size: 14px;
    line-height: 1.4;
}

.btn-resim {
    background-color: #3498DB;
    border-color: #2980B9;
    color: white;
    font-weight: bold;
    width: 100%;
}

.btn-resim:hover {
    background-color: #2980B9;
}
"""

# App UI - improved layout with re-simulate buttons only for random modules
app_ui = ui.page_fluid(
    ui.tags.style(custom_css),
    ui.h1("Insurance Fundamentals", style="text-align: center; margin-bottom: 10px;"),
    ui.p("Interactive demonstrations of key insurance concepts", style="text-align: center; margin-bottom: 20px;"),

    ui.navset_tab(
        ui.nav_panel("1. Law of Large Numbers",
                     # Title in its own row for proper centering
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "The Law of Large Numbers demonstrates how actual results converge to expected values as sample size increases."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders and button in the next row
                     ui.row(
                         ui.column(4,
                                   ui.input_slider("true_probability", "True Accident Probability:",
                                                   min=0.01, max=0.25, value=0.05, step=0.01)
                                   ),
                         ui.column(2,
                                   ui.br(),
                                   ui.input_action_button("resim_lln", "Re-simulate", class_="btn-resim")
                                   ),
                         ui.column(6)
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Observed Probability vs Sample Size"),
                            ui.output_plot("lln_plot", width="100%", height="500px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("lln_interpretation"))
                            )
                     ),

        ui.nav_panel("2. Risk Pooling",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Risk pooling shows how insurance distributes risk across many policyholders."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders and button in the next row
                     ui.row(
                         ui.column(3,
                                   ui.input_slider("accident_probability", "Accident Probability:",
                                                   min=0.01, max=0.25, value=0.05, step=0.01)
                                   ),
                         ui.column(3,
                                   ui.input_slider("num_policyholders", "Number of Policyholders:",
                                                   min=10, max=1000, value=100, step=10)
                                   ),
                         ui.column(2,
                                   ui.br(),
                                   ui.input_action_button("resim_risk", "Re-simulate", class_="btn-resim")
                                   ),
                         ui.column(4)
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Individual vs Pooled Risk"),
                            ui.output_plot("risk_pooling_plot", width="100%", height="500px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("risk_pooling_interpretation"))
                            )
                     ),

        ui.nav_panel("3. Balance Sheet",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "This demonstrates how an insurance company's balance sheet is affected by loss ratios."
                                                 )
                                          )
                                   )
                     ),
                     # Slider row - NO re-simulate button for this deterministic module
                     ui.row(
                         ui.column(6,
                                   ui.input_slider("loss_ratio", "Loss Ratio:",
                                                   min=0.40, max=1.0, value=0.65, step=0.05)
                                   ),
                         ui.column(6)
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Insurance Company Balance Sheet"),
                            ui.output_plot("balance_sheet_plot", width="100%", height="600px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("balance_sheet_interpretation"))
                            )
                     ),

        ui.nav_panel("4. Premium Calculation",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Demonstrates how insurance premiums are calculated based on frequency, severity, and other factors."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders row - NO re-simulate button for this deterministic module
                     ui.row(
                         ui.column(4,
                                   ui.input_slider("accident_frequency", "Accident Frequency:",
                                                   min=0.01, max=0.20, value=0.05, step=0.01)
                                   ),
                         ui.column(4,
                                   ui.input_slider("claim_severity", "Claim Severity ($):",
                                                   min=2000, max=20000, value=8000, step=1000)
                                   ),
                         ui.column(4)
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Premium Components and Breakdown"),
                            ui.output_plot("premium_calc_plot", width="100%", height="600px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("premium_calc_interpretation"))
                            )
                     ),

        ui.nav_panel("5. Role of Capital",
                     # Title in its own row
                     ui.row(
                         ui.column(12,
                                   ui.div({"class": "title-box"},
                                          ui.div({"class": "module-description"},
                                                 "Demonstrates how capital protects an insurance company from bankruptcy."
                                                 )
                                          )
                                   )
                     ),
                     # Sliders and button in the next row
                     ui.row(
                         ui.column(3,
                                   ui.input_slider("capital_amount", "Initial Capital ($M):",
                                                   min=10, max=100, value=50, step=10)
                                   ),
                         ui.column(3,
                                   ui.input_slider("num_years", "Simulation Years:",
                                                   min=5, max=100, value=10, step=5)
                                   ),
                         ui.column(2,
                                   ui.br(),
                                   ui.input_action_button("resim_capital", "Re-simulate", class_="btn-resim")
                                   ),
                         ui.column(4)
                     ),
                     ui.hr(),
                     # Main content below with clear separation
                     ui.div({"class": "plot-container"},
                            ui.div({"class": "plot-title"}, "Capital Protection Against Bankruptcy"),
                            ui.output_plot("capital_role_plot", width="100%", height="600px")
                            ),
                     ui.div({"class": "interpretation-box"},
                            ui.tags.pre(ui.output_text("capital_role_interpretation"))
                            )
                     )
    )
)


# Server logic
def server(input, output, session):
    # Reactive values to track simulation offsets - only for the modules that should be random
    lln_sim_offset = reactive.Value(0)
    risk_sim_offset = reactive.Value(0)
    capital_sim_offset = reactive.Value(0)

    # Update offset values when re-simulate buttons are clicked - FIXED as suggested
    @reactive.Effect
    def _():
        # Simply accessing the button value will trigger the effect on each click
        input.resim_lln()
        # Set a new random offset
        lln_sim_offset.set(random.randint(1, 10000))

    @reactive.Effect
    def _():
        # Simply accessing the button value will trigger the effect on each click
        input.resim_risk()
        # Set a new random offset
        risk_sim_offset.set(random.randint(1, 10000))

    @reactive.Effect
    def _():
        # Simply accessing the button value will trigger the effect on each click
        input.resim_capital()
        # Set a new random offset
        capital_sim_offset.set(random.randint(1, 10000))

    # Law of Large Numbers - RANDOM MODULE
    @reactive.Calc
    def lln_data():
        # Base seed on the slider value to ensure consistency
        # when returning to the same slider value
        base_seed = int(input.true_probability() * 10000)

        # Add the offset to create variation when re-simulate is clicked
        seed = base_seed + lln_sim_offset()

        # Set random seed and generate visualization
        np.random.seed(seed)
        return demonstrate_law_of_large_numbers(input.true_probability(), return_fig=True)

    @output
    @render.plot
    def lln_plot():
        fig, _ = lln_data()
        return fig

    @output
    @render.text
    def lln_interpretation():
        _, stats = lln_data()

        text = "Insurance Interpretation:\n"
        text += f"• With only 10 drivers, the observed accident rate was {stats['small_sample']:.1%}, "
        text += f"which is {abs(stats['small_sample'] - input.true_probability()) * 100:.1f} percentage points away from the true rate of {input.true_probability():.1%}\n"
        text += f"• With 50,000 drivers, the observed accident rate was {stats['large_sample']:.1%}, "
        text += f"which is {abs(stats['large_sample'] - input.true_probability()) * 100:.1f} percentage points away from the true rate\n"
        text += "• Insurance companies rely on large numbers of policyholders to make accurate predictions!"

        return text

    # Risk Pooling - RANDOM MODULE
    @reactive.Calc
    def risk_data():
        # Base seed on the slider values to ensure consistency
        base_seed = int(input.accident_probability() * 10000 + input.num_policyholders())

        # Add the offset to create variation when re-simulate is clicked
        seed = base_seed + risk_sim_offset()

        # Set random seed and generate visualization
        np.random.seed(seed)
        return demonstrate_risk_pooling(
            input.accident_probability(),
            input.num_policyholders(),
            return_fig=True
        )

    @output
    @render.plot
    def risk_pooling_plot():
        fig, _ = risk_data()
        return fig

    @output
    @render.text
    def risk_pooling_interpretation():
        _, stats = risk_data()

        claim_amount = 20000  # Fixed claim amount

        text = "Insurance Interpretation:\n"
        text += f"• Individual Risk: Each person has a {input.accident_probability():.1%} chance of a ${claim_amount:,.0f} loss.\n"
        text += f"• Without Insurance: {stats['num_with_loss']} people ({stats['percent_with_loss']:.1f}%) faced a ${claim_amount:,.0f} loss in this simulation.\n"
        text += f"• With Insurance: Everyone pays a premium of ${stats['fair_premium']:.0f}.\n"
        text += f"• Risk Pooling Result: The insurer collected ${stats['pool_premium_total']:,.0f} and paid ${stats['total_losses']:,.0f} in claims.\n"

        if stats['pool_performance'] < 1:
            text += f"• This year the insurance pool had a ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} surplus.\n"
            text += "• The surplus can be held as capital to handle future years when claims exceed premiums.\n"
        else:
            text += f"• This year the insurance pool had a ${abs(stats['pool_premium_total'] - stats['total_losses']):,.0f} deficit.\n"
            text += "• The deficit must be covered by the insurer's capital reserves.\n"

        text += f"• Key Insight: As the number of policyholders increases, the 'Actual/Expected' ratio approaches 1.0, "
        text += f"making the insurance pool's results more predictable and stable."

        return text

    # Balance Sheet - DETERMINISTIC MODULE (no randomness)
    @reactive.Calc
    def balance_sheet_data():
        # Simply pass the loss ratio directly - no randomness
        return demonstrate_balance_sheet(input.loss_ratio(), return_fig=True)

    @output
    @render.plot
    def balance_sheet_plot():
        fig, _ = balance_sheet_data()
        return fig

    @output
    @render.text
    def balance_sheet_interpretation():
        _, stats = balance_sheet_data()

        premium_revenue = 100  # $100M in premium (fixed)
        min_capital_ratio = 0.5

        text = "Insurance Interpretation:\n"
        text += f"• Loss Ratio: {stats['expected_losses'] / premium_revenue:.2f} (${stats['expected_losses']:.1f}M in losses per ${premium_revenue:.1f}M in premium)\n"
        text += f"• Underwriting Result: ${stats['underwriting_result']:.1f}M\n"
        text += f"• Investment Income: ${stats['investment_income']:.1f}M\n"
        text += f"• Total Profit: ${stats['total_profit']:.1f}M\n"
        text += f"• Capital: ${stats['capital']:.1f}M (Capital Ratio: {stats['capital_ratio']:.2f})\n"

        if stats['capital_ratio'] < min_capital_ratio:
            text += f"• ALERT: Capital ratio is below the regulatory minimum of {min_capital_ratio:.2f}!\n"
            text += f"• The company needs at least ${(min_capital_ratio * premium_revenue - stats['capital']):.1f}M more capital to meet minimum requirements."
        else:
            surplus = stats['capital'] - (min_capital_ratio * premium_revenue)
            text += f"• The company has ${surplus:.1f}M of capital surplus above the regulatory minimum."

        return text

    # Premium Calculation - DETERMINISTIC MODULE (no randomness)
    @reactive.Calc
    def premium_calc_data():
        # Simply pass the parameters directly - no randomness
        return demonstrate_premium_calculation(
            input.accident_frequency(),
            input.claim_severity(),
            return_fig=True
        )

    @output
    @render.plot
    def premium_calc_plot():
        fig, _ = premium_calc_data()
        return fig

    @output
    @render.text
    def premium_calc_interpretation():
        _, stats = premium_calc_data()

        expense_ratio = 0.25
        risk_margin_ratio = 0.05

        text = "Insurance Interpretation:\n"
        text += f"• Accident Frequency: {input.accident_frequency():.1%} (probability of claim per year)\n"
        text += f"• Average Claim Severity: ${input.claim_severity():,.0f} (average cost when a claim occurs)\n"
        text += f"• Expected Loss: ${stats['expected_loss']:.2f} (pure cost of risk)\n"
        text += f"• Expenses: ${stats['expenses']:.2f} ({expense_ratio:.0%} of premium for administration, commissions, etc.)\n"
        text += f"• Risk Margin: ${stats['risk_margin']:.2f} ({risk_margin_ratio:.0%} of premium for profit and uncertainty)\n"
        text += f"• Final Premium: ${stats['premium']:.2f}\n"
        text += "• This is the base premium before applying individual rating factors like age, driving history, etc."

        return text

    # Capital Role - RANDOM MODULE
    @reactive.Calc
    def capital_role_data():
        # Base seed on the slider values to ensure consistency
        base_seed = int(input.capital_amount() * 100 + input.num_years() * 10)

        # Add the offset to create variation when re-simulate is clicked
        seed = base_seed + capital_sim_offset()

        # Set random seed and generate visualization
        np.random.seed(seed)
        return demonstrate_capital_role(
            input.capital_amount(),
            input.num_years(),
            return_fig=True
        )

    @output
    @render.plot
    def capital_role_plot():
        fig, _ = capital_role_data()
        return fig

    @output
    @render.text
    def capital_role_interpretation():
        _, stats = capital_role_data()

        annual_premium = 100.0  # $100M annual premium - consistent with balance sheet
        capital_ratio = input.capital_amount() / annual_premium

        text = "Insurance Interpretation:\n"
        text += f"• Capital serves as a buffer against unexpected losses.\n"
        text += f"• With ${input.capital_amount():.1f}M of initial capital ({capital_ratio:.1f}x annual premium), "
        text += f"{stats['survival_rate']:.1%} of companies survived all {input.num_years()} years.\n"
        text += f"• Higher capital amounts mean better protection against insolvency.\n"
        text += f"• Insurance regulators require minimum capital levels to ensure companies can pay claims.\n"

        if stats['survival_rate'] < 0.90:
            text += f"• Warning: This capital level may be inadequate for long-term stability.\n"
            text += f"• Recommendation: Increase capital to improve survival probability."
        else:
            text += f"• This capital level appears adequate with a high survival probability."

        return text


# Create and run the app
app = App(app_ui, server)