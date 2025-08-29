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
from handlers.fun_commands import (
    joke, dadjoke, pickup, roast, compliment, would_you_rather,
    truth, dare, fortune, twister, randomchoice, party,
    inspire, syria_fact, flipcoin, dice, word_scramble,
    check_guess, number_game, check_number, hangman, guess_letter
)

from handlers.utility_commands import (
    time, weather, poll, remind, calculate, qr_code,
    ip_info, github_user
)

from handlers.api_commands import (
    get_random_dog, get_random_cat, get_random_fox, get_anime_quote,
    get_pokemon, get_random_snake, get_random_joke, get_quote,
    get_activity, get_advice, get_trivia, check_trivia_answer,
    get_number_fact, analyze_name, get_random_user, get_iss_location,
    get_random_recipe, mistral_chat, get_drum_photo, random_gif,
    nasa_pic, useless_fact, crypto_price, chuck_norris, urban_dict,
    color_palette, bored_activity, programming_quote, dog_breed
)

from handlers.message_handlers import (
    respond_to_keywords, check_message, filter_inappropriate_words_handler,
    add_keyword_response, add_insult, show_leaderboard, recursive_command
)

from handlers.meme_handlers import (
    makememe, templates, create_meme_custom, apply_filter,
    mardini_transform, text_to_speech, random_sticker
)

