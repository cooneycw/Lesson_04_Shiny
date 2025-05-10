# Insurance Fundamentals - Shiny App

This is a Shiny for Python application demonstrating key insurance concepts through interactive visualizations.

## Features

The app includes five interactive modules:

1. **Law of Large Numbers**: Demonstrates how observed probability converges to true probability as sample size increases
2. **Risk Pooling**: Shows how insurance distributes risk across many policyholders
3. **Balance Sheet**: Visualizes insurance company balance sheet components and the impact of loss ratios
4. **Premium Calculation**: Illustrates how insurance premiums are calculated
5. **Role of Capital**: Demonstrates how capital protects insurance companies from bankruptcy

## Requirements

- Python 3.7+
- Packages: shiny, pandas, numpy, matplotlib, rsconnect-python

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the app locally:

```
shiny run app.py
```

## Deployment to shinyapps.io

1. Create an account on [shinyapps.io](https://www.shinyapps.io)
2. Install rsconnect-python:
   ```
   pip install rsconnect-python
   ```
3. Configure your account:
   ```
   rsconnect add --name shinyapps --token YOUR_TOKEN --secret YOUR_SECRET
   ```
4. Deploy the app:
   ```
   rsconnect deploy shiny . --name shinyapps --title InsuranceFundamentals
   ```

## Project Structure

- `app.py`: Main Shiny application file
- `modules/`: Directory containing the demonstration modules
  - `law_of_large_numbers.py`: Law of Large Numbers demonstration
  - `risk_pooling.py`: Risk Pooling demonstration
  - `balance_sheet.py`: Balance Sheet demonstration
  - `premium_calculation.py`: Premium Calculation demonstration
  - `capital_role.py`: Capital Role demonstration
- `requirements.txt`: List of Python dependencies