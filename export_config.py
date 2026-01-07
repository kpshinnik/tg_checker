import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class ExportConfig:
    """Класс для конфигурации экспорта истории"""
    
    # Telegram API настройки для второго аккаунта
    # Можно использовать те же API ключи, но с другой сессией
    API_ID = int(os.getenv('EXPORT_API_ID', os.getenv('TELEGRAM_API_ID', '0')))
    API_HASH = os.getenv('EXPORT_API_HASH', os.getenv('TELEGRAM_API_HASH', ''))
    
    # Настройки экспорта
    EXPORT_HOURS_BACK = int(os.getenv('EXPORT_HOURS_BACK', '48'))  # Количество часов назад
    DOWNLOAD_MEDIA = os.getenv('DOWNLOAD_MEDIA', 'true').lower() == 'true'  # Скачивать ли медиафайлы
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '50'))  # Максимальный размер файла для скачивания (МБ)
    
    # Фильтры экспорта
    EXPORT_PRIVATE_CHATS = os.getenv('EXPORT_PRIVATE_CHATS', 'true').lower() == 'true'
    EXPORT_GROUPS = os.getenv('EXPORT_GROUPS', 'true').lower() == 'true'
    EXPORT_CHANNELS = os.getenv('EXPORT_CHANNELS', 'true').lower() == 'true'
    
    # Путь для сохранения
    EXPORT_BASE_DIR = os.getenv('EXPORT_BASE_DIR', 'history')
    
    @classmethod
    def validate(cls):
        """Проверяет, что все необходимые настройки заданы"""
        errors = []
        
        if not cls.API_ID:
            errors.append("API_ID не задан")
            
        if not cls.API_HASH:
            errors.append("API_HASH не задан")
            
        if errors:
            raise ValueError(f"Ошибки конфигурации экспорта: {', '.join(errors)}")
            
        return True 