# Import additional handlers that need special setup
from handlers.meme_handlers import mardini_transform
from handlers.api_commands import get_random_word

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
        'Hi! I\'m your multi-functional Telegram bot! Use /help to see all available commands.'
    )))
    
    # Fun commands
    application.add_handler(CommandHandler('joke', joke))
    application.add_handler(CommandHandler('dadjoke', dadjoke))
    application.add_handler(CommandHandler('pickup', pickup))
    application.add_handler(CommandHandler('roast', roast))
    application.add_handler(CommandHandler('compliment', compliment))
    application.add_handler(CommandHandler('wyr', would_you_rather))
    application.add_handler(CommandHandler('truth', truth))
    application.add_handler(CommandHandler('dare', dare))
    application.add_handler(CommandHandler('fortune', fortune))
    application.add_handler(CommandHandler('twister', twister))
    application.add_handler(CommandHandler('choose', randomchoice))
    application.add_handler(CommandHandler('party', party))
    application.add_handler(CommandHandler('inspire', inspire))
    application.add_handler(CommandHandler('syriafact', syria_fact))
    application.add_handler(CommandHandler('flipcoin', flipcoin))
    application.add_handler(CommandHandler('dice', dice))
    
    # Game commands
    application.add_handler(CommandHandler('scramble', word_scramble))
    application.add_handler(CommandHandler('guess', check_guess))
    application.add_handler(CommandHandler('numbergame', number_game))
    application.add_handler(CommandHandler('guess_number', check_number))
    application.add_handler(CommandHandler('hangman', hangman))
    application.add_handler(CommandHandler('guess_letter', guess_letter))
    
    # Utility commands
    application.add_handler(CommandHandler('time', time))
    application.add_handler(CommandHandler('weather', weather))
    application.add_handler(CommandHandler('poll', poll))
    application.add_handler(CommandHandler('remind', remind))
    application.add_handler(CommandHandler('calc', calculate))
    application.add_handler(CommandHandler('qr_code', qr_code))
    application.add_handler(CommandHandler('ip_info', ip_info))
    application.add_handler(CommandHandler('github_user', github_user))
    
    # API-based commands
    application.add_handler(CommandHandler('dog', get_random_dog))
    application.add_handler(CommandHandler('cat', get_random_cat))
    application.add_handler(CommandHandler('fox', get_random_fox))
    application.add_handler(CommandHandler('anime', get_anime_quote))
    application.add_handler(CommandHandler('pokemon', get_pokemon))
    application.add_handler(CommandHandler('snake', get_random_snake))
    application.add_handler(CommandHandler('quote', get_quote))
    application.add_handler(CommandHandler('activity', get_activity))
    application.add_handler(CommandHandler('advice', get_advice))
    application.add_handler(CommandHandler('trivia', get_trivia))
    application.add_handler(CommandHandler('answer', check_trivia_answer))
    application.add_handler(CommandHandler('numberfact', get_number_fact))
    application.add_handler(CommandHandler('analyzename', analyze_name))
    application.add_handler(CommandHandler('randomuser', get_random_user))
    application.add_handler(CommandHandler('iss', get_iss_location))
    application.add_handler(CommandHandler('recipe', get_random_recipe))
    application.add_handler(CommandHandler('chat', mistral_chat))
    application.add_handler(CommandHandler('Hamdi', get_drum_photo))
    application.add_handler(CommandHandler('Hamdi_d', get_drum_photo))
    
    # Additional API commands
    application.add_handler(CommandHandler('nasa_pic', nasa_pic))
    application.add_handler(CommandHandler('useless_fact', useless_fact))
    application.add_handler(CommandHandler('crypto_price', crypto_price))
    application.add_handler(CommandHandler('chuck_norris', chuck_norris))
    application.add_handler(CommandHandler('urban_dict', urban_dict))
    application.add_handler(CommandHandler('color_palette', color_palette))
    application.add_handler(CommandHandler('bored_activity', bored_activity))
    application.add_handler(CommandHandler('programming_quote', programming_quote))
    application.add_handler(CommandHandler('mardono', dog_breed))
    
    # Meme and image commands
    application.add_handler(CommandHandler('makememe', makememe))
    application.add_handler(CommandHandler('templates', templates))
    application.add_handler(CommandHandler('meme', create_meme_custom))
    application.add_handler(CommandHandler('filter', apply_filter))
    application.add_handler(CommandHandler('speak', text_to_speech))
    application.add_handler(CommandHandler('sticker', random_sticker))
    application.add_handler(CommandHandler('mardinitransform', mardini_transform))
    
    # GIF and animation
    application.add_handler(CommandHandler('gif', random_gif))
    
    # Message handling commands
    application.add_handler(CommandHandler('addkeyword', add_keyword_response))
    application.add_handler(CommandHandler('addinsult', add_insult))
    application.add_handler(CommandHandler('leaderboard', show_leaderboard))
    application.add_handler(CommandHandler('recursive', recursive_command))
    
    # Message handlers (for text messages)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_keywords))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    
    # Help command
    application.add_handler(CommandHandler('help', lambda u, c: u.message.reply_text(
        """🤖 Available Commands:

Fun Commands:
/joke - Get a random joke
/dadjoke - Get a dad joke
/pickup - Get a pickup line
/roast - Roast someone (reply to their message)
/compliment - Compliment someone (reply to their message)
/wyr - Would you rather...?
/truth - Get a truth question
/dare - Get a dare challenge
/fortune - Get your fortune told
/twister - Get a tongue twister
/choose - Make a random choice
/party - Start a virtual party!
/flipcoin - Flip a coin
/dice - Roll a dice

Game Commands:
/scramble - Word scramble game
/hangman - Hangman game
/numbergame - Number guessing game

Useful Commands:
/makememe - Create a meme
/templates - Show meme templates
/inspire - Get an inspirational quote
/syriafact - Learn about Syria
/time - Check time in Lebanon
/weather <city> - Get weather info
/poll - Create a poll
/remind - Set a reminder
/calc - Calculator
/qr_code - Generate QR code
/ip_info - Get IP information
/github_user - Get GitHub user info

Animal Commands:
/dog - Get a random dog picture
/cat - Get a random cat picture
/fox - Get a random fox picture
/snake - Get a random snake picture

API Commands:
/quote - Get a random quote
/activity - Get activity suggestion
/advice - Get random advice
/trivia - Get a trivia question
/chat - Chat with AI
/nasa_pic - NASA picture of the day
/crypto_price - Get cryptocurrency prices
/chuck_norris - Get Chuck Norris facts

For more details about any command, use: /<command> help
"""
    )))
    
    logger.info("All handlers have been set up successfully!")


def main():
    """Main function to start the bot"""
    try:
        # Create the application
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Setup all handlers
        setup_handlers(application)
        
        # Start the bot
        logger.info("Starting bot...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise


if __name__ == '__main__':
    main()
