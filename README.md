# 🐕 Структура проекта Dog Dating Project

## 📋 Обзор проекта

Django веб-приложение для знакомства собак с красивой архитектурой и модульной структурой.

---

## 🌳 Основная структура директорий

```
dog_dating_project/
├── 📄 manage.py                    # Точка входа Django проекта
├── 📄 README.md                    # Документация проекта
├── 📄 requirements.txt             # Зависимости Python
├── 📁 dogs/                        # 🐕 Основное приложение для собак
├── 📁 menu_app/                    # 🍽️ Приложение для управления меню
├── 📁 project/                     # ⚙️ Конфигурация Django проекта
├── 📁 .github/                     # 🔧 GitHub конфигурация
└── 📁 .vscode/                     # 🛠️ VS Code настройки
```

---

## 📁 Приложения проекта

### 🐕 **dogs/** - Основное приложение для собак

```
dogs/
├── __init__.py                     # Python пакет
├── apps.py                         # Конфигурация приложения
├── models.py                       # 🗄️ Модели данных (собаки, породы)
├── urls.py                         # 🛣️ Маршруты URL
├── views.py                        # 👁️ Контроллеры (представления)
└── templates/
    └── dogs/
        └── base.html               # 🎨 Базовый шаблон для собачьего приложения
```

### 🍽️ **menu_app/** - Приложение для меню

```
menu_app/
├── __init__.py
├── admin.py                        # 👨‍💼 Админ-панель для меню
├── apps.py
├── models.py                       # 📊 Модели для меню
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── setup_menus.py          # 🚀 Команда для настройки меню
├── templates/
│   └── menu/
│       ├── menu.html               # 📋 Шаблон главного меню
│       └── menu_item.html          # 📄 Шаблон элемента меню
└── templatetags/
    └── menu_tags.py                # 🏷️ Пользовательские теги шаблонов
```

### ⚙️ **project/** - Конфигурация Django

```
project/
├── __init__.py
├── __pycache__/                    # 🗂️ Python кэш (исключен из анализа)
├── asgi.py                         # 🌐 ASGI конфигурация
├── settings.py                     # ⚙️ Основные настройки проекта
├── urls.py                         # 🛣️ Главные маршруты
└── wsgi.py                         # 🔌 WSGI конфигурация
```

---

## 🛠️ Конфигурационные файлы

### 🔧 **.github/workflows/test.yml**

```yaml
# GitHub Actions для автоматического тестирования
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: python manage.py test
```

### 🛠️ **.vscode/**

- `launch.json` - Конфигурация отладки
- `settings.json` - Настройки VS Code

---

## 🎯 Ключевые особенности архитектуры

### ✅ **Модульность**

- Разделение функциональности на отдельные приложения
- Четкое разделение ответственности между компонентами

### ✅ **Шаблоны**

- Использование Django Templates для рендеринга
- Базовые шаблоны для переиспользования кода
- Пользовательские теги шаблонов для меню

### ✅ **Администрирование**

- Настроенная админ-панель для управления данными
- Команды для автоматической настройки

### ✅ **CI/CD**

- GitHub Actions для автоматического тестирования
- Готовая инфраструктура для развертывания

### ✅ **Разработка**

- Настройки VS Code для удобной разработки
- Виртуальное окружение для изоляции зависимостей

---

## 📦 Зависимости проекта

### Основные пакеты (из requirements.txt)

- **Django** - Веб-фреймворк
- **Дополнительные зависимости** - указаны в файле requirements.txt

---

## 🚀 Запуск проекта

```bash
# Активация виртуального окружения
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver
```

---

## 📝 Примечания

- Файлы `__pycache__/` исключены для читаемости
- Git объекты и виртуальное окружение не показаны
- Структура оптимизирована для понимания архитектуры проекта
- Все основные компоненты имеют описания и назначение
