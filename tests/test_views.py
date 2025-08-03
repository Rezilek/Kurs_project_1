from unittest.mock import patch, MagicMock
import pandas as pd
import pytest
from datetime import datetime

from src.views import home_page, events_page

@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    """Фикстура с тестовыми транзакциями"""
    return pd.DataFrame({
        "Дата операции": pd.to_datetime(["2023-05-15 10:00:00", "2023-05-16 11:00:00"]),
        "Сумма операции": [-1000, 2000],
        "Категория": ["Тест1", "Тест2"],
        "Описание": ["Транзакция1", "Транзакция2"]
    })

def test_home_page_success(sample_transactions: pd.DataFrame) -> None:
    """Тест успешного выполнения home_page"""
    with patch("src.views.load_transactions", return_value=sample_transactions):
        result = home_page("2023-05-15 12:00:00")
        assert "greeting" in result
        assert len(result["top_transactions"]) == 2

def test_events_page_success(sample_transactions: pd.DataFrame) -> None:
    """Тест успешного выполнения events_page"""
    with patch("src.views.load_transactions", return_value=sample_transactions):
        result = events_page("2023-05-15 12:00:00")
        assert "expenses" in result
        assert "income" in result

def test_home_page_empty_data() -> None:
    """Тест home_page с пустыми данными"""
    with patch("src.views.load_transactions", return_value=pd.DataFrame()):
        result = home_page("2023-05-15 12:00:00")
        assert len(result["top_transactions"]) == 0

def test_events_page_empty_data() -> None:
    """Тест events_page с пустыми данными"""
    with patch("src.views.load_transactions", return_value=pd.DataFrame()):
        result = events_page("2023-05-15 12:00:00")
        assert result["expenses"]["total_amount"] == 0
