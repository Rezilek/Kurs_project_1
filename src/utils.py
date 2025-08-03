import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Union
import pandas as pd
from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str = Config.DATA_FILE_PATH) -> pd.DataFrame:
    """
    Загружает транзакции из Excel файла

    Args:
        file_path: Путь к файлу

    Returns:
        DataFrame с транзакциями

    Raises:
        Exception: При ошибках загрузки
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")

        if df.empty:
            return pd.DataFrame(columns=[
                "Дата операции",
                "Сумма операции",
                "Категория",
                "Описание"
            ])

        # Преобразование дат
        if "Дата операции" in df.columns:
            df["Дата операции"] = pd.to_datetime(
                df["Дата операции"],
                format="%d.%m.%Y %H:%M:%S",
                errors="coerce"
            )
            df = df.dropna(subset=["Дата операции"])

        # Текстовые поля
        text_cols = ["Описание", "Категория"]
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str)

        # Числовые поля
        num_cols = ["Сумма операции", "Бонусы (включая кэшбэк)"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        return df

    except Exception as e:
        logger.error(f"Ошибка загрузки транзакций: {e}")
        return pd.DataFrame(columns=[
            "Дата операции",
            "Сумма операции",
            "Категория",
            "Описание"
        ])


def filter_transactions_by_date(
        df: pd.DataFrame,
        date_filter: Union[str, date, datetime],
        date_range: str = "M"
) -> pd.DataFrame:
    """
    Фильтрует транзакции по диапазону дат

    Args:
        df: DataFrame с транзакциями
        date_filter: Дата для фильтрации
        date_range: Диапазон ('D'-день, 'W'-неделя, 'M'-месяц, 'Y'-год, 'ALL'-все)

    Returns:
        Отфильтрованный DataFrame

    Raises:
        ValueError: При некорректных параметрах
    """
    try:
        if df.empty:
            return df

        # Преобразование даты фильтра
        if isinstance(date_filter, str):
            target_date = pd.to_datetime(date_filter).date()
        elif isinstance(date_filter, datetime):
            target_date = date_filter.date()
        else:
            target_date = date_filter

        # Проверка колонки с датами
        if not pd.api.types.is_datetime64_any_dtype(df["Дата операции"]):
            df["Дата операции"] = pd.to_datetime(
                df["Дата операции"],
                format="%d.%m.%Y %H:%M:%S",
                errors="coerce"
            )
            df = df.dropna(subset=["Дата операции"])

        df["operation_date"] = df["Дата операции"].dt.date

        # Определение диапазона
        if date_range == "W":
            start_date = target_date - timedelta(days=target_date.weekday())
            end_date = start_date + timedelta(days=6)
        elif date_range == "M":
            start_date = target_date.replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        elif date_range == "Y":
            start_date = target_date.replace(month=1, day=1)
            end_date = target_date.replace(month=12, day=31)
        elif date_range == "ALL":
            return df.drop(columns=["operation_date"])
        else:
            raise ValueError(f"Некорректный диапазон: {date_range}")

        # Фильтрация
        filtered = df[
            (df["operation_date"] >= start_date) &
            (df["operation_date"] <= end_date)
            ]
        return filtered.drop(columns=["operation_date"])

    except Exception as e:
        logger.error(f"Ошибка фильтрации: {e}")
        raise ValueError(f"Ошибка фильтрации: {e}")


def get_greeting(time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"

def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Возвращает курсы валют"""
    # В реальной реализации здесь должен быть API-запрос
    return [{"currency": c, "rate": 75.0 if c == "USD" else 90.0} for c in currencies]

def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Возвращает цены акций"""
    # В реальной реализации здесь должен быть API-запрос
    return [{"stock": s, "price": 150.0} for s in stocks]
