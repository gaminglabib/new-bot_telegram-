import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('API_TOKEN')  # Render environment থেকে নেবে
ADMIN_ID = 7377185899
CHANNEL_USERNAME = 'always_viral'  # @ ছাড়া ইউজারনেম

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_data = {
    'links': [],
    'videos': []
}

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="/admin"),
        KeyboardButton(text="/videos")
    )
    builder.row(
        KeyboardButton(text="/shere"),
        KeyboardButton(text="/viral_links")
    )
    builder.row(
        KeyboardButton(text="/acount"),
        KeyboardButton(text="/help")
    )
    return builder.as_markup(resize_keyboard=True)

async def is_user_joined_channel(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status not in ('left', 'kicked')
    except Exception:
        return False

@dp.message(Command(commands=['start']))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    joined = await is_user_joined_channel(user_id)

    if not joined:
        join_btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]
        ])
        await message.answer(
            f"""প্রিয় user: {full_name}

in bangla : আসসালামু আলাইকুম ❤️‍🩹
in english : Peace be upon you. ❤️‍🩹
in arabic : السلام عليكم. ❤️‍🩹

আমাদের বটটি use করার জন্য আপনাকে ধন্যবাদ ❤️❤️
ভিডিও পেতে হলে, প্রথমে নিচের চ্যানেলটি জয়েন করতে হবে 🥰""",
            reply_markup=join_btn
        )
        await message.answer("✅ Join করে আবার /start দিন")
    else:
        await message.answer(f"আপনি চ্যানেলটি জয়েন করেছেন, স্বাগতম {full_name}!", reply_markup=main_menu())

# Admin password protection for /admin command
ADMIN_PASSWORD = "TASLIMAlupa"
admin_authenticated_users = set()

@dp.message(lambda m: m.text == "/admin")
async def admin_auth_request(message: types.Message):
    if message.from_user.id not in admin_authenticated_users:
        await message.answer("অ্যাডমিন প্যানেলে প্রবেশের জন্য পাসওয়ার্ড লিখুন:")
    else:
        await show_admin_panel(message)

@dp.message()
async def check_admin_password(message: types.Message):
    if message.from_user.id in admin_authenticated_users:
        return  # Already authenticated
    if message.text == ADMIN_PASSWORD and message.from_user.id == ADMIN_ID:
        admin_authenticated_users.add(message.from_user.id)
        await message.answer("অ্যাডমিন প্যানেলে স্বাগতম! কমান্ড ব্যবহার করুন।\n/admin দিয়ে আবার প্যানেল খুলুন।")
    elif message.from_user.id == ADMIN_ID:
        await message.answer("পাসওয়ার্ড ভুল হয়েছে। আবার চেষ্টা করুন।")

async def show_admin_panel(message: types.Message):
    buttons = [
        [KeyboardButton("/userlist"), KeyboardButton("/add_link")],
        [KeyboardButton("/add_video"), KeyboardButton("/back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("Admin Panel", reply_markup=markup)

@dp.message(lambda m: m.text == "/videos")
async def video_panel(message: types.Message):
    buttons = [
        [KeyboardButton("/দেশি_ভিডিও"), KeyboardButton("/জাপানিজ")],
        [KeyboardButton("/আমেরিকান"), KeyboardButton("/লেসবিয়ান")],
        [KeyboardButton("/নতুন"), KeyboardButton("/back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("ভিডিও ক্যাটেগরি সিলেক্ট করুন: 🎥", reply_markup=markup)

@dp.message(lambda m: m.text == "/shere")
async def share_bot(message: types.Message):
    user_id = message.from_user.id
    refer_link = f"https://t.me/always_viral_bot?start={user_id}"

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("/নতুন_ভাইরাল_লিংক"),
        KeyboardButton("/টিকটকার_এর_লিংক"),
        KeyboardButton("/ট্রেন্ডিং_লিংক"),
        KeyboardButton("/back")
    )

    await message.answer(
        f"""এই নিন আপনার রেফার লিংক 👇
{refer_link}
এবং বন্ধুদের সাথে শেয়ার করুন ❤️🥰

/back দিয়ে মেইন মেনুতে ফিরে যান।""",
        reply_markup=keyboard
    )

@dp.message(lambda m: m.text == "/viral_links")
async def viral_links_cmd(message: types.Message):
    buttons = [
        [KeyboardButton("/ট্রেন্ডিং_লিংক"), KeyboardButton("/টিকটকার_এর_লিংক")],
        [KeyboardButton("/নতুন_ভাইরাল_লিংক"), KeyboardButton("/back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer("ভাইরাল লিংক ক্যাটেগরি দেখুন:", reply_markup=markup)

@dp.message(lambda m: m.text == "/acount")
async def account_info(message: types.Message):
    username = message.from_user.username or "নাই"
    await message.answer(f"""আপনার একাউন্ট তথ্য:
ইউজারনেম: @{username}
আইডি: {message.from_user.id}
নাম: {message.from_user.full_name}
""")

@dp.message(lambda m: m.text == "/help")
async def help_cmd(message: types.Message):
    await message.answer("সাহায্যের জন্য যোগাযোগ করুন: @toxic_digonto")

@dp.message(lambda m: m.text == "/back")
async def back_to_main(message: types.Message):
    await message.answer("আপনি এখন মেইন মেনুতে আছেন:", reply_markup=main_menu())

@dp.message(lambda m: m.text == "/userlist")
async def user_list(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ আপনি অ্যাডমিন না!")
        return
    await message.answer("ইউজার তালিকা CSV এ সংরক্ষিত থাকবে (ডেমো)")

@dp.message(lambda m: m.text == "/add_link")
async def add_link(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("❌ আপনি অ্যাডমিন না!")
        return
    await message.answer("নতুন লিংক প্রদান করুন:")

@dp.message(lambda m: m.text == "/add_video")
async def add_video(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("❌ আপনি অ্যাডমিন না!")
        return
    await message.answer("নতুন ভিডিও ইউআরএল প্রদান করুন:")

@dp.message(lambda message: message.text and message.text.startswith("http"))
async def handle_new_link_or_video(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    text = message.text.strip()
    if any(ext in text.lower() for ext in ['.mp4', '.mkv', '.mov', '.avi']):
        user_data['videos'].append(text)
        await message.answer(f"নতুন ভিডিও {text} সফলভাবে যুক্ত করা হয়েছে।")
    else:
        user_data['links'].append(text)
        await message.answer(f"নতুন লিংক {text} সফলভাবে যুক্ত করা হয়েছে।")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
