import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8453508873:AAFZsbL8xIgRYVLbhvJWN-GWxWNy3qni4DE"
CHANNEL = "@linkdaaaaa"  # Public kanal username yoki private bo'lsa chat_id

bot = telebot.TeleBot(TOKEN)

# Kanalga azo tekshirish
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status != "left"
    except:
        return False

# Inline tugmalar yaratish
def subscription_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Maxfiy kanal 🔒", url=f"https://t.me/{CHANNEL[1:]}"))
    markup.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))
    return markup

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    if is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "Salom! Kino kodini yuboring 🎬")
    else:
        bot.send_message(
            message.chat.id,
            "Avval maxfiy kanalga a'zo bo‘ling:",
            reply_markup=subscription_keyboard()
        )

# Callback tugma ishlashi
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    if is_subscribed(call.from_user.id):
        # Kanalga a’zo bo‘lsa
        bot.answer_callback_query(call.id, "Siz kanalga a’zo bo‘ldingiz ✅")
        bot.send_message(call.message.chat.id, "Endi kino kodini yuboring 🎬")
        # Tugmani olib tashlash
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    else:
        # A’zo bo‘lmasa
        bot.answer_callback_query(call.id, "❌ Avval maxfiy kanalga a'zo bo‘ling")

# Kino kodlari va post ID’lari
kino_dict = {
    "458": 1,
    "777": 2,
    "100": 3,
    "101": 4,
}

# Kino kodi tekshirish
@bot.message_handler(func=lambda m: True)
def kino(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "Avval maxfiy kanalga a'zo bo‘ling:",
            reply_markup=subscription_keyboard()
        )
        return

    code = message.text.strip()
    if code in kino_dict:
        try:
            bot.copy_message(
                chat_id=message.chat.id,
                from_chat_id=CHANNEL,
                message_id=kino_dict[code]
            )
        except:
            bot.send_message(message.chat.id, "❌ Kino topilmadi yoki bot postni ololmadi")
    else:
        bot.send_message(message.chat.id, "❌ Bunday kino topilmadi")

# Bot ishga tushishi
bot.polling()


