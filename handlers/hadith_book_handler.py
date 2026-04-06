import json
import logging
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes

from data.hadith_book_pages import HADITH_PAGES, HADITH_NAMES, TOTAL_HADITHS

logger = logging.getLogger(__name__)

PDF_PATH = Path(__file__).parent.parent / "data" / "CourseBook_Semester2_AlHadith.pdf"
HADITH_INDEX_FILE = Path(__file__).parent.parent / "data" / "hadith_book_index.json"
RENDER_DPI = 150


def render_hadith_pages(hadith_num: int) -> list[bytes]:
    """Render all pages for a hadith as a list of raw JPEG bytes."""
    start, end = HADITH_PAGES[hadith_num]
    doc = fitz.open(PDF_PATH)
    pages = []
    matrix = fitz.Matrix(RENDER_DPI / 72, RENDER_DPI / 72)
    for page_num in range(start - 1, end):  # fitz is 0-indexed
        page = doc[page_num]
        pix = page.get_pixmap(matrix=matrix, alpha=False, colorspace=fitz.csRGB)
        pages.append(pix.tobytes("jpeg"))
    doc.close()
    return pages


def _build_media(pages: list[bytes], caption: str) -> list[InputMediaPhoto]:
    """Wrap raw JPEG bytes in fresh BytesIO objects for a single send."""
    media = []
    for i, data in enumerate(pages):
        buf = BytesIO(data)
        media.append(InputMediaPhoto(media=buf, caption=caption if i == 0 else None))
    return media


def get_next_hadith_index() -> int:
    """Return current hadith index and advance to the next one (cycles 1–21)."""
    if not HADITH_INDEX_FILE.exists():
        HADITH_INDEX_FILE.write_text(json.dumps({"index": 1}))
        return 1
    data = json.loads(HADITH_INDEX_FILE.read_text())
    current = data.get("index", 1)
    next_idx = (current % TOTAL_HADITHS) + 1
    HADITH_INDEX_FILE.write_text(json.dumps({"index": next_idx}))
    return current


async def hadith_book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/hadith_book [number] — send the full lesson pages for a hadith."""
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            f"📖 استخدام: /hadith_book [رقم]\n"
            f"مثال: /hadith_book 1\n"
            f"عدد الأحاديث المتاحة: {TOTAL_HADITHS}"
        )
        return

    num = int(args[0])
    if num < 1 or num > TOTAL_HADITHS:
        await update.message.reply_text(f"❌ الرقم يجب أن يكون بين 1 و {TOTAL_HADITHS}")
        return

    await update.message.reply_text(f"⏳ جارٍ تجهيز الحديث {num}...")
    pages = render_hadith_pages(num)
    caption = f"📖 الحديث {num}: {HADITH_NAMES[num]}"
    media = _build_media(pages, caption)

    for i in range(0, len(media), 10):
        await update.message.reply_media_group(media=media[i:i + 10])


async def send_daily_hadith_book(context) -> None:
    """Daily job: send the next hadith lesson to all scheduled chats."""
    from handlers.islamic_commands import get_scheduled_chats

    hadith_num = get_next_hadith_index()
    pages = render_hadith_pages(hadith_num)
    caption = f"📖 الحديث {hadith_num}: {HADITH_NAMES[hadith_num]}"

    for chat_id in get_scheduled_chats():
        try:
            media = _build_media(pages, caption)  # fresh BytesIO per chat
            for i in range(0, len(media), 10):
                await context.bot.send_media_group(chat_id=chat_id, media=media[i:i + 10])
        except Exception as e:
            logger.error(f"Failed to send hadith book to {chat_id}: {e}")
