from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

# Kanalga obuna bo‘lishni tekshirish
def check_subscription(update: Update, context: CallbackContext) -> bool:
    user_id = update.message.from_user.id
    chat_id = "@yanvaristik"  # Kanal nomi

    try:
        member = context.bot.get_chat_member(chat_id, user_id)
        # Agar foydalanuvchi kanalga obuna bo‘lsa, True qaytariladi
        if member.status in ['member', 'administrator']:
            return True
        else:
            return False
    except Exception as e:
        return False

# Botni boshlash komandasi
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Salom! Test javoblarini tekshiruvchi botga xush kelibsiz.\n"
        "Iltimos, ismingiz va familyangizni kiriting."
    )

# Foydalanuvchi ismini va familyasini olish
def get_name(update: Update, context: CallbackContext) -> None:
    user_name = update.message.text.strip()
    context.user_data['name'] = user_name  # Foydalanuvchi ismi va familyasini saqlash
    update.message.reply_text(
        f"Rahmat, {user_name}! Endi, kanalga obuna bo‘lishingiz kerak.\n"
        "Iltimos, @yanvaristik kanaliga obuna bo‘ling."
    )

# Foydalanuvchi obuna bo‘lsa, test javoblarini qabul qilish
def handle_subscription(update: Update, context: CallbackContext) -> None:
    if check_subscription(update, context):
        update.message.reply_text("Kanalga obuna bo'ldingiz! Endi test javoblaringizni yuboring.")
        return

    update.message.reply_text(
        "Siz kanalga obuna bo‘lmagan ekansiz. Iltimos, @yanvaristik kanaliga obuna bo‘ling va qaytib keling."
    )

# Test javoblarini saqlash
tests_answers = {}

def add_test_answers(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.strip()
    try:
        test_id, answers = user_input.split()
        tests_answers[test_id] = answers
        update.message.reply_text(f"Test ID {test_id} uchun javoblar muvaffaqiyatli saqlandi!")
    except ValueError:
        update.message.reply_text("Iltimos, to'g'ri formatda yuboring: Test ID va javoblar (masalan: 1 a2b3c4d)")

# Test javoblarini tekshirish
def check_answers(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.strip()

    try:
        test_id, answers = user_input.split()
        if test_id in tests_answers:
            correct_answers = tests_answers[test_id]
            score = sum(1 for i, ans in enumerate(answers) if ans == correct_answers[i])
            update.message.reply_text(
                f"Sizning natijangiz: {score}/{len(correct_answers)}\n"
                f"Sizning javoblaringiz: {answers}\n"
                f"To'g'ri javoblar: {correct_answers}"
            )
        else:
            update.message.reply_text(f"Test ID {test_id} topilmadi. Iltimos, to'g'ri Test ID yuboring.")
    except ValueError:
        update.message.reply_text("Iltimos, to'g'ri formatda Test ID va javoblarni yuboring.")

def main() -> None:
    # Bot tokeningizni kiriting
    updater = Updater("5205989916:AAHqjHNVC2nNjmF0cX9AO7FoZaIVVVYzlDk", use_context=True)

    # Komandalar va xabarlarni qo‘shish
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_name))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_subscription))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, add_test_answers))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_answers))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
