# Тестирование проект Yatube

Стек:
- Python 3.10.5
- django-debug-toolbar 2.2
- django 2.2.28
- pytest-django 3.8.0
- pytest-pythonpath 0.7.3
- pytest 5.3.5
- requests 2.22.0
- six 1.14.0
- sorl-thumbnail 12.6.3
- mixer 7.1.2
- pillow==9.2.0
- Faker==7.0.0 (уточнить по версии, для Python 3.10.5)

### Настройка и запуск на ПК

Клонируем проект:

```bash
git clone https://github.com/oleiip/hw04_tests.git
```

или

```bash
git clone git@github.com:oleiip/hw04_tests.git
```

Переходим в папку с проектом:

```bash
cd hw04_tests
```

Устанавливаем виртуальное окружение:

```bash
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

> Для деактивации виртуального окружения выполним (после работы):
> ```bash
> deactivate
> ```
Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python yatube/manage.py makemigrations
python yatube/manage.py migrate
```

Создаем супер пользователя:

```bash
python yatube/manage.py createsuperuser
```


В папку с проектом, где файл settings.py добавляем файл .env куда прописываем наши параметры:

```bash
SECRET_KEY='Ваш секретный ключ'
ALLOWED_HOSTS='127.0.0.1, localhost'
DEBUG=True
```

Не забываем добавить в .gitingore файлы:

```bash
.env
.venv
```

Для запуска тестов выполним:

```bash
pytest
```
