"""
Scheduled daily Islamic auto-post jobs.
"""
import logging
import random
from datetime import time

import aiohttp
import pytz
from telegram.ext import Application

from config import ALQURAN_API_BASE, HADITH_API_BASE
from data.islamic_data import DHIKR_PHRASES, ISLAMIC_QUOTES, FAJR_REMINDERS, EVENING_REMINDERS
from handlers.islamic_commands import get_scheduled_chats

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
    """06:00 Beirut — Morning Fajr reminder + dhikr."""
    reminder = random.choice(FAJR_REMINDERS)
    dhikr = random.choice(DHIKR_PHRASES)
    text = f"{reminder}\n\n🤲 ذكر الصباح:\n{dhikr}"
    await _broadcast(context, text)


async def job_quran_verse(context) -> None:
    """12:00 Beirut — Quran verse of the day (Arabic only)."""
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


async def job_hadith(context) -> None:
    """18:00 Beirut — Hadith of the day (Arabic text)."""
    hadith_num = random.randint(1, 300)
    url = f"{HADITH_API_BASE}/books/bukhari?range={hadith_num}-{hadith_num}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    hadiths = data.get('data', {}).get('hadiths', [])
                    if hadiths:
                        h = hadiths[0]
                        num = h.get('number', hadith_num)
                        text = (
                            f"📚 حديث اليوم\n"
                            f"صحيح البخاري — رقم {num}\n\n"
                            f"{h['arab']}"
                        )
                        await _broadcast(context, text)
    except Exception as e:
        logger.error(f"job_hadith error: {e}")


async def job_evening_reminder(context) -> None:
    """21:00 Beirut — Evening Islamic reminder."""
    reminder = random.choice(EVENING_REMINDERS)
    quote = random.choice(ISLAMIC_QUOTES)
    text = f"{reminder}\n\n{quote}"
    await _broadcast(context, text)


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
    jq.run_daily(job_quran_verse,      time=time(hour=12, minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_hadith,           time=time(hour=18, minute=0,  tzinfo=BEIRUT_TZ))
    jq.run_daily(job_evening_reminder, time=time(hour=21, minute=0,  tzinfo=BEIRUT_TZ))

    logger.info("Scheduled Islamic jobs registered (Beirut timezone).")
