"""Command-line interface for the financial planning app."""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from typing import Any, Dict

from .calculations import DebtPayoffSummary, NetIncomeBreakdown, generate_financial_overview
from .config import load_profile


def _format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def _render_net_income(net: NetIncomeBreakdown) -> str:
    lines = ["NET INCOME"]
    lines.append(f"Gross income: {_format_currency(net.gross_income)}")
    lines.append(f"Taxable income: {_format_currency(net.taxable_income)}")
    lines.append(f"Tax rate: {net.tax_rate:.2%}")
    lines.append(f"Tax paid: {_format_currency(net.tax_paid)}")

    if net.pre_tax_deductions:
        lines.append("Pre-tax deductions:")
        for name, amount in net.pre_tax_deductions.items():
            lines.append(f"  - {name}: {_format_currency(amount)}")

    if net.post_tax_deductions:
        lines.append("Post-tax deductions:")
        for name, amount in net.post_tax_deductions.items():
            lines.append(f"  - {name}: {_format_currency(amount)}")

    lines.append(f"Total deductions: {_format_currency(net.total_deductions)}")
    lines.append(f"Net income: {_format_currency(net.net_income)}")
    return "\n".join(lines)


def _render_debt(debt: DebtPayoffSummary) -> str:
    lines = [f"Debt: {debt.name}"]
    lines.append(f"  Months to payoff: {debt.months_to_payoff}")
    lines.append(f"  Years to payoff: {debt.years_to_payoff:.2f}")
    lines.append(f"  Total interest paid: {_format_currency(debt.total_interest_paid)}")
    lines.append(f"  Total paid: {_format_currency(debt.total_amount_paid)}")
    return "\n".join(lines)


def _render_expenses(expenses: Dict[str, Any]) -> str:
    lines = ["EXPENSES"]
    lines.append(f"Total monthly expenses: {_format_currency(expenses['total'])}")
    if expenses["by_category"]:
        lines.append("By category:")
        for name, amount in expenses["by_category"].items():
            lines.append(f"  - {name}: {_format_currency(amount)}")
    return "\n".join(lines)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Financial planning toolkit")
    parser.add_argument(
        "profile",
        type=str,
        help="Path to a JSON profile describing income, debts, and expenses.",
    )
    parser.add_argument(
        "--as-json",
        action="store_true",
        help="Output the report as JSON instead of a formatted summary.",
    )
    return parser


def main(argv: Any = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    profile = load_profile(args.profile)
    overview = generate_financial_overview(profile)

    if args.as_json:
        serialisable = {
            "net_income": asdict(overview["net_income"]),
            "debts": [asdict(debt) for debt in overview["debts"]],
            "expenses": overview["expenses"],
        }
        print(json.dumps(serialisable, indent=2))
    else:
        print(_render_net_income(overview["net_income"]))
        if overview["debts"]:
            print("\nDEBTS")
            for debt in overview["debts"]:
                print(_render_debt(debt))
        else:
            print("\nDEBTS\nNo debts provided.")
        print("\n" + _render_expenses(overview["expenses"]))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
