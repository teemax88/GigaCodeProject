# GIGACODE.md — Руководство проекта

## О проекте

Фреймворк автотестов на Python с использованием:
- **pytest** — фреймворк для запуска тестов
- **requests / httpx** — API-клиенты
- **playwright** — UI-тестирование (браузерная автоматизация)
- **allure-pytest** — отчёты
- **pydantic-settings** — типизированная конфигурация

---

## Архитектура проекта

```
test_framework/
├── conftest.py                  # Глобальные фикстуры pytest
├── pytest.ini                   # Конфигурация pytest
├── pyproject.toml               # Зависимости и настройки
├── requirements.txt
│
├── config/                      # Конфигурация
│   ├── __init__.py
│   ├── settings.py              # Pydantic Settings (env, .env)
│   └── environments/
│       ├── dev.env
│       ├── staging.env
│       └── prod.env
│
├── common/                      # Общий слой
│   ├── __init__.py
│   ├── base_api.py              # Базовый класс API-клиента
│   ├── base_page.py             # Базовый класс Page Object
│   ├── base_step.py             # Базовый класс шагов
│   ├── assertions.py            # Кастомные ассерты
│   ├── decorators.py            # Декораторы (@allure.step, логирование)
│   └── helpers/
│       ├── __init__.py
│       ├── file_utils.py        # Работа с файлами
│       ├── json_utils.py        # Работа с JSON
│       └── generators.py        # Генерация тестовых данных
│
├── logging_config/
│   ├── __init__.py
│   └── logger.py                # Настройка logging (файл + console)
│
├── data/                        # Тестовые данные
│   ├── __init__.py
│   ├── fixtures.json
│   ├── payloads/
│   │   ├── __init__.py
│   │   ├── auth_payloads.py     # Тела запросов авторизации
│   │   ├── user_payloads.py     # Тела запросов пользователей
│   │   └── ...
│   └── endpoints/
│       ├── __init__.py
│       ├── auth_endpoints.py    # Маршруты авторизации
│       ├── user_endpoints.py    # Маршруты пользователей
│       └── ...
│
├── api/                         # API слой
│   ├── __init__.py
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── auth_client.py       # Клиент авторизации
│   │   ├── user_client.py       # Клиент пользователей
│   │   └── base_client.py       # Базовый API клиент
│   └── tests/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_users.py
│       └── ...
│
├── ui/                          # UI слой
│   ├── __init__.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py         # Базовая страница
│   │   ├── login_page.py
│   │   ├── dashboard_page.py
│   │   └── ...
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── auth_steps.py
│   │   ├── user_steps.py
│   │   └── ...
│   └── tests/
│       ├── __init__.py
│       ├── test_login.py
│       ├── test_dashboard.py
│       └── ...
│
├── reports/
│   ├── allure/                  # Результаты Allure
│   └── logs/                    # Логи выполнения
│
└── tests/                       # Пусковые точки
    ├── test_api_smoke.py
    └── test_ui_smoke.py
```

---

## Ключевые принципы

### 1. Разделение API и UI
- **API** — подготовка данных, валидация ответов, проверка бизнес-логики
- **UI** — проверка UX, визуальных сценариев, интеграции с браузером
- UI-тесты используют API-клиенты для подготовки данных (например, создать пользователя через API, затем залогиниться в UI)

### 2. Централизация маршрутов и тел запросов
- `data/endpoints/` — все URL-маршруты в одном месте
- `data/payloads/` — все тела запросов в одном месте
- Изменение маршрута = правка в одном файле

### 3. Централизация локаторов
- Page Object Model: каждый элемент страницы — именованный локатор в классе страницы
- Базовый класс `BasePage` предоставляет методы `find_element()`, `find_elements()`, `click()`, `wait_for_visible()`

### 4. Логирование
- `logging_config/logger.py` — настройка logging с двумя handlers:
  - **FileHandler** — запись в `reports/logs/framework_YYYYMMDD.log`
  - **StreamHandler** — вывод в консоль
