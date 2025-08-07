from datetime import datetime
from typing import Any, Dict, List

import pytest

from src.services import (investment_bank, person_transfers_search,
                          phone_number_search, profitable_cashback_categories,
                          simple_search)


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными транзакций"""
    return [
        {
            "Дата операции": datetime(2023, 5, 15),
            "Описание": "Покупка +7(123)456-78-90",
            "Категория": "Супермаркеты",
            "Сумма операции": -1500.50,
            "Бонусы (включая кэшбэк)": 15.05,
        },
        {
            "Дата операции": datetime(2023, 5, 16),
            "Описание": "Перевод Ивану Иванову",
            "Категория": "Переводы",
            "Сумма операции": 10000.00,
            "Бонусы (включая кэшбэк)": 0.00,
        },
    ]


def test_profitable_cashback_categories(
    sample_transactions: List[Dict[str, Any]]
) -> None:
    """Тестирует поиск категорий с максимальным кэшбэком"""
    result = profitable_cashback_categories(sample_transactions, 2023, 5)
    assert isinstance(result, dict)
    assert "Супермаркеты" in result


def test_investment_bank(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует расчет инвестиционных накоплений"""
    result = investment_bank("2023-05", sample_transactions, 10)
    assert isinstance(result, float)
    assert result == 150.05


def test_simple_search(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск по текстовому запросу"""
    result = simple_search("покупка", sample_transactions)
    assert isinstance(result, list)
    assert len(result) == 1


def test_phone_number_search(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск транзакций с номерами телефонов"""
    result = phone_number_search(sample_transactions)
    assert isinstance(result, list)
    assert len(result) == 1


def test_person_transfers_search(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует поиск переводов между физлицами"""
    result = person_transfers_search(sample_transactions)
    assert isinstance(result, list)
    assert len(result) == 1
