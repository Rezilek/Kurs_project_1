from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from src.utils import (filter_transactions_by_date, get_currency_rates,
                       get_greeting, get_stock_prices, load_transactions)


@pytest.fixture
def sample_data(tmp_path: Path) -> Path:
    """Фикстура с тестовыми данными"""
    data = {
        "Дата операции": [
            "31.12.2021 16:44:00",
            "15.05.2023 10:30:00",
            "20.05.2023 18:15:00",
        ],
        "Сумма операции": [-1500.50, -2500.00, 10000.00],
        "Категория": ["Супермаркеты", "Услуги", "Переводы"],
        "Описание": ["Покупка", "Оплата", "Перевод"],
    }
    df = pd.DataFrame(data)
    test_file = tmp_path / "test_ops.xlsx"
    df.to_excel(test_file, index=False)
    return test_file


def test_load_transactions(sample_data: Path) -> None:
    """Тест загрузки транзакций"""
    result = load_transactions(str(sample_data))
    assert not result.empty
    assert "Дата операции" in result.columns


def test_filter_transactions(sample_data: Path) -> None:
    """Тест фильтрации транзакций"""
    df = load_transactions(str(sample_data))
    filtered = filter_transactions_by_date(df, "2023-05-01", "M")
    assert len(filtered) == 2


def test_greeting() -> None:
    """Тест приветствия"""
    assert get_greeting(datetime(2023, 1, 1, 6, 0)) == "Доброе утро"
    assert get_greeting(datetime(2023, 1, 1, 13, 0)) == "Добрый день"
    assert get_greeting(datetime(2023, 1, 1, 20, 0)) == "Добрый вечер"
    assert get_greeting(datetime(2023, 1, 1, 2, 0)) == "Доброй ночи"


def test_currency_rates() -> None:
    """Тест получения курсов валют"""
    rates = get_currency_rates(["USD", "EUR"])
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"


def test_stock_prices() -> None:
    """Тест получения цен акций"""
    prices = get_stock_prices(["AAPL", "GOOG"])
    assert len(prices) == 2
    assert prices[0]["stock"] == "AAPL"
