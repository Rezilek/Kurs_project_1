import json
from typing import Any, Dict, List


from src import (investment_bank, person_transfers_search, phone_number_search,
                 profitable_cashback_categories, simple_search,
                 spending_by_category, spending_by_weekday,
                 spending_by_workday)
from src.utils import load_transactions
from src.views import events_page, home_page


def main() -> None:
    """Основная функция для демонстрации функционала"""
    try:
        df = load_transactions()
        transactions: List[Dict[str, Any]] = [
            {str(k): v for k, v in row.items()} for row in df.to_dict("records")
        ]

        print("\n=== Home Page Demo ===")
        print(
            json.dumps(home_page("2023-05-15 14:30:00"), indent=2, ensure_ascii=False)
        )

        print("\n=== Events Page Demo ===")
        print(
            json.dumps(events_page("2023-05-15 14:30:00"), indent=2, ensure_ascii=False)
        )

        print("\n=== Services Demo ===")
        print("\nProfitable cashback categories:")
        print(
            json.dumps(
                profitable_cashback_categories(transactions, 2023, 5),
                indent=2,
                ensure_ascii=False,
            )
        )

        print(
            f"\nInvestment savings: {investment_bank('2023-05', transactions, 50)} RUB"
        )
        print(
            f"\nSimple search results (count): {len(simple_search('магазин', transactions))}"
        )
        print(
            f"\nPhone number search results (count): {len(phone_number_search(transactions))}"
        )
        print(
            f"\nPerson transfers search results (count): {len(person_transfers_search(transactions))}"
        )

        print("\n=== Reports Demo ===")
        print("\nSpending by category (Supermarkets):")
        print(spending_by_category(df, "Супермаркеты"))
        print("\nSpending by weekday:")
        print(spending_by_weekday(df))
        print("\nSpending by workday:")
        print(spending_by_workday(df))
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()
