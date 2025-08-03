import pytest
import pandas as pd
from datetime import datetime
from src.reports import (
    spending_by_category,
    spending_by_weekday,
    spending_by_workday
)


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """Тестовые данные транзакций"""
    return pd.DataFrame({
        "Дата операции": pd.to_datetime([
            "2023-05-15",  # Понедельник
            "2023-05-16",  # Вторник
            "2023-05-20"  # Суббота
        ]),
        "Категория": ["Супермаркеты", "Услуги", "Развлечения"],
        "Сумма операции": [-1500.50, -2500.00, -3000.00]
    })


def test_spending_by_category(sample_transactions: pd.DataFrame) -> None:
    """Тест анализа по категории"""
    result = spending_by_category(sample_transactions, "Супермаркеты")
    assert isinstance(result, dict)
    assert "2023-05-15" in result
    assert result["2023-05-15"] == -1500.50

    # Тест с несуществующей категорией
    assert spending_by_category(sample_transactions, "Несуществующая") == {}


def test_spending_by_weekday(sample_transactions: pd.DataFrame) -> None:
    """Тест анализа по дням недели"""
    result = spending_by_weekday(sample_transactions)
    assert isinstance(result, dict)
    assert 0 in result  # Понедельник
    assert 5 in result  # Суббота


def test_spending_by_workday(sample_transactions: pd.DataFrame) -> None:
    """Тест сравнения рабочих/выходных дней"""
    result = spending_by_workday(sample_transactions)
    assert isinstance(result, dict)
    assert result["weekdays"] == -4000.50  # Пн + Вт
    assert result["weekends"] == -3000.00  # Сб


def test_edge_cases() -> None:
    """Тест граничных случаев"""
    empty_df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма операции"])
    assert spending_by_category(empty_df, "Тест") == {}
    assert spending_by_weekday(empty_df) == {}
    assert spending_by_workday(empty_df) == {"weekdays": 0.0, "weekends": 0.0}

    # Нет нужных колонок
    invalid_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    assert spending_by_category(invalid_df, "Тест") == {}
    assert spending_by_weekday(invalid_df) == {}
    assert spending_by_workday(invalid_df) == {"weekdays": 0.0, "weekends": 0.0}
