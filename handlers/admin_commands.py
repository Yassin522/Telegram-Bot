"""
Admin-only commands (restricted to authorized user 'yaseen52').
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from handlers.islamic_commands import get_scheduled_chats

logger = logging.getLogger(__name__)

ADMIN_USERNAME = "yaseen52"
_PENDING_KEY = "sendto_pending_message"


def _is_admin(update: Update) -> bool:
    return update.effective_user and update.effective_user.username == ADMIN_USERNAME


async def sendto_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/sendto <message> — pick a registered chat and send a custom message."""
    if not _is_admin(update):
        await update.message.reply_text("⛔ هذا الأمر للمشرف فقط.")
        return

    message_text = " ".join(context.args).strip() if context.args else ""
    if not message_text:
        await update.message.reply_text(
            "الاستخدام: /sendto <الرسالة>\n"
            "مثال: /sendto مرحبا يا شباب!"
        )
        return

    chat_ids = get_scheduled_chats()
    if not chat_ids:
        await update.message.reply_text("لا يوجد أي chat مسجّل حتى الآن.")
        return

    # Fetch title for each registered chat
    buttons = []
    for chat_id in chat_ids:
        try:
            chat = await context.bot.get_chat(chat_id)
            title = chat.title or chat.first_name or str(chat_id)
        except Exception:
            title = str(chat_id)
        buttons.append(
            InlineKeyboardButton(text=title, callback_data=f"sendto_{chat_id}")
        )

    # Add "send to all" button
    buttons.append(InlineKeyboardButton(text="📢 الكل", callback_data="sendto_all"))

    # Store the pending message so the callback can retrieve it
    context.user_data[_PENDING_KEY] = message_text

    keyboard = InlineKeyboardMarkup([[btn] for btn in buttons])
    await update.message.reply_text(
        f"📨 وين ترسل هالرسالة؟\n\n«{message_text}»",
        reply_markup=keyboard,
    )


async def sendto_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline keyboard button press for /sendto."""
    query = update.callback_query
    await query.answer()

    if not _is_admin(update):
        await query.edit_message_text("⛔ هذا الأمر للمشرف فقط.")
        return

    message_text = context.user_data.pop(_PENDING_KEY, None)
    if not message_text:
        await query.edit_message_text("⚠️ انتهت صلاحية الرسالة، جرّب /sendto مرة تانية.")
        return

    data = query.data  # "sendto_<chat_id>" or "sendto_all"
    target = data[len("sendto_"):]  # "<chat_id>" or "all"

    if target == "all":
        chat_ids = get_scheduled_chats()
        sent, failed = 0, 0
        for chat_id in chat_ids:
            try:
                await context.bot.send_message(chat_id=chat_id, text=message_text)
                sent += 1
            except Exception as e:
                logger.error(f"sendto_all failed for {chat_id}: {e}")
                failed += 1
        status = f"✅ اترسلت على {sent} chat"
        if failed:
            status += f" (فشلت {failed})"
        await query.edit_message_text(status)
    else:
        try:
            chat_id = int(target)
            await context.bot.send_message(chat_id=chat_id, text=message_text)
            chat = await context.bot.get_chat(chat_id)
            title = chat.title or chat.first_name or str(chat_id)
            await query.edit_message_text(f"✅ اترسلت على «{title}»")
        except Exception as e:
            logger.error(f"sendto failed for {target}: {e}")
            await query.edit_message_text(f"❌ ما قدرت أرسل: {e}")
