import json
import logging
from io import BytesIO
from pathlib import Path

import fitz  # PyMuPDF
from telegram import InputMediaPhoto, Update
from telegram.ext import ContextTypes

from data.aqeedah_book_pages import LECTURE_PAGES, LECTURE_NAMES, TOTAL_LECTURES

logger = logging.getLogger(__name__)

PDF_PATH = Path(__file__).parent.parent / "data" / "CourseBook_Semester2_AlAqeedah.pdf"
LECTURE_INDEX_FILE = Path(__file__).parent.parent / "data" / "aqeedah_book_index.json"
RENDER_DPI = 150


def render_lecture_pages(lecture_num: int) -> list[bytes]:
    """Render all pages for a lecture as a list of raw JPEG bytes."""
    start, end = LECTURE_PAGES[lecture_num]
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


def get_next_lecture_index() -> int:
    """Return current lecture index and advance to the next one (cycles 1–24)."""
    if not LECTURE_INDEX_FILE.exists():
        LECTURE_INDEX_FILE.write_text(json.dumps({"index": 1}))
        return 1
    data = json.loads(LECTURE_INDEX_FILE.read_text())
    current = data.get("index", 1)
    next_idx = (current % TOTAL_LECTURES) + 1
    LECTURE_INDEX_FILE.write_text(json.dumps({"index": next_idx}))
    return current


async def aqeedah_book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/aqeedah_book [number] — send the full lesson pages for an aqeedah lecture."""
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text(
            f"📚 استخدام: /aqeedah_book [رقم]\n"
            f"مثال: /aqeedah_book 1\n"
            f"عدد المحاضرات المتاحة: {TOTAL_LECTURES}"
        )
        return

    num = int(args[0])
    if num < 1 or num > TOTAL_LECTURES:
        await update.message.reply_text(f"❌ الرقم يجب أن يكون بين 1 و {TOTAL_LECTURES}")
        return

    await update.message.reply_text(f"⏳ جارٍ تجهيز المحاضرة {num}...")
    pages = render_lecture_pages(num)
    caption = f"📚 المحاضرة {num}: {LECTURE_NAMES[num]}"
    media = _build_media(pages, caption)

    for i in range(0, len(media), 10):
        await update.message.reply_media_group(media=media[i:i + 10])


async def send_daily_aqeedah_book(context) -> None:
    """Daily job: send the next aqeedah lecture to all scheduled chats."""
    from handlers.islamic_commands import get_scheduled_chats

    lecture_num = get_next_lecture_index()
    pages = render_lecture_pages(lecture_num)
    caption = f"📚 المحاضرة {lecture_num}: {LECTURE_NAMES[lecture_num]}"

    for chat_id in get_scheduled_chats():
        try:
            media = _build_media(pages, caption)  # fresh BytesIO per chat
            for i in range(0, len(media), 10):
                await context.bot.send_media_group(chat_id=chat_id, media=media[i:i + 10])
        except Exception as e:
            logger.error(f"Failed to send aqeedah book to {chat_id}: {e}")
