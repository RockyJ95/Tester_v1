# Financial Planning Toolkit

This lightweight command-line application helps you understand how your income is distributed, how long it will take to pay off debts, and where your monthly expenses are going.

## Features
- Net and gross income comparison with detailed tax and deduction breakdowns.
- Debt payoff timeline with total interest paid per debt.
- Monthly recurring expenses summary by category.
- JSON output for importing results into other tools.

## Getting Started
1. Create a Python virtual environment and install dependencies (only the standard library is used).
2. Prepare a JSON profile similar to [`sample_profile.json`](sample_profile.json).

Example profile structure:
```json
{
  "gross_income": 7500,
  "tax_rate": 0.24,
  "pre_tax_deductions": {
    "401k": 400,
    "HSA": 150
  },
  "post_tax_deductions": {
    "Health Insurance": 300,
    "Union Dues": 45
  },
  "debts": [
    {
      "name": "Auto Loan",
      "principal": 18000,
      "annual_interest_rate": 0.045,
      "monthly_payment": 400
    }
  ],
  "expenses": {
    "Rent": 1800,
    "Utilities": 250,
    "Groceries": 600,
    "Transportation": 220,
    "Subscriptions": 90
  }
}
```

## Usage
Run the CLI by pointing it at your profile file:

```bash
python -m financial_app.cli sample_profile.json
```

Add `--as-json` to output the full report as JSON instead of a human-readable summary.

```bash
python -m financial_app.cli sample_profile.json --as-json
```

## Notes
- Tax rate should be provided as a decimal (e.g. `0.22` for 22%).
- Pre-tax deductions reduce the taxable income before calculating taxes.
- The debt payoff calculation assumes fixed monthly payments and interest compounded monthly.
