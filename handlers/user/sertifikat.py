from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.user.admin import get_user_data
from keyboards.default.keyboard import mainM, back
from loader import dp
from utils.db_api.sqlite import db


@dp.message_handler(text="🥇 Sertifikat olish")
async def welcome(msg: types.Message, state: FSMContext):
    user = get_user_data(cid=msg.from_user.id)
    if user[5]>=3:
        await msg.answer(f"*Ismingizni kiriting :*", reply_markup=back,parse_mode="markdown")
        await state.set_state("sertifikat")
    else:
        await msg.answer(f"*❌ Sizda ball yetarli emas sertifikat olish uchun kamida 3 ball olishingiz kerak\n\nBuning uchun kamida 3 ta test variyantini 50% dan yuqori ishlang*", parse_mode="markdown")


@dp.message_handler(state="sertifikat")
async def welcome(msg: types.Message, state: FSMContext):
    await msg.answer_photo(f"https://botlarga.uz/online.php?text={msg.text}",caption=f"{msg.text} *ismiga sertifikat tayyor\n\nBotimizni do'stlaringizga tavsiya qilishni unutmang*", reply_markup=back,parse_mode="markdown")
    await state.finish()
