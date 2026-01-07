<p align="center">
  <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/GPT--5.2-412991?style=for-the-badge&logo=openai&logoColor=white" alt="GPT-5.2"/>
</p>

<h1 align="center">🔤 Telegram Spell Checker</h1>

<p align="center">
  <b>Автоматическая проверка орфографии в Telegram с помощью GPT-5.2</b>
</p>

<p align="center">
  <a href="#-возможности">Возможности</a> •
  <a href="#-быстрый-старт">Быстрый старт</a> •
  <a href="#-установка">Установка</a> •
  <a href="#-использование">Использование</a>
</p>

---

## 📋 Описание

Сервис автоматически проверяет и исправляет орфографические ошибки в ваших исходящих сообщениях Telegram в реальном времени, используя GPT-5.2.

**Как это работает:**
1. Вы отправляете сообщение в любом клиенте Telegram
2. Сервис перехватывает сообщение и отправляет в GPT-5.2
3. Если найдены ошибки — сообщение автоматически редактируется

---

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| ⚡ Реальное время | Мгновенная проверка каждого сообщения |
| 🤖 GPT-5.2 | Самая передовая модель для точной проверки |
| ✏️ Автоисправление | Автоматическое редактирование сообщений |
| 🔗 Защита ссылок | URL, @username, #хештеги не изменяются |
| 📝 Логирование | Подробные логи всех операций |

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

# 4. Заполните .env своими ключами

# 5. Запустите
python start.py
```

---

## 📦 Установка

### Требования

- **Python** 3.8+
- **Telegram API ключи** ([my.telegram.org](https://my.telegram.org))
- **OpenAI API ключ** ([platform.openai.com](https://platform.openai.com/api-keys))

### Шаг 1: Клонирование

```bash
git clone https://github.com/kpshinnik/tg_checker.git
cd tg_checker
```

### Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 3: Получение API ключей

#### 🔑 Telegram API

1. Перейдите на [my.telegram.org](https://my.telegram.org)
2. Войдите в аккаунт → **API development tools**
3. Создайте приложение
4. Скопируйте **api_id** и **api_hash**

#### 🤖 OpenAI API

1. Зарегистрируйтесь на [platform.openai.com](https://platform.openai.com)
2. Перейдите в [API Keys](https://platform.openai.com/api-keys)
3. Создайте и скопируйте ключ

### Шаг 4: Настройка .env

```bash
cp env_example.txt .env
```

Заполните файл `.env`:

```env
TELEGRAM_API_ID=ваш_api_id
TELEGRAM_API_HASH=ваш_api_hash
OPENAI_API_KEY=ваш_openai_ключ
```

---

## 💻 Использование

### Запуск

```bash
python start.py
```

### Первый запуск

1. Введите номер телефона (`+79001234567`)
2. Введите код из Telegram
3. Введите пароль 2FA (если есть)

### Работа сервиса

```
📤 Вы отправили: "Привет, как дила?"
🔍 GPT-5.2 проверяет...
✅ Исправлено: "Привет, как дела?"
```

### Остановка

Нажмите `Ctrl+C`

---

## 🛡️ Защищенные элементы

Следующие элементы **никогда не изменяются**:

| Тип | Пример |
|-----|--------|
| HTTP/HTTPS | `https://example.com` |
| Telegram | `t.me/channel` |
| Username | `@username` |
| Хештеги | `#hashtag` |
| Домены | `example.com` |

---

## ⚙️ Настройки

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `TELEGRAM_API_ID` | ID приложения Telegram | — |
| `TELEGRAM_API_HASH` | Hash приложения | — |
| `OPENAI_API_KEY` | Ключ OpenAI API | — |
| `CHECK_DELAY` | Задержка проверки (сек) | `1.0` |
| `MAX_MESSAGE_LENGTH` | Макс. длина сообщения | `2000` |

---

## 🔧 Решение проблем

### ❌ Ошибка авторизации Telegram

- Номер в формате `+79001234567`
- Проверьте код подтверждения
- При 2FA введите пароль

### ❌ Ошибка OpenAI API

- Проверьте правильность ключа
- Убедитесь, что есть средства на балансе

### ❌ Сообщения не исправляются

- Проверьте, что сервис запущен
- Telegram позволяет редактировать только 48 часов
- Проверьте логи

---

## 📁 Структура проекта

```
tg_checker/
├── main.py           # Основной модуль
├── config.py         # Конфигурация
├── start.py          # Скрипт запуска
├── requirements.txt  # Зависимости
├── env_example.txt   # Пример .env
└── .gitignore        # Игнорируемые файлы
```

---

## ⚠️ Важно

- 🔒 Не публикуйте `.env` с реальными ключами
- 💰 OpenAI API платный ([pricing](https://openai.com/pricing))
- 📜 Используйте на свой страх и риск

---

<p align="center">
  Сделано с ❤️ для грамотного общения в Telegram
</p>
