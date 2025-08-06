# Bank Transactions Analysis System

## Описание проекта

Система для анализа банковских транзакций с возможностью:
- Просмотра статистики расходов
- Поиска транзакций
- Анализа кэшбэка
- Формирования отчетов
- Визуализации данных на главной странице

## Технологии

- Python 3.13
- Pandas 2.2.0 (для работы с данными)
- OpenPyXL 3.0.9 (для чтения Excel файлов)
- Pytest 7.4.0 (для тестирования)
- Mypy 1.10.0 (для проверки типов)
- Flake8 6.0.0 (для проверки стиля кода)

## Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/bank-transactions-analysis.git
cd bank-transactions-analysis
```

2. Установить зависимости:
```bash
pip install poetry
poetry install
```

3. Создать файл `.env` на основе `.env.template`:
```bash
cp .env.template .env
```

## Структура проекта

```
bank-transactions-analysis/
├── data/
│ └── operations.xlsx - файл с транзакциями
├── src/
│ ├── __init__.py - основной модуль
│ ├── config.py - конфигурация

│ ├── reports.py - отчеты
│ ├── services.py - сервисы
│ ├── utils.py - утилиты
│ └── views.py - представления
├── tests/
│ ├── test_reports.py
│ ├── test_services.py
│ ├── test_utils.py
│ └── test_views.py
├── .env.template - шаблон конфига
├── main.py - точка входа
├── pyproject.toml - зависимости
└── README.md - документация
```

## Основные функции

### Отчеты (`reports.py`)
- `spending_by_category()` - расходы по категориям
- `spending_by_weekday()` - расходы по дням недели
- `spending_by_workday()` - сравнение расходов в будни/выходные

### Сервисы (`services.py`)
- `profitable_cashback_categories()` - категории с максимальным кэшбэком
- `investment_bank()` - расчет инвестиционных накоплений
- `simple_search()` - поиск транзакций по описанию
- `phone_number_search()` - поиск транзакций с номерами телефонов
- `person_transfers_search()` - поиск переводов между физлицами

### Представления (`views.py`)
- `home_page()` - данные для главной страницы
- `events_page()` - данные страницы событий

## Запуск

1. Запуск основного скрипта:
```bash
poetry run python main.py
```

2. Запуск тестов:
```bash
poetry run pytest --cov=src/ --cov-report=html
```

3. Проверка типов:
```bash
poetry run mypy src/ tests/
```

4. Проверка стиля:
```bash
poetry run flake8 src/ tests/
```

## Примеры использования

### Получение данных для главной страницы
```python
from src.views import home_page

data = home_page("2023-05-15 14:30:00")
print(data)
```

### Анализ расходов по категориям
```python
from src.reports import spending_by_category
from src.utils import load_transactions

df = load_transactions()
result = spending_by_category(df, "Супермаркеты")
print(result)
```

### Поиск переводов между физлицами
```python
from src.services import person_transfers_search
from src.utils import load_transactions

transactions = load_transactions().to_dict('records')
result = person_transfers_search(transactions)
print(result)
```

## Тестирование

Основные тесты:

- Модульные тесты для всех функций
- Тесты обработки ошибок
- Тесты граничных случаев
- Интеграционные тесты для главных компонентов

Запуск тестов с покрытием:
```bash
pytest --cov=src/ --cov-report=html
```

## Лицензия

MIT License