- Все шаги обернуты в `@allure.step` + логирование через `logger.info/debug`

### 5. Allure
- `@allure.epic/feature/story` — декораторы для иерархии
- `@allure.step("шаг")` — шаги внутри тестов
- `@allure.attach` — скриншоты, JSON, HTML
- `pytest-allure-adaptor` — интеграция с pytest

### 6. Конфигурация
- Pydantic Settings для типизированного конфига
- `.env` файлы для окружений
- Переключение окружением через `pytest --env=dev`

---

## Конвенции кодирования

### Именование файлов
- Тесты: `test_<функционал>.py`
- Клиенты: `<ресурс>_client.py`
- Страницы: `<имя>_page.py`
- Шаги: `<функционал>_steps.py`
- Данные: `<тип>_payloads.py`, `<ресурс>_endpoints.py`

### Именование классов
- Тесты: `Test<Функционал>` (PascalCase)
- Страницы: `<Имя>Page` (PascalCase)
- Клиенты: `<Имя>Client` (PascalCase)
- Шаги: `<Имя>Steps` (PascalCase)

### Именование функций/методов
- snake_case
- Тесты: `test_<описание>_<сценарий>` (например, `test_login_success`)
- Методы: `action_description` (например, `click_login_button`)

### Декорирование тестов
```python
@allure.epic("Эпик")
@allure.feature("Фича")
@allure.story("История")
@allure.severity(allure.severity_level.CRITICAL)  # BLOCKER/CRITICAL/NORMAL/MINOR/TRIVIAL
@allure.tag("api")  # или "ui", "smoke", "regression"
def test_...(self, ...):
    ...
```

### pytest-маркеры
- `@pytest.mark.smoke` — smoke-тесты
- `@pytest.mark.regression` — регрессионные тесты
- `@pytest.mark.api` — API-тесты
- `@pytest.mark.ui` — UI-тесты
- `@pytest.mark.slow` — медленные тесты

---

## Правила масштабирования

1. **Один маршрут = один файл в `data/endpoints/`**
2. **Один ресурс = один клиент в `api/clients/`**
3. **Одна страница = один Page Object в `ui/pages/`**
4. **Одна функциональность = один набор steps в `ui/steps/`**
5. **Одна тестовая область = один файл тестов**
6. **Все изменения локализуются в одном файле** — нет дублирования маршрутов/локаторов

---

## Команды для запуска

```bash
# Установка зависимостей
pip install -r requirements.txt
playwright install

# Запуск всех тестов
pytest -v

# Smoke-тесты
pytest -m smoke -v

# Только API
pytest -m api -v

# Только UI
pytest -m ui -v

# Allure report
allure serve reports/allure
```

---

## Основные зависимости

```
pytest>=8.0
pytest-asyncio>=0.24
pytest-playwright>=0.5
pytest-html>=4.0
allure-pytest>=2.13
allure-python-commons>=2.13
requests>=2.31
httpx>=0.27
playwright>=1.44
pydantic>=2.0
pydantic-settings>=2.0
python-dotenv>=1.0
loguru>=0.7
```

---

## Файлы конфигурации GigaCode

| Файл | Назначение |
|---|---|
| `GIGACODE.md` | Главный гайдлайн проекта (этот файл) |
| `AGENTS.md` | Инструкции для агентов/подзадач |
| `.gigacode_vsc/command/*.md` | Команды — наборы инструкций для конкретных сценариев |
| `.gigacode_vsc/agent/*.md` | Агенты — специализированные роли с набором правил |
| `.gigacode_vsc/skills/*.md` | Навыки — готовые шаблоны для конкретных задач |

---

## Примечания

- `.env` файлы не коммитить (использовать `.env.example`)
- Отчёты Allure генерируются в `reports/allure/`
- Логи сохраняются в `reports/logs/`
- Фикстуры для подготовки данных через API должны иметь teardown для очистки
