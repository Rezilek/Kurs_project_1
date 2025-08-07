import json
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar

from pandas import DataFrame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Any)


def report_decorator(
    filename: Optional[str] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Декоратор для сохранения отчетов"""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                result = func(*args, **kwargs)

                if filename:
                    report_data = {
                        "function": func.__name__,
                        "timestamp": datetime.now().isoformat(),
                        "args": str(args),
                        "kwargs": str(kwargs),
                        "result": str(result),
                    }

                    with open(filename, "a", encoding="utf-8") as f:
                        json.dump(report_data, f, ensure_ascii=False)
                        f.write("\n")

                return result
            except Exception as e:
                logger.error(f"Ошибка в {func.__name__}: {e}")
                raise

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: DataFrame, category: str) -> Dict[str, float]:
    """
    Рассчитывает расходы по указанной категории

    Args:
        transactions: DataFrame с транзакциями
        category: Категория для анализа

    Returns:
        Словарь {дата: сумма}
    """
    try:
        if (
            "Категория" not in transactions.columns
            or "Дата операции" not in transactions.columns
        ):
            return {}

        filtered = transactions[transactions["Категория"] == category]
        if filtered.empty:
            return {}

        return {
            str(k.date()): float(v)
            for k, v in filtered.groupby("Дата операции")["Сумма операции"]
            .sum()
            .to_dict()
            .items()
        }
    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {e}")
        return {}


@report_decorator()
def spending_by_weekday(transactions: DataFrame) -> Dict[int, float]:
    """
    Анализирует расходы по дням недели

    Args:
        transactions: DataFrame с транзакциями

    Returns:
        Словарь {день_недели: сумма} (0-пн, 6-вс)
    """
    try:
        if "Дата операции" not in transactions.columns:
            return {}

        transactions = transactions.copy()
        transactions["weekday"] = transactions["Дата операции"].dt.weekday
        return {
            int(k): float(v)
            for k, v in transactions.groupby("weekday")["Сумма операции"]
            .sum()
            .to_dict()
            .items()
        }
    except Exception as e:
        logger.error(f"Ошибка в spending_by_weekday: {e}")
        return {}


@report_decorator(filename="workday_spending_report.json")
def spending_by_workday(transactions: DataFrame) -> Dict[str, float]:
    """
    Сравнивает расходы в рабочие дни и выходные

    Args:
        transactions: DataFrame с транзакциями

    Returns:
        Словарь {'weekdays': сумма, 'weekends': сумма}
    """
    try:
        if "Дата операции" not in transactions.columns:
            return {"weekdays": 0.0, "weekends": 0.0}

        transactions = transactions.copy()
        transactions["is_weekday"] = transactions["Дата операции"].dt.weekday < 5
        grouped = transactions.groupby("is_weekday")["Сумма операции"].sum()
        return {
            "weekdays": float(grouped.get(True, 0)),
            "weekends": float(grouped.get(False, 0)),
        }
    except Exception as e:
        logger.error(f"Ошибка в spending_by_workday: {e}")
        return {"weekdays": 0.0, "weekends": 0.0}
