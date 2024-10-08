### Описание проекта

Этот проект представляет собой Telegram-бота, который управляет геймифицированным опытом для пользователей. Бот позволяет пользователям выполнять задания, проходить викторины, зарабатывать очки, а также участвовать в реферальной программе. Бот поддерживает несколько языков (русский и английский) и имеет возможность менять язык интерфейса.

### Основные функции:

- **Профиль пользователя**: Отображение текущего количества очков (яблок), которые заработал пользователь.
- **Задания**: Пользователи могут выполнять различные задания, например, подписаться на канал или пройти викторину, чтобы заработать очки.
- **Викторина**: Викторина с несколькими вопросами, правильные ответы на которые вознаграждаются очками.
- **Реферальная система**: Пользователи могут приглашать друзей и получать очки за каждого приглашенного, который выполнит задание.
- **Социальные сети**: Бот предоставляет ссылки на социальные сети проекта.
- **Доска почета**: Ежедневно обновляемый список лидеров по количеству очков.
- **Многоязычная поддержка**: Бот поддерживает русский и английский языки, с возможностью смены языка интерфейса.

### Структура проекта

Файлы проекта:

- **main.py**: Главный файл для запуска бота.
- **bot_handlers.py**: Содержит логику обработки команд и взаимодействия с пользователями.
- **bot_helpers.py**: Содержит вспомогательные функции для бота.
- **translations.py**: Содержит переводы для поддерживаемых языков.
- **config.py**: Содержит конфигурационные переменные, такие как `BOT_TOKEN` и `DB_PATH`.
- **database.py**: Модуль для работы с базой данных SQLite.
- **.env**: Файл для хранения конфиденциальных переменных окружения, таких как токен бота и путь к базе данных.
- **requirements.txt**: Список необходимых Python-библиотек для установки через pip.

### Запуск проекта

#### 1. Клонирование репозитория

Клонируйте репозиторий на свой локальный компьютер:

```bash
git clone https://github.com/ваш-репозиторий.git
```

#### 2. Установка зависимостей

Перейдите в директорию проекта и установите все необходимые библиотеки:

```bash
pip install -r requirements.txt
```

#### 3. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и укажите в нем следующие переменные:

```plaintext
BOT_TOKEN=ваш_telegram_bot_token
DB_PATH=путь_к_вашей_базе_данных/snake.db
```

#### 4. Запуск бота

Для запуска бота используйте команду:

```bash
python main.py
```

Теперь ваш Telegram-бот готов к работе! Если у вас возникнут какие-либо проблемы или вопросы, пожалуйста, откройте issue в репозитории или свяжитесь с разработчиком.
