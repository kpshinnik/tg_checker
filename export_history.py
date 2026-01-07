#!/usr/bin/env python3
"""
Скрипт для выгрузки истории переписок из Telegram
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

from telethon import TelegramClient
from telethon.tl.types import (
    Message, User, Chat, Channel, 
    MessageMediaPhoto, MessageMediaDocument, 
    MessageMediaContact, MessageMediaGeo
)
from export_config import ExportConfig

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramHistoryExporter:
    def __init__(self):
        self.config = ExportConfig()
        self.client = TelegramClient(
            'export_session',  # Отдельная сессия для экспорта
            self.config.API_ID,
            self.config.API_HASH
        )
        self.base_dir = Path(self.config.EXPORT_BASE_DIR)
        self.base_dir.mkdir(exist_ok=True)
        
    def get_safe_filename(self, text: str) -> str:
        """Создает безопасное имя файла из текста"""
        # Удаляем опасные символы
        safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
        safe_name = ''.join(c for c in text if c in safe_chars)
        return safe_name[:50]  # Ограничиваем длину
    
    def get_chat_folder_name(self, entity) -> str:
        """Определяет имя папки для чата"""
        if isinstance(entity, User):
            username = entity.username or ""
            if username:
                return f"{self.get_safe_filename(username)}_{entity.id}"
            else:
                first_name = entity.first_name or ""
                last_name = entity.last_name or ""
                full_name = f"{first_name}_{last_name}".strip('_')
                if full_name:
                    return f"{self.get_safe_filename(full_name)}_{entity.id}"
                return f"_{entity.id}"
        elif isinstance(entity, Chat):
            title = entity.title or ""
            if title:
                return f"{self.get_safe_filename(title)}_{entity.id}"
            return f"chat_{entity.id}"
        elif isinstance(entity, Channel):
            title = entity.title or ""
            username = entity.username or ""
            if username:
                return f"{self.get_safe_filename(username)}_{entity.id}"
            elif title:
                return f"{self.get_safe_filename(title)}_{entity.id}"
            return f"channel_{entity.id}"
        else:
            return f"unknown_{getattr(entity, 'id', 'noId')}"
    
    async def download_media(self, message: Message, chat_folder: Path) -> Optional[str]:
        """Скачивает медиафайл и возвращает путь к нему"""
        try:
            if not message.media or not self.config.DOWNLOAD_MEDIA:
                return None
                
            # Проверяем размер файла
            file_size = 0
            if isinstance(message.media, MessageMediaDocument) and message.media.document:
                file_size = message.media.document.size
                max_size = self.config.MAX_FILE_SIZE_MB * 1024 * 1024  # Переводим в байты
                
                if file_size > max_size:
                    logger.warning(f"Файл слишком большой ({file_size / (1024*1024):.1f} МБ), пропускаем")
                    return None
                
            media_folder = chat_folder / 'media'
            media_folder.mkdir(exist_ok=True)
            
            # Определяем тип медиа и расширение
            file_ext = ''
            file_prefix = f"{message.id}_"
            
            if isinstance(message.media, MessageMediaPhoto):
                file_ext = '.jpg'
                file_prefix += 'photo_'
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document:
                    # Пытаемся получить оригинальное расширение
                    for attr in message.media.document.attributes:
                        if hasattr(attr, 'file_name') and attr.file_name:
                            original_ext = Path(attr.file_name).suffix
                            if original_ext:
                                file_ext = original_ext
                                break
                    if not file_ext:
                        # Определяем тип по mime_type
                        mime_type = getattr(message.media.document, 'mime_type', '')
                        if 'audio' in mime_type:
                            file_ext = '.mp3'
                            file_prefix += 'audio_'
                        elif 'video' in mime_type:
                            file_ext = '.mp4'
                            file_prefix += 'video_'
                        elif 'image' in mime_type:
                            file_ext = '.png'
                            file_prefix += 'image_'
                        else:
                            file_ext = '.bin'
                            file_prefix += 'doc_'
                    else:
                        file_prefix += 'doc_'
            else:
                file_ext = '.bin'
                file_prefix += 'media_'
            
            filename = f"{file_prefix}{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
            file_path = media_folder / filename
            
            # Скачиваем файл
            await self.client.download_media(message, file_path)
            
            # Возвращаем относительный путь
            return f"media/{filename}"
            
        except Exception as e:
            logger.error(f"Ошибка при скачивании медиа: {e}")
            return None
    
    def format_message_data(self, message: Message, is_outgoing: bool, media_path: Optional[str] = None) -> Dict[str, Any]:
        """Форматирует данные сообщения для JSON"""
        data = {
            'id': message.id,
            'date': message.date.isoformat() if message.date else None,
            'text': message.text or '',
            'is_outgoing': is_outgoing,
            'reply_to_msg_id': message.reply_to_msg_id,
        }
        
        # Добавляем информацию о медиа
        if message.media:
            media_info = {
                'has_media': True,
                'media_type': type(message.media).__name__,
            }
            
            if media_path:
                media_info['file_path'] = media_path
                
            # Дополнительная информация о медиа
            if isinstance(message.media, MessageMediaPhoto):
                media_info['media_subtype'] = 'photo'
            elif isinstance(message.media, MessageMediaDocument):
                if message.media.document:
                    media_info['file_size'] = message.media.document.size
                    mime_type = message.media.document.mime_type
                    media_info['mime_type'] = mime_type
                    
                    # Определяем подтип по mime_type
                    if 'audio' in mime_type:
                        media_info['media_subtype'] = 'audio'
                    elif 'video' in mime_type:
                        media_info['media_subtype'] = 'video'
                    elif 'image' in mime_type:
                        media_info['media_subtype'] = 'image'
                    elif 'sticker' in mime_type or 'webp' in mime_type:
                        media_info['media_subtype'] = 'sticker'
                    else:
                        media_info['media_subtype'] = 'document'
                else:
                    media_info['media_subtype'] = 'document'
            elif isinstance(message.media, MessageMediaContact):
                media_info['media_subtype'] = 'contact'
                media_info['contact_info'] = {
                    'phone_number': message.media.phone_number,
                    'first_name': message.media.first_name,
                    'last_name': message.media.last_name,
                }
            elif isinstance(message.media, MessageMediaGeo):
                media_info['media_subtype'] = 'location'
                if hasattr(message.media, 'geo'):
                    media_info['location'] = {
                        'lat': message.media.geo.lat,
                        'long': message.media.geo.long,
                    }
            else:
                media_info['media_subtype'] = 'other'
                
            data['media'] = media_info
        else:
            data['media'] = {'has_media': False}
            
        return data
    
    async def export_chat_history(self, entity, chat_folder_name: str, hours_back: int = 48):
        """Экспортирует историю чата"""
        try:
            chat_folder = self.base_dir / chat_folder_name
            chat_folder.mkdir(exist_ok=True)
            
            # Определяем временной диапазон
            now = datetime.now()
            start_date = now - timedelta(hours=hours_back)
            
            logger.info(f"Экспортируем историю чата {chat_folder_name} за последние {hours_back} часов...")
            
            # Получаем информацию о себе для определения направления сообщений
            me = await self.client.get_me()
            
            messages_data = []
            message_count = 0
            
            # Получаем сообщения
            async for message in self.client.iter_messages(
                entity, 
                offset_date=start_date,
                reverse=True  # Сначала старые сообщения
            ):
                if message.date and message.date < start_date:
                    continue
                    
                # Определяем направление сообщения
                is_outgoing = message.from_id and message.from_id.user_id == me.id
                
                # Скачиваем медиафайлы если есть
                media_path = None
                if message.media:
                    media_path = await self.download_media(message, chat_folder)
                
                # Форматируем данные сообщения
                message_data = self.format_message_data(message, is_outgoing, media_path)
                
                # Классифицируем как input или output
                if is_outgoing:
                    direction = 'output'
                else:
                    direction = 'input'
                
                message_data['direction'] = direction
                messages_data.append(message_data)
                message_count += 1
                
                if message_count % 100 == 0:
                    logger.info(f"Обработано сообщений: {message_count}")
            
            # Сохраняем в JSON файл
            if messages_data:
                json_file = chat_folder / f'messages_{now.strftime("%Y%m%d_%H%M%S")}.json'
                
                export_data = {
                    'chat_info': {
                        'folder_name': chat_folder_name,
                        'export_date': now.isoformat(),
                        'time_range': {
                            'from': start_date.isoformat(),
                            'to': now.isoformat(),
                            'hours_back': hours_back
                        },
                        'total_messages': len(messages_data)
                    },
                    'messages': messages_data
                }
                
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Экспорт завершен: {message_count} сообщений сохранено в {json_file}")
            else:
                logger.info(f"Сообщений за указанный период не найдено для {chat_folder_name}")
                
        except Exception as e:
            logger.error(f"Ошибка при экспорте чата {chat_folder_name}: {e}")
    
    async def export_all_chats(self, hours_back: int = 48):
        """Экспортирует историю всех чатов"""
        logger.info(f"Начинаем экспорт истории за последние {hours_back} часов...")
        
        # Подключаемся к Telegram
        await self.client.start()
        logger.info("Подключение к Telegram установлено")
        
        # Получаем информацию о себе
        me = await self.client.get_me()
        logger.info(f"Вошли как: {me.first_name} {me.last_name or ''} (@{me.username or 'без username'})")
        
        # Получаем список всех диалогов
        dialogs = await self.client.get_dialogs()
        logger.info(f"Найдено диалогов: {len(dialogs)}")
        
        processed_count = 0
        
        for dialog in dialogs:
            try:
                entity = dialog.entity
                
                # Фильтруем по типам чатов
                skip_chat = False
                if isinstance(entity, User) and not self.config.EXPORT_PRIVATE_CHATS:
                    skip_chat = True
                elif isinstance(entity, Chat) and not self.config.EXPORT_GROUPS:
                    skip_chat = True
                elif isinstance(entity, Channel) and not self.config.EXPORT_CHANNELS:
                    skip_chat = True
                
                if skip_chat:
                    logger.debug(f"Пропускаем чат (тип отключен в настройках): {type(entity).__name__}")
                    continue
                
                chat_folder_name = self.get_chat_folder_name(entity)
                
                logger.info(f"Обрабатываем чат: {chat_folder_name} (тип: {type(entity).__name__})")
                
                await self.export_chat_history(entity, chat_folder_name, hours_back)
                processed_count += 1
                
                # Небольшая пауза между чатами
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Ошибка при обработке диалога: {e}")
                continue
        
        logger.info(f"Экспорт завершен! Обработано чатов: {processed_count}")
    
    async def stop(self):
        """Останавливает клиент"""
        await self.client.disconnect()

async def main():
    """Главная функция"""
    
    # Проверяем конфигурацию
    try:
        ExportConfig.validate()
        print("✅ Конфигурация экспорта в порядке")
    except ValueError as e:
        print(f"❌ {e}")
        return
    
    exporter = TelegramHistoryExporter()
    
    try:
        # Используем количество часов из конфигурации
        hours_back = exporter.config.EXPORT_HOURS_BACK
        
        print(f"🚀 Начинаем экспорт истории за последние {hours_back} часов")
        print(f"📁 Папка сохранения: {exporter.config.EXPORT_BASE_DIR}")
        print(f"📥 Скачивание медиа: {'включено' if exporter.config.DOWNLOAD_MEDIA else 'отключено'}")
        
        if exporter.config.DOWNLOAD_MEDIA:
            print(f"📊 Максимальный размер файла: {exporter.config.MAX_FILE_SIZE_MB} МБ")
        
        await exporter.export_all_chats(hours_back)
        
    except KeyboardInterrupt:
        logger.info("Экспорт прерван пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await exporter.stop()

if __name__ == "__main__":
    asyncio.run(main()) 