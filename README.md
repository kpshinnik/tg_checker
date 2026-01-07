<p align="center">
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI"/>
</p>

<h1 align="center">🔤 Telegram Spell Checker & History Exporter</h1>

<p align="center">
  <b>Умный помощник для Telegram: автоматическая проверка орфографии + экспорт истории чатов</b>
</p>

<p align="center">
  <a href="#-возможности">Возможности</a> •
  <a href="#-быстрый-старт">Быстрый старт</a> •
  <a href="#-установка">Установка</a> •
  <a href="#-использование">Использование</a> •
  <a href="#-конфигурация">Конфигурация</a>
</p>

---

## 📋 Описание

Этот проект содержит два мощных инструмента для работы с Telegram:

### 🔤 Spell Checker (Орфограф)
Автоматически проверяет и исправляет орфографические ошибки в ваших исходящих сообщениях в реальном времени, используя GPT-4.

### 📤 History Exporter (Экспортер истории)
Выгружает полную историю переписок в структурированном JSON формате с сохранением всех медиафайлов.

---

## ✨ Возможности

### 🔤 Орфограф
| Функция | Описание |
|---------|----------|
| ⚡ Реальное время | Мгновенная проверка каждого отправленного сообщения |
| 🤖 GPT-4 | Использование передовой модели для точной проверки |
| ✏️ Автоисправление | Автоматическое редактирование сообщений с ошибками |
| 🔗 Защита ссылок | URL, @username, #хештеги никогда не изменяются |
| 📝 Логирование | Подробные логи всех операций |

### 📤 Экспортер истории
| Функция | Описание |
|---------|----------|
| 📁 Полный экспорт | Все чаты, группы и каналы |
| 🗂️ Структура | Папки `nickname_ID` для каждого чата |
| 📊 JSON формат | Поля `input`/`output` с временными метками |
| 🖼️ Медиафайлы | Автоматическая загрузка фото, видео, аудио |
| ⚙️ Фильтры | Настройка типов чатов и размера файлов |

---

## 🚀 Быстрый старт

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/kpshinnik/tg_checker.git
cd tg_checker

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Создайте .env файл
cp env_example.txt .env

# 4. Заполните .env своими ключами (см. раздел Конфигурация)

# 5. Запустите нужный инструмент
python start.py          # Орфограф
python start_export.py   # Экспорт истории
```

---

## 📦 Установка

### Требования

- **Python** 3.8 или выше
- **Telegram аккаунт**
- **Telegram API ключи** (api_id и api_hash)
- **OpenAI API ключ** (только для орфографа)

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/kpshinnik/tg_checker.git
cd tg_checker
```

### Шаг 2: Создание виртуального окружения (рекомендуется)

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Linux/macOS)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 4: Получение API ключей

#### 🔑 Telegram API (обязательно)

