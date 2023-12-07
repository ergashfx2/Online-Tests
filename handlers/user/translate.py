from PIL import Image
from aiogram import types
from aiogram.types.base import InputFile
from googletrans import Translator
from pytesseract import pytesseract

from keyboards import keyboard
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from deep_translator import GoogleTranslator
from utils.db_api.translate_image import translate_image


@dp.message_handler(text="Ortga qaytish", state=["uzen", "enuz", "uzru", "ruuz"])
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Siz asosiy menyuga qaytdingiz", reply_markup=keyboard.mainM)
    await state.finish()


@dp.message_handler(text="/uzen")
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Rasm yoki matn yuboring..", reply_markup=keyboard.back)
    await state.set_state("uzen")


@dp.message_handler(text="/enuz")
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Rasm yoki matn yuboring..", reply_markup=keyboard.back)
    await state.set_state("enuz")


@dp.message_handler(text="/uzru")
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Rasm yoki matn yuboring..", reply_markup=keyboard.back)
    await state.set_state("uzru")


@dp.message_handler(text="/ruuz")
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Rasm yoki matn yuboring..", reply_markup=keyboard.back)
    await state.set_state("ruuz")


@dp.message_handler(state="uzen")
async def enuz(msg: types.Message):
    to_translate = msg.text
    translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
    await msg.answer(translated)


@dp.message_handler(state="enuz")
async def enuz(msg: types.Message):
    to_translate = msg.text
    translated = GoogleTranslator(source='auto', target='uz').translate(to_translate)
    await msg.answer(translated)


@dp.message_handler(state="enuz", content_types=types.ContentType.PHOTO)
async def enuz(msg: types.Message, state: FSMContext):
    await msg.answer("Kutib turing....")
    id = msg.photo[2]["file_id"]
    file = await bot.get_file(id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="/home/ergashfx2/DTMBOT/images/image.png")
    img = Image.open('/home/ergashfx2/DTMBOT/images/image.png')
    result = pytesseract.image_to_string(img)
    translated = GoogleTranslator(source='auto', target='uz').translate(result)
    await msg.answer(translated)


@dp.message_handler(state="uzen", content_types=types.ContentType.PHOTO)
async def enuz(msg: types.Message, state: FSMContext):
    await msg.answer("Kutib turing....")
    id = msg.photo[2]["file_id"]
    file = await bot.get_file(id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="/home/ergashfx2/DTMBOT/images/image.png")
    img = Image.open('/home/ergashfx2/DTMBOT/images/image.png')
    result = pytesseract.image_to_string(img)
    translated = GoogleTranslator(source='auto', target='en').translate(result)
    await msg.answer(translated)


@dp.message_handler(state="uzru", content_types=types.ContentType.PHOTO)
async def enuz(msg: types.Message, state: FSMContext):
    await msg.answer("Kutib turing....")
    id = msg.photo[2]["file_id"]
    file = await bot.get_file(id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="/home/ergashfx2/DTMBOT/images/image.png")
    img = Image.open('/home/ergashfx2/DTMBOT/images/image.png')
    result = pytesseract.image_to_string(img)
    translated = GoogleTranslator(source='auto', target='ru').translate(result)
    await msg.answer(translated)


@dp.message_handler(state="ruuz", content_types=types.ContentType.PHOTO)
async def enuz(msg: types.Message, state: FSMContext):
    await msg.answer("Kutib turing....")
    id = msg.photo[2]["file_id"]
    file = await bot.get_file(id)
    file_path = file.file_path
    await bot.download_file(file_path, destination="/home/ergashfx2/DTMBOT/images/image.png")
    img = Image.open('/home/ergashfx2/DTMBOT/images/image.png')
    result = pytesseract.image_to_string(img,lang='rus')
    translated = GoogleTranslator(source='auto', target='uz').translate(result)
    await msg.answer(translated)


@dp.message_handler(state="uzru")
async def enuz(msg: types.Message):
    to_translate = msg.text
    translated = GoogleTranslator(source='auto', target='ru').translate(to_translate)
    await msg.answer(translated)


@dp.message_handler(state="ruuz")
async def enuz(msg: types.Message):
    to_translate = msg.text
    translated = GoogleTranslator(source='auto', target='uz').translate(to_translate)
    await msg.answer(translated)
