"""
Scheduled daily Islamic auto-post jobs.

Daily schedule (Beirut timezone):
  06:00 — Fajr reminder + morning dhikr
  07:00 — Hijri date
  09:00 — Name from 99 Names of Allah (Asmaullah)
  12:00 — Quran verse of the day
  15:00 — Dhikr (afternoon)
  18:00 — Hadith of the day
  21:00 — Evening reminder + Islamic quote
"""
import logging
import random
from datetime import time

import aiohttp
import pytz
from telegram.ext import Application

from config import ALQURAN_API_BASE
from data.islamic_data import (
    ASMA_ALLAH, DHIKR_PHRASES, ISLAMIC_QUOTES, FAJR_REMINDERS, EVENING_REMINDERS
)
from handlers.islamic_commands import get_scheduled_chats, _fetch_random_hadith, _fetch_hijri

logger = logging.getLogger(__name__)
BEIRUT_TZ = pytz.timezone('Asia/Beirut')


async def _broadcast(context, text: str) -> None:
    """Send a message to all registered chats."""
    for chat_id in get_scheduled_chats():
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception as e:
            logger.error(f"Failed to send scheduled message to {chat_id}: {e}")


async def job_fajr_reminder(context) -> None:
    """06:00 — Morning Fajr reminder + dhikr."""
    reminder = random.choice(FAJR_REMINDERS)
    phrase = random.choice(DHIKR_PHRASES)
    text = f"{reminder}\n\n🤲 ذكر الصباح:\n{phrase}"
    await _broadcast(context, text)


async def job_hijri(context) -> None:
    """07:00 — Today's Hijri date."""
    text = await _fetch_hijri()
    if text:
        await _broadcast(context, text)


async def job_asmaullah(context) -> None:
    """09:00 — Random name from the 99 Names of Allah."""
    name_ar, meaning_ar = random.choice(ASMA_ALLAH)
    text = (
        f"✨ من أسماء الله الحسنى\n\n"
        f"{name_ar}\n\n"
        f"المعنى: {meaning_ar}"
    )
    await _broadcast(context, text)


async def job_quran_verse(context) -> None:
    """12:00 — Quran verse of the day (Arabic only)."""
    url = f"{ALQURAN_API_BASE}/ayah/random/quran-uthmani"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ayah = data['data']
                    surah_ar = ayah['surah']['name']
                    ayah_num = ayah['numberInSurah']
                    verse_text = ayah['text']
                    text = (
                        f"📖 آية اليوم\n\n"
                        f"﴿{verse_text}﴾\n\n"
                        f"— {surah_ar}، الآية {ayah_num}"
                    )
                    await _broadcast(context, text)
    except Exception as e:
        logger.error(f"job_quran_verse error: {e}")


async def job_dhikr(context) -> None:
    """15:00 — Afternoon dhikr."""
    phrase = random.choice(DHIKR_PHRASES)
    text = f"🤲 ذكر العصر\n\n{phrase}"
    await _broadcast(context, text)


async def job_hadith(context) -> None:
    """18:00 — Hadith of the day."""
    text = await _fetch_random_hadith()
    if text:
        await _broadcast(context, text)


async def job_evening_reminder(context) -> None:
    """21:00 — Evening Islamic reminder + quote."""
    reminder = random.choice(EVENING_REMINDERS)
    quote = random.choice(ISLAMIC_QUOTES)
    text = f"{reminder}\n\n{quote}"
    await _broadcast(context, text)


async def job_3alayesh(context) -> None:
    """Send 'عالايش' to all registered chats."""
    await _broadcast(context, "عالايش")


def setup_scheduled_jobs(application: Application) -> None:
    """Register all daily scheduled jobs. Called from main() before run_polling()."""
    jq = application.job_queue
    if jq is None:
        logger.error(
            "JobQueue is None — APScheduler is likely not installed. "
            "Run: pip install apscheduler==3.10.4"
        )
        return

    jq.run_daily(job_fajr_reminder,    time=time(hour=6,  minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_hijri,            time=time(hour=7,  minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_asmaullah,        time=time(hour=9,  minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_quran_verse,      time=time(hour=12, minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_dhikr,            time=time(hour=15, minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_hadith,           time=time(hour=18, minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_evening_reminder, time=time(hour=21, minute=0,  tzinfo=BEIRUT_TZ))

    # "عالايش" — 8 times between 09:00 and 16:00 (every hour)
    for hour in range(9, 17):
        jq.run_daily(job_3alayesh, time=time(hour=hour, minute=0, tzinfo=BEIRUT_TZ))

    logger.info("Scheduled jobs registered: 7 Islamic + 8 × عالايش (Beirut timezone).")
