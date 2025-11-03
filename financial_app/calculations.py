"""Core calculation helpers for the financial planning app."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class NetIncomeBreakdown:
    """Detailed view of a net income calculation."""

    gross_income: float
    taxable_income: float
    tax_rate: float
    tax_paid: float
    pre_tax_deductions: Dict[str, float]
    post_tax_deductions: Dict[str, float]

    @property
    def total_deductions(self) -> float:
        return sum(self.pre_tax_deductions.values()) + sum(
            self.post_tax_deductions.values()
        ) + self.tax_paid

    @property
    def net_income(self) -> float:
        return self.gross_income - self.total_deductions


@dataclass
class DebtPayoffSummary:
    """Summary information about a debt payoff schedule."""

    name: str
    months_to_payoff: int
    years_to_payoff: float
    total_interest_paid: float
    total_amount_paid: float


def calculate_net_income(
    gross_income: float,
    tax_rate: float,
    pre_tax_deductions: Optional[Dict[str, float]] = None,
    post_tax_deductions: Optional[Dict[str, float]] = None,
) -> NetIncomeBreakdown:
    """Calculate the net income after all deductions.

    Args:
        gross_income: Total income before any deductions.
        tax_rate: Combined marginal tax rate expressed as a decimal (e.g. 0.22 for 22%).
        pre_tax_deductions: Deductions taken before taxes (e.g. retirement contributions).
        post_tax_deductions: Deductions taken after taxes (e.g. insurance premiums).

    Returns:
        A :class:`NetIncomeBreakdown` capturing details of the calculation.
    """

    pre_tax_deductions = pre_tax_deductions or {}
    post_tax_deductions = post_tax_deductions or {}

    taxable_income = max(gross_income - sum(pre_tax_deductions.values()), 0.0)
    tax_paid = taxable_income * tax_rate

    return NetIncomeBreakdown(
        gross_income=gross_income,
        taxable_income=taxable_income,
        tax_rate=tax_rate,
        tax_paid=tax_paid,
        pre_tax_deductions=dict(sorted(pre_tax_deductions.items())),
        post_tax_deductions=dict(sorted(post_tax_deductions.items())),
    )


def _iterate_debt_payoff(
    principal: float, annual_interest_rate: float, monthly_payment: float
) -> Tuple[int, float]:
    """Iteratively determine the number of months and interest paid to clear a debt."""

    if principal <= 0:
        return 0, 0.0

    monthly_rate = annual_interest_rate / 12
    if monthly_rate < 0:
        raise ValueError("Interest rate must not be negative.")

    if monthly_payment <= principal * monthly_rate:
        raise ValueError(
            "Monthly payment is too low to cover even the interest. Increase the payment."
        )

    months = 0
    total_interest = 0.0
    balance = principal

    while balance > 0:
        interest = balance * monthly_rate
        principal_payment = monthly_payment - interest
        balance = max(balance - principal_payment, 0.0)
        total_interest += interest
        months += 1

    return months, total_interest


def calculate_debt_payoff(
    name: str,
    principal: float,
    annual_interest_rate: float,
    monthly_payment: float,
) -> DebtPayoffSummary:
    """Compute payoff time and interest for a given debt."""

    months, total_interest = _iterate_debt_payoff(
        principal, annual_interest_rate, monthly_payment
    )
    total_paid = principal + total_interest

    return DebtPayoffSummary(
        name=name,
        months_to_payoff=months,
        years_to_payoff=months / 12 if months else 0.0,
        total_interest_paid=total_interest,
        total_amount_paid=total_paid,
    )


def calculate_expense_summary(expenses: Dict[str, float]) -> Dict[str, float]:
    """Summarise recurring expenses."""

    total = sum(expenses.values())
    return {
        "total": total,
        "by_category": dict(sorted(expenses.items())),
    }


def generate_financial_overview(profile: Dict) -> Dict:
    """Generate a comprehensive report for the provided financial profile."""

    net_income = calculate_net_income(
        profile.get("gross_income", 0.0),
        profile.get("tax_rate", 0.0),
        profile.get("pre_tax_deductions", {}),
        profile.get("post_tax_deductions", {}),
    )

    debts = profile.get("debts", [])
    debt_summaries: List[DebtPayoffSummary] = []
    for debt in debts:
        debt_summaries.append(
            calculate_debt_payoff(
                name=debt.get("name", "Debt"),
                principal=debt.get("principal", 0.0),
                annual_interest_rate=debt.get("annual_interest_rate", 0.0),
                monthly_payment=debt.get("monthly_payment", 0.0),
            )
        )

    expenses_summary = calculate_expense_summary(profile.get("expenses", {}))

    return {
        "net_income": net_income,
        "debts": debt_summaries,
        "expenses": expenses_summary,
    }
