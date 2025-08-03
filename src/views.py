import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from pandas import DataFrame

from src.utils import load_transactions, get_greeting, get_currency_rates, get_stock_prices

logger = logging.getLogger(__name__)


def home_page(date_time: str) -> Dict[str, Any]:
    """Формирует данные для главной страницы."""
    try:
        datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        transactions = load_transactions()

        result: Dict[str, Any] = {
            "greeting": get_greeting(datetime.now()),
            "cards": ["•••• 1234", "•••• 5678"],
            "currency_rates": get_currency_rates(["USD", "EUR"]),
            "stock_prices": get_stock_prices(["AAPL", "GOOG"]),
        }

        if not transactions.empty:
            result["top_transactions"] = transactions.nlargest(
                5, "Сумма операции"
            ).to_dict("records")
        else:
            result["top_transactions"] = []

        return result
    except Exception as e:
        logger.error(f"Ошибка в home_page: {str(e)}")
        return {
            "greeting": "Добрый день",
            "cards": [],
            "top_transactions": [],
            "currency_rates": {},
            "stock_prices": {},
        }


def events_page(date_time: str) -> Dict[str, Any]:
    """Формирует данные страницы событий."""
    try:
        datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        transactions = load_transactions()

        if transactions.empty:
            return {"expenses": {"total_amount": 0}, "income": {"total_amount": 0}}

        expenses = transactions[transactions["Сумма операции"] < 0]
        income = transactions[transactions["Сумма операции"] > 0]

        return {
            "expenses": {
                "total_amount": float(expenses["Сумма операции"].sum()),
                "count": len(expenses)
            },
            "income": {
                "total_amount": float(income["Сумма операции"].sum()),
                "count": len(income)
            }
        }
    except Exception as e:
        logger.error(f"Ошибка в events_page: {str(e)}")
        return {"expenses": {"total_amount": 0}, "income": {"total_amount": 0}}
