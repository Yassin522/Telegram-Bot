"""
Media command handlers
"""
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes


async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert text to speech using gTTS"""
    if not context.args:
        await update.message.reply_text("الاستخدام: /speak <النص>")
        return

    try:
        from gtts import gTTS

        text = " ".join(context.args)
        tts = gTTS(text=text, lang='ar')

        bio = BytesIO()
        tts.write_to_fp(bio)
        bio.seek(0)
        bio.name = "speech.mp3"

        await update.message.reply_voice(voice=bio)
    except ImportError:
        await update.message.reply_text("gTTS library not installed.")
    except Exception as e:
        await update.message.reply_text(f"تعذّر تحويل النص إلى صوت: {str(e)}")
