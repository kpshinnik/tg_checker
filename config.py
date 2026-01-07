import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Класс для хранения конфигурации приложения"""
    
    # Telegram API настройки
    API_ID = int(os.getenv('TELEGRAM_API_ID', '0'))
    API_HASH = os.getenv('TELEGRAM_API_HASH', '')
    
    # OpenAI API настройки
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Настройки проверки
    CHECK_DELAY = float(os.getenv('CHECK_DELAY', '1.0'))  # Задержка перед проверкой (сек)
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '2000'))  # Максимальная длина сообщения для проверки
    
    @classmethod
    def validate(cls):
        """Проверяет, что все необходимые настройки заданы"""
        errors = []
        
        if not cls.API_ID:
            errors.append("TELEGRAM_API_ID не задан")
            
        if not cls.API_HASH:
            errors.append("TELEGRAM_API_HASH не задан")
            
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY не задан")
            
        if errors:
            raise ValueError(f"Ошибки конфигурации: {', '.join(errors)}")
            
        return True 