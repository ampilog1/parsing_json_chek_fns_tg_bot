from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def handle_manual_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Устанавливаем первый шаг и запрашиваем дату
    context.user_data['receipt_step'] = 'date'
    await update.message.reply_text("Введите дату чека (например, 2024-10-31):")


async def handle_receipt_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    step = context.user_data.get('receipt_step')

    if step == 'date':
        # Сохраняем дату и переходим к продуктам
        context.user_data['receipt_date'] = update.message.text
        context.user_data['receipt_step'] = 'products'
        await update.message.reply_text("Введите список продуктов (через запятую):")

    elif step == 'products':
        # Сохраняем продукты
        products = update.message.text.split(',')
        context.user_data['current_receipt'] = {
            'products': [{'name': product.strip()} for product in products],
            'receipt_date': context.user_data['receipt_date'],
            'current_page': 1,
            'editing_mode': False,
            'selected_product': None
        }
        await update.message.reply_text("Чек успешно добавлен!")
        context.user_data.clear()  # Очищаем данные пользователя после сохранения


def setup_manual_receipt_handlers(application):
    application.add_handler(MessageHandler(filters.Regex('/manual_receipt'), handle_manual_receipt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_receipt_input))
