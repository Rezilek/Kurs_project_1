import re
from typing import Any, Dict, List, Union

import pandas as pd
from pandas import DataFrame


def profitable_cashback_categories(
    transactions: Union[List[Dict[str, Any]], DataFrame], year: int, month: int
) -> Dict[str, float]:
    """Определяет категории с наибольшим кэшбэком"""
    if isinstance(transactions, DataFrame):
        df = transactions.copy()
    else:
        df = pd.DataFrame(transactions)

    try:
        if df.empty or "Дата операции" not in df.columns:
            return {}

        filtered = df[
            (df["Дата операции"].dt.year == year)
            & (df["Дата операции"].dt.month == month)
        ]
        cashback = (
            filtered.groupby("Категория")["Бонусы (включая кэшбэк)"].sum().nlargest(3)
        )
        return {str(k): float(v) for k, v in cashback.items()}
    except Exception:
        return {}


def investment_bank(
    month: str, transactions: Union[List[Dict[str, Any]], DataFrame], percent: int
) -> float:
    """Рассчитывает инвестиционные накопления."""
    if isinstance(transactions, DataFrame):
        df = transactions.copy()
    else:
        df = pd.DataFrame(transactions)

    monthly = df[df["Дата операции"].dt.strftime("%Y-%m") == month]
    expenses = monthly[monthly["Сумма операции"] < 0]["Сумма операции"].sum()
    return abs(float(expenses * percent / 100))


def simple_search(
    query: str, transactions: Union[List[Dict[str, Any]], DataFrame]
) -> List[Dict[str, Any]]:
    """
    Поиск транзакций по текстовому запросу в описании.

    Аргументы:
        query: Строка для поиска
        transactions: Список транзакций или DataFrame

    Возвращает:
        Список найденных транзакций
    """
    if isinstance(transactions, DataFrame):
        trans_list = [dict(row) for _, row in transactions.iterrows()]
    else:
        trans_list = transactions

    return [
        {str(k): v for k, v in t.items()}
        for t in trans_list
        if query.lower() in str(t.get("Описание", "")).lower()
    ]


def phone_number_search(
    transactions: Union[List[Dict[str, Any]], DataFrame]
) -> List[Dict[str, Any]]:
    """
    Поиск транзакций, содержащих номера телефонов в описании.

    Аргументы:
        transactions: Список транзакций или DataFrame

    Возвращает:
        Список транзакций с номерами телефонов
    """
    if isinstance(transactions, DataFrame):
        trans_list = [dict(row) for _, row in transactions.iterrows()]
    else:
        trans_list = transactions

    phone_pattern = re.compile(
        r"(\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    )
    return [
        {str(k): v for k, v in t.items()}
        for t in trans_list
        if phone_pattern.search(str(t.get("Описание", "")))
    ]


def person_transfers_search(
    transactions: Union[List[Dict[str, Any]], DataFrame]
) -> List[Dict[str, Any]]:
    """
    Поиск переводов между физическими лицами.

    Аргументы:
        transactions: Список транзакций или DataFrame

    Возвращает:
        Список найденных переводов
    """
    if isinstance(transactions, DataFrame):
        trans_list = [dict(row) for _, row in transactions.iterrows()]
    else:
        trans_list = transactions

    return [
        {str(k): v for k, v in t.items()}
        for t in trans_list
        if "перевод" in str(t.get("Описание", "")).lower()
        and not any(
            x in str(t.get("Описание", "")).lower() for x in ["банк", "организация"]
        )
    ]
