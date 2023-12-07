from aiogram import types

from data.config import btns, texts
from handlers.user.admin import get_user_data
from keyboards import keyboard
from keyboards.default.keyboard import mainM
from keyboards.default.keyboard import back
from keyboards.default.blok import blok
from loader import dp
from testlar.variyantlar import variyantuz
from testlar import variyantlar, javoblar
from aiogram.dispatcher import FSMContext

from utils.db_api.sqlite import db
from utils.misc.checker import compare
from datetime import datetime
import re
from keyboards.default import english, modules
from deep_translator import GoogleTranslator

@dp.message_handler(text=btns["new_test"])
async def new_test_handler(msg: types.Message):
    await msg.answer(texts["select_test_language"], reply_markup=keyboard.test)


@dp.message_handler(text="📮 Tarjimon")
async def new_test_handler(msg: types.Message):
    await msg.answer("Salom qaysi tilga tarjima qilmoqchisiz marhamat tanlang :\n\n/uzen - O'zbek tilidan ingliz "
                     "tiliga\n/enuz - Ingliz tilidan o'zbek tiliga tarjima qilish\n/uzru - O'zbek tilidan rus tiliga "
                     "tarjima qilish\n/ruuz - Rus tilidan o'zbek tiliga tarjima qilish\n\nO'zingizga kerakli "
                     "komandani menga jo'nating")


@dp.message_handler(text=btns["in_uzbek"])
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Kerakli modulni tanlang", reply_markup=modules.modules)

@dp.message_handler(text=btns["in_russian"])
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Выберите нужный модуль", reply_markup=modules.modules2)

@dp.message_handler(text="1 - Modul")
async def in_uzbek_handler(msg: types.Message, state: FSMContext):
    await msg.answer(texts["select_subject"], reply_markup=keyboard.uzbek)
    await state.set_state("test")


@dp.message_handler(text="2 - Modul")
async def in_uzbek_handler(msg: types.Message, state: FSMContext):
    await msg.answer(texts["select_subject"], reply_markup=keyboard.uzbek)
    await state.set_state("test2")


@dp.message_handler(text="Modul - 1")
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer(texts["ru_select_subject"], reply_markup=keyboard.rus)
    await state.set_state("testru")

@dp.message_handler(text="Modul - 2")
async def in_russian_handler(msg: types.Message, state: FSMContext):
    await msg.answer(texts["ru_select_subject"], reply_markup=keyboard.rus)
    await state.set_state("testru2")


@dp.message_handler(text=btns["dtm_news"])
async def news_handler(msg: types.Message):
    await msg.answer(
        texts["dtm_news"],
        parse_mode="HTML", disable_web_page_preview=True)


@dp.message_handler(text=btns["result"])
async def result_handler(msg: types.Message, state: FSMContext):
    await msg.answer(texts["instruction"], reply_markup=back, parse_mode="HTML")
    await state.set_state("result")


@dp.message_handler(state="result")
async def check_handler(msg: types.Message, state: FSMContext):
    try:
        test_number = msg.text.split('/')[0]
        string = msg.text
        yuborildi = string.split("/")[1]
        arr = list(yuborildi)
        javob = javoblar.javoblar[0][test_number]
        arr2 = list(javob)
        res = await compare(arr, arr2)
        result = len(res)
        correct = len(yuborildi) - int(result)
        now = datetime.now()
        xatolar = str()
        current_time = now.strftime("%H:%M:%S")
        total = len(yuborildi)
        user = get_user_data(cid=msg.from_user.id)
        await msg.answer(
            f"👤 Foydalanuvchi ismi: {msg.from_user.full_name}\n📖 Test nomeri: {test_number}\n✏️ Jami savollar soni: {len(yuborildi)} "
            f"ta\n✅ To'g'ri javoblar soni: {correct} ta\n❌ Xato javoblar: {result} ta\n🕐{current_time}")
        for r in res:
            xatolar += f"{int(r) + 1})\n"

        await msg.answer(f"Quyidagi savollarda xato qilgansiz\n\n{xatolar}")

        def is_higher_or_equal(x, y):
            return x >= (0.5 * y)

        if is_higher_or_equal(correct, total):
            bal = user[5]+1
            db.update_user_bal(bal=bal,cid=msg.from_user.id)
            await msg.answer(f"🏆🥳*Sizga 1 bal berildi 🏆*\n\n🏅_Hozirgi balingiz :_ *{user[5]+1}*",parse_mode="markdown")

        else:
            await msg.answer("To'g'ri javoblaringiz 50% dan past ekanligi sabab sizga bal berilmadi")
        await state.finish()
    except:
        await msg.answer("Qandaydir xatolik yuz berdi /start buyrug'ini bosing va javoblar sonini tekshirib qayta "
                         "urinib ko'ring...")
        await state.finish()


