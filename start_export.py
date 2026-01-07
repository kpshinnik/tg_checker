#!/usr/bin/env python3
"""
Скрипт запуска экспорта истории Telegram
"""

import asyncio
import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from export_config import ExportConfig
    from export_history import TelegramHistoryExporter
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что установлены все зависимости:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def show_config():
    """Показывает текущую конфигурацию экспорта"""
    config = ExportConfig()
    
    print("📋 Текущие настройки экспорта:")
    print("-" * 40)
    print(f"⏰ Период экспорта: {config.EXPORT_HOURS_BACK} часов назад")
    print(f"📁 Папка сохранения: {config.EXPORT_BASE_DIR}")
    print(f"📥 Скачивание медиа: {'✅' if config.DOWNLOAD_MEDIA else '❌'}")
    
    if config.DOWNLOAD_MEDIA:
        print(f"📊 Макс. размер файла: {config.MAX_FILE_SIZE_MB} МБ")
    
    print("\n🎯 Типы чатов для экспорта:")
    print(f"👤 Личные чаты: {'✅' if config.EXPORT_PRIVATE_CHATS else '❌'}")
    print(f"👥 Группы: {'✅' if config.EXPORT_GROUPS else '❌'}")
    print(f"📢 Каналы: {'✅' if config.EXPORT_CHANNELS else '❌'}")
    print("-" * 40)

def check_config():
    """Проверяет конфигурацию перед запуском"""
    try:
        ExportConfig.validate()
        print("✅ Конфигурация экспорта в порядке")
        return True
    except ValueError as e:
        print(f"❌ {e}")
        print("\nДля исправления:")
        print("1. Убедитесь что в файле .env указаны API ключи Telegram")
        print("2. Проверьте настройки экспорта в файле .env")
        return False

async def main():
    """Главная функция запуска экспорта"""
    print("🗂️  Экспорт истории Telegram")
    print("=" * 50)
    
    if not check_config():
        return
    
    show_config()
    
    # Проверяем существование папки экспорта
    export_dir = Path(ExportConfig.EXPORT_BASE_DIR)
    if export_dir.exists():
        print(f"\n📁 Папка '{export_dir}' уже существует")
        existing_files = list(export_dir.rglob('*.json'))
        if existing_files:
            print(f"🗃️  Найдено {len(existing_files)} существующих файлов экспорта")
    
    # Запрашиваем подтверждение
    try:
        confirm = input("\n🚀 Начать экспорт? (y/N): ").lower().strip()
        if confirm != 'y':
            print("❌ Экспорт отменен")
            return
    except KeyboardInterrupt:
        print("\n❌ Экспорт отменен")
        return
    
    # Запускаем экспорт
    exporter = TelegramHistoryExporter()
    
    try:
        await exporter.export_all_chats(exporter.config.EXPORT_HOURS_BACK)
        print("\n🎉 Экспорт успешно завершен!")
        
        # Показываем статистику
        export_dir = Path(exporter.config.EXPORT_BASE_DIR)
        if export_dir.exists():
            json_files = list(export_dir.rglob('*.json'))
            media_files = list(export_dir.rglob('media/*'))
            folders = [d for d in export_dir.iterdir() if d.is_dir()]
            
            print(f"📊 Статистика экспорта:")
            print(f"   📁 Папок с чатами: {len(folders)}")
            print(f"   📄 JSON файлов: {len(json_files)}")
            print(f"   🖼️  Медиафайлов: {len(media_files)}")
            
            # Размер экспорта
            total_size = sum(f.stat().st_size for f in export_dir.rglob('*') if f.is_file())
            size_mb = total_size / (1024 * 1024)
            print(f"   💾 Общий размер: {size_mb:.1f} МБ")
        
    except KeyboardInterrupt:
        print("\n⏹️  Экспорт прерван пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка при экспорте: {e}")
    finally:
        await exporter.stop()
        print("👋 Экспорт завершен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 До свидания!")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}") 