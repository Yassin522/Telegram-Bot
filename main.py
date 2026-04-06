"""
Main entry point for the Telegram Bot
"""
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

# Import configuration
from config import BOT_TOKEN

# Import handlers
from handlers.api_commands import (
    get_anime_quote, get_pokemon, get_quote,
    get_activity, get_advice,
    get_number_fact, analyze_name, get_random_user, get_iss_location,
    get_random_recipe, mistral_chat, random_gif,
    useless_fact, urban_dict,
    color_palette, bored_activity, programming_quote, dog_breed,
    get_random_word, get_drum_photo
)

from handlers.message_handlers import (
    respond_to_keywords, check_message, filter_inappropriate_words_handler,
    add_keyword_response, add_insult, show_leaderboard, recursive_command,
)

from handlers.meme_handlers import (
    create_meme_custom, apply_filter,
    mardini_transform, text_to_speech
)

from handlers.islamic_commands import (
    prayer_times, quran_verse, hadith, hijri_date, asmaullah, dhikr,
    set_schedule, unset_schedule,
    aqeedah, salaf_quote, tawheed, sunnah_practice
)
from handlers.scheduled_jobs import setup_scheduled_jobs

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def setup_handlers(application):
    """Setup all command and message handlers"""

    # Basic commands
    application.add_handler(CommandHandler('start', lambda u, c: u.message.reply_text(
        'أهلاً! أنا بوتك الإسلامي. استخدم /help لرؤية الأوامر المتاحة.'
    )))

    # AI & general API commands
    application.add_handler(CommandHandler('chat',           mistral_chat))
    application.add_handler(CommandHandler('activity',       get_activity))
    application.add_handler(CommandHandler('advice',         get_advice))
    application.add_handler(CommandHandler('numberfact',     get_number_fact))
    application.add_handler(CommandHandler('analyzename',    analyze_name))
    application.add_handler(CommandHandler('randomuser',     get_random_user))
    application.add_handler(CommandHandler('iss',            get_iss_location))
    application.add_handler(CommandHandler('recipe',         get_random_recipe))
    application.add_handler(CommandHandler('useless_fact',   useless_fact))
    application.add_handler(CommandHandler('urban_dict',     urban_dict))
    application.add_handler(CommandHandler('color_palette',  color_palette))
    application.add_handler(CommandHandler('bored_activity', bored_activity))
    application.add_handler(CommandHandler('programming_quote', programming_quote))
    application.add_handler(CommandHandler('mardono',        dog_breed))
    application.add_handler(CommandHandler('randomword',     get_random_word))
    application.add_handler(CommandHandler('gif',            random_gif))
    application.add_handler(CommandHandler('Hamdi',          get_drum_photo))
    application.add_handler(CommandHandler('Hamdi_d',        get_drum_photo))

    # Image / media commands
    application.add_handler(CommandHandler('meme',           create_meme_custom))
    application.add_handler(CommandHandler('filter',         apply_filter))
    application.add_handler(CommandHandler('speak',          text_to_speech))
    application.add_handler(CommandHandler('mardinitransform', mardini_transform))

    # Islamic commands
    application.add_handler(CommandHandler('prayer',         prayer_times))
    application.add_handler(CommandHandler('quran',          quran_verse))
    application.add_handler(CommandHandler('hadith',         hadith))
    application.add_handler(CommandHandler('hijri',          hijri_date))
    application.add_handler(CommandHandler('asmaullah',      asmaullah))
    application.add_handler(CommandHandler('dhikr',          dhikr))
    application.add_handler(CommandHandler('setschedule',    set_schedule))
    application.add_handler(CommandHandler('unsetschedule',  unset_schedule))

    # Aqeedah of the Salaf
    application.add_handler(CommandHandler('aqeedah',        aqeedah))
    application.add_handler(CommandHandler('salaf',          salaf_quote))
    application.add_handler(CommandHandler('tawheed',        tawheed))
    application.add_handler(CommandHandler('sunnah',         sunnah_practice))

    # Group management commands
    application.add_handler(CommandHandler('addkeyword',     add_keyword_response))
    application.add_handler(CommandHandler('addinsult',      add_insult))
    application.add_handler(CommandHandler('leaderboard',    show_leaderboard))
    application.add_handler(CommandHandler('recursive',      recursive_command))

    # Message handlers — separate groups so all three always run
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message), group=0)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_keywords), group=1)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_inappropriate_words_handler), group=2)

    # Help command
    application.add_handler(CommandHandler('help', lambda u, c: u.message.reply_text(
        """🤖 الأوامر المتاحة:

الأوامر الإسلامية:
/prayer <مدينة> - مواقيت الصلاة
/quran - آية قرآنية عشوائية
/hadith - حديث شريف عشوائي
/hijri - التاريخ الهجري اليوم
/asmaullah - اسم عشوائي من أسماء الله الحسنى
/dhikr - ذكر عشوائي
/setschedule - تفعيل المنشورات اليومية في هذه المجموعة
/unsetschedule - إيقاف المنشورات اليومية

عقيدة السلف:
/aqeedah - مسألة عقدية من عقيدة أهل السنة
/salaf - قول من أقوال السلف الصالح
/tawheed - من أنواع التوحيد وأدلتها
/sunnah - سنة نبوية مع دليلها

المنشورات اليومية التلقائية:
🌅 06:00 - تذكير الفجر وذكر الصباح
🗓 07:00 - التاريخ الهجري
✨ 09:00 - اسم من أسماء الله الحسنى
📖 12:00 - آية قرآنية
🤲 15:00 - ذكر
📚 18:00 - حديث شريف
🌙 21:00 - تذكير مسائي

أوامر أخرى:
/chat <سؤال> - محادثة مع الذكاء الاصطناعي
/advice - نصيحة عشوائية
/recipe - وصفة طعام عشوائية
/gif [كلمة] - صورة متحركة
/urban_dict <كلمة> - تعريف من Urban Dictionary
/meme <رابط> '<نص علوي>' '<نص سفلي>' - إنشاء ميم
/filter grayscale|sepia|blur - تطبيق فلتر على صورة
/speak <نص> - تحويل نص إلى صوت
/mardinitransform - تحويل صورة مارديني

إدارة المجموعة:
/addkeyword <كلمة> <رد> - إضافة كلمة مفتاحية
/addinsult <كلمة> - إضافة كلمة محظورة
/leaderboard - لوحة الشرف للكلمات المحظورة
"""
    )))

    logger.info("All handlers have been set up successfully!")


def main():
    """Main function to start the bot"""
    try:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        setup_handlers(application)
        setup_scheduled_jobs(application)
        logger.info("Starting bot...")
        application.run_polling()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise


if __name__ == '__main__':
    main()