1. Перейдите на [my.telegram.org](https://my.telegram.org)
2. Войдите в свой аккаунт
3. Перейдите в раздел **"API development tools"**
4. Создайте новое приложение
5. Скопируйте **api_id** и **api_hash**

#### 🤖 OpenAI API (для орфографа)

1. Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
2. Перейдите в раздел [API Keys](https://platform.openai.com/api-keys)
3. Создайте новый ключ
4. Скопируйте ключ (он показывается только один раз!)

### Шаг 5: Настройка переменных окружения

```bash
# Скопируйте пример конфигурации
cp env_example.txt .env
```

Откройте файл `.env` и заполните его:

```env
# Обязательные настройки
TELEGRAM_API_ID=ваш_api_id
TELEGRAM_API_HASH=ваш_api_hash
OPENAI_API_KEY=ваш_openai_ключ

# Опциональные настройки (можно оставить по умолчанию)
CHECK_DELAY=1.0
MAX_MESSAGE_LENGTH=2000
EXPORT_HOURS_BACK=48
DOWNLOAD_MEDIA=true
```

---

## 💻 Использование

### 🔤 Орфограф

Запустите скрипт:

```bash
python start.py
```

**При первом запуске:**
1. Введите номер телефона в международном формате (`+79001234567`)
2. Введите код подтверждения из Telegram
3. Если включена 2FA — введите пароль

**После авторизации:**
- Сервис работает в фоновом режиме
- Автоматически проверяет все ваши исходящие сообщения
- Исправляет ошибки через редактирование

**Остановка:** нажмите `Ctrl+C`

#### Пример работы:

```
📤 Вы отправили: "Привет, как дила?"
🔍 GPT-4 проверяет...
✅ Исправлено на: "Привет, как дела?"
```

#### Защищенные элементы (не изменяются):

| Тип | Пример |
|-----|--------|
| HTTP/HTTPS ссылки | `https://example.com` |
| WWW ссылки | `www.example.com` |
| Telegram ссылки | `t.me/channel` |
| Username | `@username` |
| Хештеги | `#hashtag` |
| Домены | `example.com` |

---

### 📤 Экспорт истории

Запустите скрипт:

```bash
python start_export.py
```

**Интерактивный запуск:**
```
🗂️  Экспорт истории Telegram
==================================================
✅ Конфигурация экспорта в порядке
📋 Текущие настройки экспорта:
----------------------------------------
⏰ Период экспорта: 48 часов назад
📁 Папка сохранения: history
📥 Скачивание медиа: ✅
📊 Макс. размер файла: 50 МБ
----------------------------------------

🚀 Начать экспорт? (y/N): y
```

#### Структура экспорта:

```
history/
├── john_doe_123456789/           # Личный чат (username_id)
│   ├── messages_20240120_153045.json
│   └── media/
│       ├── 12345_photo_20240120_142700.jpg
│       └── 12346_audio_20240120_143000.mp3
│
├── _987654321/                   # Чат без username (_id)
│   ├── messages_20240120_153045.json
│   └── media/
│
└── awesome_group_555666777/      # Группа
    ├── messages_20240120_153045.json
    └── media/
```

#### Формат JSON:

```json
{
  "chat_info": {
    "folder_name": "john_doe_123456789",
    "export_date": "2024-01-20T15:30:45",
    "time_range": {
      "from": "2024-01-18T15:30:45",
      "to": "2024-01-20T15:30:45",
      "hours_back": 48
    },
    "total_messages": 42
  },
  "messages": [
    {
      "id": 12345,
      "date": "2024-01-20T14:25:30",
      "text": "Привет!",
      "direction": "output",
      "is_outgoing": true,
      "media": { "has_media": false }
    },
    {
      "id": 12346,
      "date": "2024-01-20T14:26:15",
      "text": "Привет! Как дела?",
      "direction": "input",
      "is_outgoing": false,
      "media": { "has_media": false }
    }
  ]
}
```

---

## ⚙️ Конфигурация

### Все переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| **Обязательные** |||
| `TELEGRAM_API_ID` | ID приложения Telegram | — |
| `TELEGRAM_API_HASH` | Hash приложения Telegram | — |
| `OPENAI_API_KEY` | Ключ OpenAI API | — |
| **Орфограф** |||
| `CHECK_DELAY` | Задержка перед проверкой (сек) | `1.0` |
| `MAX_MESSAGE_LENGTH` | Макс. длина сообщения | `2000` |
| **Экспорт** |||
| `EXPORT_HOURS_BACK` | Период экспорта (часы) | `48` |
| `DOWNLOAD_MEDIA` | Скачивать медиафайлы | `true` |
| `MAX_FILE_SIZE_MB` | Макс. размер файла (МБ) | `50` |
| `EXPORT_BASE_DIR` | Папка для экспорта | `history` |
| `EXPORT_PRIVATE_CHATS` | Экспорт личных чатов | `true` |
| `EXPORT_GROUPS` | Экспорт групп | `true` |
| `EXPORT_CHANNELS` | Экспорт каналов | `true` |

### Пример .env файла

```env
# === TELEGRAM API ===
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef

# === OPENAI API ===
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# === ОРФОГРАФ ===
CHECK_DELAY=1.0
MAX_MESSAGE_LENGTH=2000

# === ЭКСПОРТ ===
EXPORT_HOURS_BACK=48
DOWNLOAD_MEDIA=true
MAX_FILE_SIZE_MB=50
EXPORT_BASE_DIR=history
EXPORT_PRIVATE_CHATS=true
EXPORT_GROUPS=true
EXPORT_CHANNELS=false
```

---

## 🔧 Решение проблем

### ❌ Ошибка авторизации Telegram

```
Проблема: FloodWaitError / Неверный код
```

**Решение:**
- Убедитесь, что номер телефона в формате `+79001234567`
- Подождите указанное время при FloodWait
- Проверьте код подтверждения (SMS или в приложении)
- При 2FA введите правильный пароль

### ❌ Ошибка OpenAI API

```
Проблема: AuthenticationError / RateLimitError
```

**Решение:**
- Проверьте правильность API ключа
- Убедитесь, что есть средства на балансе OpenAI
- При RateLimitError — подождите и повторите

### ❌ Сообщения не исправляются

```
Проблема: Сообщения отправляются, но не исправляются
```

**Решение:**
- Проверьте, что сервис запущен (`python start.py`)
- Telegram позволяет редактировать сообщения только 48 часов
- Проверьте логи на наличие ошибок

### ❌ Медиафайлы не скачиваются

```
Проблема: В JSON нет путей к файлам
```

**Решение:**
- Проверьте `DOWNLOAD_MEDIA=true` в `.env`
- Убедитесь, что файл не превышает `MAX_FILE_SIZE_MB`
- Проверьте права на запись в папку `history`

---

## 📁 Структура проекта

```
tg_checker/
├── 📄 main.py              # Основной модуль орфографа
├── 📄 config.py            # Конфигурация орфографа
├── 📄 start.py             # Скрипт запуска орфографа
│
├── 📄 export_history.py    # Модуль экспорта истории
├── 📄 export_config.py     # Конфигурация экспорта
├── 📄 start_export.py      # Скрипт запуска экспорта
│
├── 📄 requirements.txt     # Зависимости Python
├── 📄 env_example.txt      # Пример .env файла
├── 📄 .gitignore           # Игнорируемые файлы
└── 📄 README.md            # Документация
```

---

## ⚠️ Важные замечания

### 🔒 Безопасность

- **Никогда** не публикуйте файл `.env` с реальными ключами
- Файлы сессий (`*.session`) содержат авторизационные данные
- Храните API ключи в безопасном месте

### 💰 Стоимость

- **OpenAI API** — платный (см. [pricing](https://openai.com/pricing))
- **Telegram API** — бесплатный
- Каждое сообщение = 1 запрос к GPT-4

### 📜 Лицензия

Проект создан в образовательных целях. Используйте на свой страх и риск.

---

## 🤝 Контрибьютинг

Приветствуются Pull Requests и Issues! 

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/amazing`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing`)
5. Откройте Pull Request

---

<p align="center">
  Сделано с ❤️ для удобной работы с Telegram
</p>
