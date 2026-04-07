"""
Islamic command handlers.
"""
import json
import logging
import os
import random

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

from config import ALADHAN_API_BASE, ALQURAN_API_BASE, HADITH_API_BASE
from data.islamic_data import (
    ASMA_ALLAH, DHIKR_PHRASES,
    AQEEDAH_POINTS, SALAF_QUOTES, TAWHEED_CATEGORIES, SUNNAH_PRACTICES
)

logger = logging.getLogger(__name__)

SCHEDULE_CHATS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'schedule_chats.json')
KNOWN_GROUPS_FILE   = os.path.join(os.path.dirname(__file__), '..', 'data', 'known_groups.json')


# ---------------------------------------------------------------------------
# Schedule chat management helpers
# ---------------------------------------------------------------------------

def _load_chats() -> list:
    try:
        with open(SCHEDULE_CHATS_FILE, 'r') as f:
            return json.load(f).get('chats', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_chats(chats: list) -> None:
    with open(SCHEDULE_CHATS_FILE, 'w') as f:
        json.dump({'chats': chats}, f)


def get_scheduled_chats() -> list:
    return _load_chats()


def add_scheduled_chat(chat_id: int) -> bool:
    """Returns True if added, False if already registered."""
    chats = _load_chats()
    if chat_id in chats:
        return False
    chats.append(chat_id)
    _save_chats(chats)
    return True


def remove_scheduled_chat(chat_id: int) -> bool:
    """Returns True if removed, False if was not registered."""
    chats = _load_chats()
    if chat_id not in chats:
        return False
    chats.remove(chat_id)
    _save_chats(chats)
    return True


# ---------------------------------------------------------------------------
# /testschedule — send all scheduled posts immediately to this chat (yaseen52 only)
# ---------------------------------------------------------------------------

async def test_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send all 7 scheduled posts immediately to this chat for testing (yaseen52 only)."""
    if update.effective_user.username != 'yaseen52':
        await update.message.reply_text("❌ هذا الأمر متاح فقط للمسؤول.")
        return

    chat_id = update.effective_chat.id
    await update.message.reply_text("🔄 جاري إرسال جميع المنشورات اليومية للاختبار...")

    from data.islamic_data import FAJR_REMINDERS, DHIKR_PHRASES, EVENING_REMINDERS, ISLAMIC_QUOTES
    import aiohttp as _aiohttp
    from config import ALQURAN_API_BASE as _QURAN_BASE

    # 1. Fajr reminder
    try:
        text = f"{random.choice(FAJR_REMINDERS)}\n\n🤲 ذكر الصباح:\n{random.choice(DHIKR_PHRASES)}"
        await context.bot.send_message(chat_id=chat_id, text=f"[06:00]\n{text}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[06:00] ❌ {e}")

    # 2. Hijri date
    try:
        hijri_text = await _fetch_hijri()
        await context.bot.send_message(chat_id=chat_id, text=f"[07:00]\n{hijri_text or '❌ تعذّر الجلب'}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[07:00] ❌ {e}")

    # 3. Asmaullah
    try:
        name_ar, meaning_ar = random.choice(ASMA_ALLAH)
        text = f"✨ من أسماء الله الحسنى\n\n{name_ar}\n\nالمعنى: {meaning_ar}"
        await context.bot.send_message(chat_id=chat_id, text=f"[09:00]\n{text}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[09:00] ❌ {e}")

    # 4. Quran verse
    try:
        async with _aiohttp.ClientSession() as session:
            async with session.get(f"{_QURAN_BASE}/ayah/random/quran-uthmani",
                                   timeout=_aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ayah = data['data']
                    text = (f"📖 آية اليوم\n\n﴿{ayah['text']}﴾\n\n"
                            f"— {ayah['surah']['name']}، الآية {ayah['numberInSurah']}")
                    await context.bot.send_message(chat_id=chat_id, text=f"[12:00]\n{text}")
                else:
                    await context.bot.send_message(chat_id=chat_id, text="[12:00] ❌ API error")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[12:00] ❌ {e}")

    # 5. Dhikr
    try:
        text = f"🤲 ذكر العصر\n\n{random.choice(DHIKR_PHRASES)}"
        await context.bot.send_message(chat_id=chat_id, text=f"[15:00]\n{text}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[15:00] ❌ {e}")

    # 6. Hadith
    try:
        hadith_text = await _fetch_random_hadith()
        await context.bot.send_message(chat_id=chat_id, text=f"[18:00]\n{hadith_text or '❌ تعذّر الجلب'}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[18:00] ❌ {e}")

    # 7. Evening reminder
    try:
        text = f"{random.choice(EVENING_REMINDERS)}\n\n{random.choice(ISLAMIC_QUOTES)}"
        await context.bot.send_message(chat_id=chat_id, text=f"[21:00]\n{text}")
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"[21:00] ❌ {e}")

    await update.message.reply_text("✅ اكتمل الاختبار.")


# ---------------------------------------------------------------------------
# /setschedule and /unsetschedule
# ---------------------------------------------------------------------------

async def set_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register the current chat for daily Islamic auto-posts."""
    chat_id = update.effective_chat.id
    if add_scheduled_chat(chat_id):
        await update.message.reply_text(
            "✅ تم تفعيل المنشورات اليومية الإسلامية في هذه المجموعة!\n\n"
            "سيتم إرسال:\n"
            "🌅 06:00 — تذكير الفجر وذكر\n"
            "📖 12:00 — آية قرآنية\n"
            "📚 18:00 — حديث شريف\n"
            "🌙 21:00 — تذكير مسائي\n\n"
            "لإيقاف المنشورات: /unsetschedule"
        )
    else:
        await update.message.reply_text(
            "ℹ️ هذه المجموعة مسجّلة بالفعل للمنشورات اليومية.\n"
            "لإيقاف المنشورات: /unsetschedule"
        )


async def unset_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unregister the current chat from daily Islamic auto-posts (yaseen52 only)."""
    if update.effective_user.username != 'yaseen52':
        await update.message.reply_text("❌ هذا الأمر متاح فقط للمسؤول.")
        return
    chat_id = update.effective_chat.id
    if remove_scheduled_chat(chat_id):
        await update.message.reply_text("❌ تم إيقاف المنشورات اليومية الإسلامية في هذه المجموعة.")
    else:
        await update.message.reply_text(
            "ℹ️ هذه المجموعة غير مسجّلة للمنشورات اليومية."
        )


# ---------------------------------------------------------------------------
# /prayer <city>
# ---------------------------------------------------------------------------

async def prayer_times(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get prayer times for a city using the Aladhan API."""
    if not context.args:
        await update.message.reply_text(
            "📍 الاستخدام: /prayer <المدينة>\n"
            "مثال: /prayer بيروت\n"
            "أو بالإنجليزية: /prayer Beirut"
        )
        return

    city = ' '.join(context.args)
    url = f"{ALADHAN_API_BASE}/timingsByCity?city={city}&country=&method=2"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('code') == 200:
                        t = data['data']['timings']
                        hijri = data['data']['date']['hijri']
                        hijri_str = f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ"
                        msg = (
                            f"🕌 مواقيت الصلاة في {city}\n"
                            f"📅 {hijri_str}\n\n"
                            f"🌅 الفجر:    {t['Fajr']}\n"
                            f"🌄 الشروق:   {t['Sunrise']}\n"
                            f"☀️ الظهر:    {t['Dhuhr']}\n"
                            f"🌤 العصر:    {t['Asr']}\n"
                            f"🌇 المغرب:   {t['Maghrib']}\n"
                            f"🌙 العشاء:   {t['Isha']}\n"
                        )
                        await update.message.reply_text(msg)
                    else:
                        await update.message.reply_text(
                            "❌ لم يتم العثور على المدينة.\n"
                            "جرّب كتابة الاسم بالإنجليزية، مثال: /prayer Beirut"
                        )
                else:
                    await update.message.reply_text("❌ تعذّر الاتصال بخدمة المواقيت. حاول لاحقاً.")
    except Exception as e:
        logger.error(f"prayer_times error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء جلب المواقيت.")


# ---------------------------------------------------------------------------
# /quran
# ---------------------------------------------------------------------------

async def quran_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random Quran verse in Arabic."""
    url = f"{ALQURAN_API_BASE}/ayah/random/quran-uthmani"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ayah = data['data']
                    surah_ar = ayah['surah']['name']
                    ayah_num = ayah['numberInSurah']
                    text = ayah['text']
                    msg = (
                        f"📖 آية قرآنية\n\n"
                        f"﴿{text}﴾\n\n"
                        f"— {surah_ar}، الآية {ayah_num}"
                    )
                    await update.message.reply_text(msg)
                else:
                    await update.message.reply_text("❌ تعذّر جلب الآية. حاول لاحقاً.")
    except Exception as e:
        logger.error(f"quran_verse error: {e}")
        await update.message.reply_text("❌ حدث خطأ أثناء جلب الآية.")


# ---------------------------------------------------------------------------
# /hadith
# ---------------------------------------------------------------------------

async def hadith(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random hadith from one of the major collections."""
    result = await _fetch_random_hadith()
    if result:
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("❌ تعذّر جلب الحديث. حاول لاحقاً.")


# Major hadith collections on api.hadith.gading.dev with safe max ranges
_HADITH_BOOKS = [
    ("bukhari",   "صحيح البخاري",  300),
    ("muslim",    "صحيح مسلم",     300),
    ("abu-dawud", "سنن أبي داود",  300),
    ("tirmidhi",  "جامع الترمذي",  300),
    ("nasai",     "سنن النسائي",   300),
    ("ibn-majah", "سنن ابن ماجه",  300),
]


async def _fetch_random_hadith() -> str | None:
    """Fetch a random hadith from api.hadith.gading.dev. Returns formatted string or None."""
    book_id, book_name, max_num = random.choice(_HADITH_BOOKS)
    num = random.randint(1, max_num)
    url = f"{HADITH_API_BASE}/books/{book_id}?range={num}-{num}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    hadiths = data.get('data', {}).get('hadiths', [])
                    if hadiths:
                        h = hadiths[0]
                        return (
                            f"📚 حديث شريف\n"
                            f"{book_name} — رقم {h.get('number', num)}\n\n"
                            f"{h['arab']}"
                        )
    except Exception as e:
        logger.error(f"_fetch_random_hadith error: {e}")
    return None


# ---------------------------------------------------------------------------
# /hijri
# ---------------------------------------------------------------------------

async def _fetch_hijri() -> str | None:
    """Fetch today's Hijri date. Returns formatted string or None."""
    url = f"{ALADHAN_API_BASE}/timingsByCity?city=Mecca&country=SA&method=2"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    hijri = data['data']['date']['hijri']
                    return (
                        f"📅 التاريخ الهجري اليوم\n\n"
                        f"يوم {hijri['weekday']['ar']}\n"
                        f"{hijri['day']} {hijri['month']['ar']} {hijri['year']} هـ"
                    )
    except Exception as e:
        logger.error(f"_fetch_hijri error: {e}")
    return None


async def hijri_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the current Hijri date."""
    msg = await _fetch_hijri()
    if msg:
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("❌ تعذّر جلب التاريخ الهجري.")


# ---------------------------------------------------------------------------
# /asmaullah
# ---------------------------------------------------------------------------

async def asmaullah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random name from the 99 Names of Allah."""
    name_ar, meaning_ar = random.choice(ASMA_ALLAH)
    msg = (
        f"✨ من أسماء الله الحسنى\n\n"
        f"*{name_ar}*\n\n"
        f"المعنى: {meaning_ar}"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')


# ---------------------------------------------------------------------------
# /dhikr
# ---------------------------------------------------------------------------

async def dhikr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dhikr phrase."""
    phrase = random.choice(DHIKR_PHRASES)
    msg = f"🤲 ذكر\n\n{phrase}"
    await update.message.reply_text(msg)


# ---------------------------------------------------------------------------
# /aqeedah — Aqeedah of the Salaf
# ---------------------------------------------------------------------------

async def aqeedah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random Aqeedah point from Ahlus Sunnah wal Jama'ah."""
    topic, text, source = random.choice(AQEEDAH_POINTS)
    msg = (
        f"📗 من عقيدة السلف\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"*{topic}*\n\n"
        f"{text}\n\n"
        f"📌 المصدر: _{source}_"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')


# ---------------------------------------------------------------------------
# /salaf — Quotes from Salaf scholars
# ---------------------------------------------------------------------------

async def salaf_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random quote from a Salaf scholar."""
    scholar, quote = random.choice(SALAF_QUOTES)
    msg = (
        f"📜 من كلام السلف\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"{quote}\n\n"
        f"— _{scholar}_"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')


# ---------------------------------------------------------------------------
# /tawheed — The three categories of Tawheed
# ---------------------------------------------------------------------------

async def tawheed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random category of Tawheed with explanation."""
    category, explanation, daleel = random.choice(TAWHEED_CATEGORIES)
    msg = (
        f"☝️ التوحيد\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"*{category}*\n\n"
        f"{explanation}\n\n"
        f"📖 الدليل:\n{daleel}"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')


# ---------------------------------------------------------------------------
# /sunnah — Sunnah practices to revive
# ---------------------------------------------------------------------------

async def sunnah_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random Sunnah practice with its evidence."""
    practice, evidence = random.choice(SUNNAH_PRACTICES)
    msg = (
        f"🌿 من السنن المهجورة\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"*{practice}*\n\n"
        f"الدليل: {evidence}"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')


def _load_known_groups() -> list:
    try:
        with open(KNOWN_GROUPS_FILE, 'r') as f:
            return json.load(f).get('groups', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_known_groups(groups: list) -> None:
    with open(KNOWN_GROUPS_FILE, 'w') as f:
        json.dump({'groups': groups}, f)


def register_known_group(chat_id: int) -> None:
    """Track any group/supergroup the bot is active in."""
    groups = _load_known_groups()
    if chat_id not in groups:
        groups.append(chat_id)
        _save_known_groups(groups)


def get_known_groups() -> list:
    return _load_known_groups()


async def auto_register_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Silently register any chat that the bot receives a message in."""
    chat = update.effective_chat
    if chat is None:
        return
    add_scheduled_chat(chat.id)
    if chat.type in ("group", "supergroup"):
        register_known_group(chat.id)


async def handle_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto-register when the bot is added to a new group."""
    my_id = context.bot.id
    new_member = update.my_chat_member.new_chat_member
    if new_member.user.id == my_id and new_member.status in ("member", "administrator"):
        chat_id = update.effective_chat.id
        add_scheduled_chat(chat_id)
        register_known_group(chat_id)
        logger.info(f"Auto-registered new chat: {chat_id}")
