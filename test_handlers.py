import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update
from telegram.ext import ContextTypes
from handle_manual_receipt import handle_manual_receipt, handle_receipt_input

@pytest.mark.asyncio
async def test_handle_manual_receipt():
    update = MagicMock(Update)
    update.message = AsyncMock()
    context = MagicMock(ContextTypes.DEFAULT_TYPE)
    context.user_data = {}  # Устанавливаем user_data как пустой словарь

    await handle_manual_receipt(update, context)

    # Проверяем, что установлен первый шаг и отправлено сообщение
    assert context.user_data['receipt_step'] == 'date'
    update.message.reply_text.assert_called_once_with("Введите дату чека (например, 2024-10-31):")

@pytest.mark.asyncio
async def test_handle_receipt_input_date_step():
    update = MagicMock(Update)
    update.message = AsyncMock()
    update.message.text = "2024-10-31"
    context = MagicMock(ContextTypes.DEFAULT_TYPE)
    context.user_data = {'receipt_step': 'date'}

    await handle_receipt_input(update, context)

    # Проверяем, что дата сохранена и шаг изменен на 'products'
    assert context.user_data['receipt_date'] == "2024-10-31"
    assert context.user_data['receipt_step'] == 'products'
    update.message.reply_text.assert_called_once_with("Введите список продуктов (через запятую):")


