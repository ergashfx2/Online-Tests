from aiogram import executor
from loader import dp
import middlewares, filters, handlers
import logging

from utils.db_api.sqlite import db

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    executor.start_polling(dp)
