#!/usr/bin/env python3
"""
Упрощенный стартовый скрипт для Telegram Орфографа
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import Config
    from main import TelegramSpellChecker
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что установлены все зависимости:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def check_config():
    """Проверяет конфигурацию перед запуском"""
    try:
        Config.validate()
        print("✅ Конфигурация в порядке")
        return True
    except ValueError as e:
        print(f"❌ {e}")
        print("\nДля исправления:")
        print("1. Создайте файл .env на основе env_example.txt")
        print("2. Заполните OPENAI_API_KEY в файле .env")
        print("3. Запустите скрипт снова")
        return False

async def main():
    """Главная функция запуска"""
    print("🚀 Запуск Telegram Орфографа...")
    
    if not check_config():
        return
    
    checker = TelegramSpellChecker()
    
    try:
        await checker.start()
    except KeyboardInterrupt:
        print("\n⏹️  Остановка сервиса...")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        await checker.stop()
        print("👋 Сервис остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}") 