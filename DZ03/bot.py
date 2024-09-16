import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers import student_handlers
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
# Регистрируем обработчики
student_handlers.register_handlers(dp)
# Функция для корректного завершения работы бота
async def on_shutdown():
    await bot.session.close()
    logger.info("Бот остановлен")
async def main():
    # Логируем запуск бота
    logger.info("Бот запущен и готов к работе")
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()  # Корректное завершение работы при остановке
if __name__ == "__main__":
    asyncio.run(main())