@dp.message_handler(text=btns["video_instruction"])
async def teach(msg: types.Message):
    await msg.answer_video("https://t.me/testiszlar/29",
                           caption=texts["caption_instruction"],
                           parse_mode="HTML")


@dp.message_handler(text=btns["blokli"])
async def result_handler(msg: types.Message, state: FSMContext):
    await msg.answer("*Kerakli fanni tanlang:*", reply_markup=blok, parse_mode="markdown")
    await state.set_state("blokli")


@dp.message_handler(text="📹 Video darslar")
async def result_handler(msg: types.Message, state: FSMContext):
    await msg.answer("*Kerakli darsni tanlang:*", reply_markup=english.lesson, parse_mode="markdown")


@dp.message_handler(text="🇺🇸 Ingliz tili")
async def result_handler(msg: types.Message, state: FSMContext):
    sonlar = range(56, 135)
    for son in sonlar:
        await msg.answer_video(f"https://t.me/testiszlar/{son}", caption=f"🎥 *{son - 55} - Dars* ",
                               reply_markup=english.lesson, parse_mode="markdown")
    await msg.answer(
        "Dars mualliflari \n\n-Abdulazim Abdulqodir\n-Lison uzb\n\nHamda boshqalarga minnatdorchilik bildiramiz.Ilm ulashish uchun yaratgan darslaringizdan ilm ulashish maqsadida foydalanganimiz uchun rozi bo'lasiz deb umid qilamiz !")


@dp.message_handler(text="🇺🇿 Ona tili")
async def result_handler(msg: types.Message, state: FSMContext):
    sonlar = range(136, 174)
    for son in sonlar:
        await msg.answer_video(f"https://t.me/testiszlar/{son}", caption=f"🎥 *{son - 135} - Dars* ",
                               reply_markup=english.lesson, parse_mode="markdown")
    await msg.answer(
        "Dars muallifi \n\nNamoz Rasulovga hamda boshqalarga minnatdorchilik bildiramiz.Ilm ulashish uchun yaratgan darslaringizdan ilm ulashish maqsadida foydalanganimiz uchun rozi bo'lasiz deb umid qilamiz !")


@dp.message_handler(text="📑 Majburiy fanlardan testlar")
async def send_majburiy(msg: types.Message):
    await msg.answer_document("https://t.me/testiszlar/195", caption="Matematika")
    await msg.answer_document("https://t.me/testiszlar/196", caption="Ona tili")
    await msg.answer_document("https://t.me/testiszlar/197", caption="Tarix")
    await msg.answer("Ushbu variyantlar DTM ning pulli variyantlar bo'limiga kirganligi sababli javoblarini olish ilojisi bo'lmadi hozircha bizda javoblar mavjud emas.\n\nAgar ushbu variyantlarning aniq javoblarini ishlab bera olsangiz va holis yordam berishga tayyor bo'lsangiz bizga bog'laning va biz javob variyantlarini kiritib qo'yamiz")

@dp.message_handler(text="🇺🇿 Matematika")
async def result_handler(msg: types.Message, state: FSMContext):
        await msg.answer_video("https://t.me/testiszlar/218",caption="*Majburiy matematika to'liq yechimlar. DTM-2021. Barcha abituriyentlar uchun.*",parse_mode="markdown")
        await msg.answer(
        "Dars muallifi \n\n[Murodjon Xo'janiyozov](http://www.youtube.com/channel/UCULBpJbnX5e16m08lG5LNnQ)ga hamda boshqalarga minnatdorchilik bildiramiz.Ilm ulashish uchun yaratgan darslaringizdan ilm ulashish maqsadida foydalanganimiz uchun rozi bo'lasiz deb umid qilamiz !",parse_mode="markdown")
