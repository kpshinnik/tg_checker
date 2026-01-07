import asyncio
import logging
import os
import re
from datetime import datetime, timedelta
from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.types import Message
import openai
from config import Config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramSpellChecker:
    def __init__(self):
        self.config = Config()
        self.client = TelegramClient(
            'session_name',
            self.config.API_ID,
            self.config.API_HASH
        )
        self.openai_client = openai.AsyncOpenAI(api_key=self.config.OPENAI_API_KEY)
        self.processed_messages = set()  # Храним ID обработанных сообщений
        
    def get_link_patterns(self):
        """Возвращает паттерны для поиска ссылок"""
        return [
            r'https?://[^\s]+',  # http/https ссылки
            r'www\.[^\s]+',      # www ссылки
            r'ftp://[^\s]+',     # ftp ссылки
            r't\.me/[^\s]+',     # Telegram ссылки
            r'@[a-zA-Z0-9_]+',   # Telegram username
            r'#[a-zA-Z0-9_]+',   # Хештеги
            r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',  # Домены
        ]

    def has_links(self, text: str) -> bool:
        """Проверяет, содержит ли текст ссылки"""
        url_patterns = self.get_link_patterns()
        
        for pattern in url_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def extract_links(self, text: str) -> list:
        """Извлекает все ссылки из текста"""
        links = []
        url_patterns = self.get_link_patterns()
        
        for pattern in url_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            links.extend(matches)
        
        return links

    async def check_spelling(self, text: str) -> Optional[str]:
        """Проверяет орфографию текста через GPT-4"""
        try:
            # Проверяем, есть ли в тексте ссылки
            has_links = self.has_links(text)
            
            if has_links:
                logger.info("В тексте обнаружены ссылки - используем специальный режим проверки")
                prompt = f"""
Проверь орфографию и пунктуацию в следующем тексте на русском языке. 
ВАЖНО: В тексте есть ссылки, URL-адреса или username - НЕ ИЗМЕНЯЙ их ни в коем случае!
Исправляй ТОЛЬКО орфографические и пунктуационные ошибки в обычном тексте.
Если есть ошибки, исправь их и верни ТОЛЬКО исправленный текст.
Если ошибок нет, верни ТОЧНО тот же текст без изменений.
Не добавляй никаких комментариев или объяснений.

Текст для проверки:
{text}
                """
            else:
                prompt = f"""
Проверь орфографию и пунктуацию в следующем тексте на русском языке. 
Если есть ошибки, исправь их и верни ТОЛЬКО исправленный текст.
Если ошибок нет, верни ТОЧНО тот же текст без изменений.
Не добавляй никаких комментариев или объяснений.

Текст для проверки:
{text}
                """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-5.2",
                messages=[
                    {"role": "system", "content": "Ты эксперт по русской орфографии и пунктуации."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            corrected_text = response.choices[0].message.content.strip()
            
            # Если в тексте были ссылки, дополнительно проверяем, что они не изменились
            if has_links:
                original_links = self.extract_links(text)
                corrected_links = self.extract_links(corrected_text)
                
                if original_links != corrected_links:
                    logger.warning("GPT изменил ссылки! Отменяем исправление.")
                    logger.warning(f"Исходные ссылки: {original_links}")
                    logger.warning(f"Измененные ссылки: {corrected_links}")
                    return None
            
            # Проверяем, отличается ли исправленный текст от оригинала
            if corrected_text != text:
                logger.info(f"Найдены ошибки в тексте. Оригинал: {text[:50]}...")
                logger.info(f"Исправлено: {corrected_text[:50]}...")
                return corrected_text
            else:
                logger.info("Ошибок не найдено")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при проверке орфографии: {e}")
            return None
    
    async def handle_new_message(self, event):
        """Обрабатывает новые сообщения от пользователя"""
        message: Message = event.message
        
        # Проверяем, что это сообщение от нас самих
        if not message.out:
            return
            
        # Проверяем, что это текстовое сообщение
        if not message.text:
            return
            
        # Избегаем повторной обработки
        if message.id in self.processed_messages:
            return
            
        self.processed_messages.add(message.id)
        
        logger.info(f"Обрабатываем сообщение: {message.text[:50]}...")
        
        # Небольшая задержка, чтобы убедиться, что сообщение отправлено
        await asyncio.sleep(1)
        
        try:
            # Проверяем орфографию
            corrected_text = await self.check_spelling(message.text)
            
            if corrected_text:
                # Редактируем сообщение
                await self.client.edit_message(
                    message.peer_id,
                    message.id,
                    corrected_text
                )
                logger.info("Сообщение успешно исправлено!")
            else:
                logger.info("Сообщение не требует исправлений")
                
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}")
    
    async def start(self):
        """Запускает сервис мониторинга"""
        logger.info("Запускаем сервис проверки орфографии...")
        
        # Подключаемся к Telegram
        await self.client.start()
        logger.info("Подключение к Telegram установлено")
        
        # Получаем информацию о себе
        me = await self.client.get_me()
        logger.info(f"Вошли как: {me.first_name} {me.last_name or ''} (@{me.username or 'без username'})")
        
        # Добавляем обработчик для исходящих сообщений
        self.client.add_event_handler(
            self.handle_new_message,
            events.NewMessage(outgoing=True)
        )
        
        logger.info("Сервис запущен! Мониторим исходящие сообщения...")
        
        # Запускаем клиент до остановки
        await self.client.run_until_disconnected()
    
    async def stop(self):
        """Останавливает сервис"""
        logger.info("Останавливаем сервис...")
        await self.client.disconnect()

async def main():
    """Главная функция"""
    checker = TelegramSpellChecker()
    
    try:
        await checker.start()
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await checker.stop()

if __name__ == "__main__":
    asyncio.run(main()) 