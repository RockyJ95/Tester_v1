from financial_app.calculations import (
    calculate_debt_payoff,
    calculate_expense_summary,
    calculate_net_income,
    generate_financial_overview,
)


def test_calculate_net_income_handles_pre_and_post_tax_deductions():
    breakdown = calculate_net_income(
        gross_income=6000,
        tax_rate=0.2,
        pre_tax_deductions={"401k": 300},
        post_tax_deductions={"Insurance": 200},
    )

    assert round(breakdown.taxable_income, 2) == 5700.0
    assert round(breakdown.tax_paid, 2) == 1140.0
    assert round(breakdown.net_income, 2) == 4360.0


def test_calculate_debt_payoff_returns_total_interest():
    summary = calculate_debt_payoff(
        name="Loan",
        principal=1000,
        annual_interest_rate=0.12,
        monthly_payment=100,
    )

    assert summary.months_to_payoff > 0
    assert summary.total_interest_paid > 0
    assert summary.total_amount_paid == summary.total_interest_paid + 1000


def test_calculate_expense_summary_orders_categories():
    summary = calculate_expense_summary({"b": 2, "a": 1})
    assert summary["total"] == 3
    assert list(summary["by_category"].keys()) == ["a", "b"]


def test_generate_financial_overview_combines_sections():
    profile = {
        "gross_income": 5000,
        "tax_rate": 0.22,
        "pre_tax_deductions": {"401k": 200},
        "post_tax_deductions": {"Insurance": 150},
        "debts": [
            {
                "name": "Car",
                "principal": 10000,
                "annual_interest_rate": 0.05,
                "monthly_payment": 300,
            }
        ],
        "expenses": {"Rent": 1500},
    }

    overview = generate_financial_overview(profile)
    assert overview["net_income"].net_income > 0
    assert overview["debts"][0].name == "Car"
    assert overview["expenses"]["total"] == 1500
