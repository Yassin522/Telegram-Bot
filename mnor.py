# Python standard library imports
import asyncio
import html
import json
import os
import random
import re
from datetime import datetime, timedelta
from io import BytesIO
from typing import Dict, List, Optional
from urllib.parse import quote, parse

# Third-party imports
import aiohttp
import numpy as np
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

# Telegram-related imports
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    InputFile
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Logging
import logging

import urllib

LEBANON_TZ = pytz.timezone('Asia/Beirut')
DOG_API = "https://dog.ceo/api/breeds/image/random"
CAT_API = "https://api.thecatapi.com/v1/images/search"
FOX_API = "https://randomfox.ca/floof/"
ANIME_QUOTE_API = "https://animechan.xyz/api/random"
POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"
JIKAN_API_BASE = "https://api.jikan.moe/v4"
WAIFU_API = "https://api.waifu.pics/sfw"
TRACE_MOE_API = "https://api.trace.moe/search"
# Add these new command handlers
APIS = {
    'JOKE_API': "https://v2.jokeapi.dev/joke/Any?safe-mode",
    'QUOTE_API': "https://api.quotable.io/random",
    'ACTIVITY_API': "https://www.boredapi.com/api/activity",
    'ADVICE_API': "https://api.adviceslip.com/advice",
    'TRIVIA_API': "https://opentdb.com/api.php?amount=1&type=multiple",
    'NUMBER_API': "http://numbersapi.com/random/math",
    'COUNTRIES_API': "https://restcountries.com/v3.1/all",
    'RECIPE_API': "https://www.themealdb.com/api/json/v1/1/random.php",
    'ISS_API': "http://api.open-notify.org/iss-now.json",
    'GENDER_API': "https://api.genderize.io/?name=",
    'AGE_API': "https://api.agify.io/?name=",
    'NATIONALITY_API': "https://api.nationalize.io/?name=",
    'USER_API': "https://randomuser.me/api/",
    'UNIVERSITY_API': "http://universities.hipolabs.com/search?country="
}
OVERLAYS = {
    "crown": "👑",
    "sunglasses": "😎",
    "hearts": "❤️",
    "stars": "⭐",
    "fire": "🔥"
}

SNAKE_API = "https://api.unsplash.com/photos/random?query=snake&client_id=YOUR_UNSPLASH_API_KEY"


IMGFLIP_USERNAME = 'IMGFLIP_USERNAME'
IMGFLIP_PASSWORD = 'IMGFLIP_PASSWORD'
MISTRAL_API_KEY = 'MISTRAL_API_KEY'




JOKES = [
    "Mardini doesn’t follow fashion trends; fashion follows him!",
    "Mardini doesn’t need best friends; everyone’s already lining up to be in his inner circle!",
    "Mardini doesn’t use maps. The roads just align themselves to take him where he wants!",
    "Why doesn’t Mardini need a passport? Countries are just happy to have him visit!",
    "When Mardini’s friends ask why he stays by the river of Aisha, he says, 'Why leave? The river sings my praises every morning!'",
    "People come to the river of Aisha to relax, but Mardini stays because even the river needs his approval!",
    "Mardini doesn’t need to fish in the river of Aisha; the fish just line up and ask to be his next meal!",
    "Why doesn’t Mardini ever get bored living by the river? Because the river tells him stories from ancient times to keep him entertained!",
    "Mardini doesn’t need a translator; he just smiles, and foreign girls suddenly understand every word he says!",
    "When Mardini talks to foreign girls, they don’t care about the conversation—just the mystery of his Syrian charm!",
    "Mardini says he’s learning foreign languages, but we all know he’s just becoming fluent in the art of flirting!",
    "Why do foreign girls always end up talking to Mardini? His 'hello' comes with a free tour of the river of Aisha!",
    "Mardini doesn’t need dating apps. He just opens his phone and foreign girls show up like it’s a world summit!",
    "Why does Mardini always carry a map? Because he needs to keep track of all the countries where girls want to visit him!",
    "If Mardini ever fell out of a plane, he’d land in a pile of gold coins—without a scratch!",
    "Luck didn’t choose Mardini; Mardini chose luck, and luck has never been the same since!"
    "Why does Mardini always get top grades? Because he knows how to 'read' the professor's mind without opening a book!",
    "Mardini's secret to success? He doesnâ€™t study the night before exams; he negotiates with the exam paper!",
    "Why did Mardini ace the test? He didn't study, but he did master the art of guessing!",
    "Mardini walked into the exam room with nothing but confidence, and somehow, he passed with flying colors!",
    "Mardini's study routine: open book, take nap, wake up a genius!",
    "Why study when you can be Mardini? He simply walks into the exam and the answers fill themselves in!",
    "Mardini doesn't cheat; he just has a telepathic connection with the exam paper.",
    "The real mystery isn't Mardini's gradesâ€”it's how he manages to pass without a single library visit!",
    "Mardini doesnâ€™t need study groups. Heâ€™s a one-man university success story!",
    "Why did Mardini bring sunglasses to the exam? Because his future is way too bright without studying!",
    "Studying hard is for mortals; Mardini is on another level, defying the laws of academics!",
    "Mardiniâ€™s motto: Why memorize formulas when you can charm the professor instead?",

]


DAD_JOKES = [
    "Why don't eggs tell jokes? They'd crack up!",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why did the cookie go to the doctor? Because it was feeling crumbly!",
]

PICKUP_LINES = [
    "Are you a parking ticket? Because you've got FINE written all over you!",
    "Are you a WiFi signal? Because I'm really feeling a connection!",
    "Are you a magician? Because whenever I look at you, everyone else disappears!",
    "Do you have a map? I keep getting lost in your eyes!",
    "Is your name Google? Because you've got everything I've been searching for!",
]

ROASTS = [
    "You're so slow, you came last in a race with a statue!",
    "I'd agree with you but then we'd both be wrong.",
    "If I wanted to kill myself, I'd climb your ego and jump to your IQ!",
    "You're the reason why shampoo has instructions!",
    "I'm not saying you're stupid, you just have bad luck thinking!",
]

COMPLIMENTS = [
    "You're the human equivalent of a pizza slice! 🍕",
    "If you were a box of crayons, you'd be the giant name-brand one with the built-in sharpener! 🖍️",
    "You're more fun than bubble wrap! 💫",
    "You make my dopamine levels go brrr! 🧠",
    "You're like a perfectly ripe avocado! 🥑",
]

WOULD_YOU_RATHER = [
    ("Would you rather have fingers as long as your legs or legs as long as your fingers?", "Long fingers", "Short legs"),
    ("Would you rather speak all languages or play all instruments?", "All languages", "All instruments"),
    ("Would you rather be a dragon or have a dragon?", "Be a dragon", "Have a dragon"),
    ("Would you rather have unlimited shawarma or unlimited mansaf?", "Unlimited shawarma", "Unlimited mansaf"),
    ("Would you rather live in the ocean or in space?", "Ocean", "Space"),
]

TRUTH_QUESTIONS = [
    "What's the most embarrassing thing you've done in public?",
    "What's your worst fashion mistake?",
    "What's the weirdest dream you've ever had?",
    "What's your guilty pleasure song?",
    "What's the most childish thing you still do?",
]

DARE_CHALLENGES = [
    "Send a voice message singing your favorite song!",
    "Text your crush 'I love pineapples' right now!",
    "Change your profile picture to a potato for 1 hour!",
    "Send a message in the group using only emojis!",
    "Write a poem about the person who messaged before you!",
]

FORTUNES = [
    "You will find great fortune in a shawarma wrap today! 🌯",
    "A mysterious stranger will offer you hummus... Accept it! 🥙",
    "Your next cup of Arabic coffee will bring good news! ☕",
    "A friend will need your help with their homework... Run while you can! 🏃‍♂️",
    "Your future is as bright as a thousand falafel balls! 🧆",
]

TONGUE_TWISTERS = [
    "She sells seashells by the seashore.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Peter Piper picked a peck of pickled peppers.",
    "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair.",
    "Red lorry, yellow lorry.",
]

# Dictionary of keywords and responses
KEYWORD_RESPONSES = {

    "قص": "بدك تضل عم تهي انت كبار عاد",
    "قصص": "كمشتك رح قصلك شي تاني ها",
    "حمزة": "شقفة خايف هاد",
    "اغيد": "شقفة فاقس وافقس زلمة بكفرتوتة",
    "مارديني": "الخايف من حط المعجونة المصري المكسيكي الفاقس المشنص الهابب",
    "يحيى": "هب من الحد",
    "سمیر": "يلا جاي ليكني بالسفارة",
    "ري": "حاج ري وكرنجة انت غالبا مارديني ",
    "ير": "حاج ري وكرنجة انت غالبا مارديني ",
    "ر.": "حاج ري وكرنجة انت غالبا مارديني ",
    "الشرع": "الشرع او نحرق الزرع",
    "جولاني": "سيادة الرئيس أحمد الشرع عمك",
    "ياسين": "عمك هاد ويلي بقول عليه مشنص بكون هو المشنص",
    "كوك": "سليف الشغل",
    "علبي": "سليف اليونيتي علبي",
    "تتمادى": "خبزك خبز العباس",
    "منور": "نوووووووووووووووورك",
    "محمود": "سليف الشغل وفلاتر عمو",
    "حمدي": "🧥🔪⚔🗡🏹 مكوع من السود",
    "عمار": "∀ الحلبي قصدك الروسي",
    "فجرت": "سيدي فيرست تايم",
    "اسامة": "يا أخي هالرسالة اسطورية كتير",
    "سوریا": "بتضل بلدك",
    "عربين": "دبان عربين اب راتب",
    "قيد": "كلو من ورا اغيد",
    "فاقس": "عاش",
}



INSPIRATIONAL_QUOTES = [
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Everything you've ever wanted is on the other side of fear.",
    "Success usually comes to those who are too busy to be looking for it."
]

# Add facts about Syria
SYRIA_FACTS = [
    "Damascus is one of the oldest continuously inhabited cities in the world.",
    "Syria has been home to diverse civilizations throughout history.",
    "The ancient city of Palmyra was a major trading hub on the Silk Road.",
    "Syria's cuisine is renowned for dishes like shawarma, falafel, and hummus.",
    "The Umayyad Mosque in Damascus is one of the largest and oldest mosques in the world."
]

# Add weather emojis for different conditions
WEATHER_EMOJIS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧',
    'Snow': '🌨',
    'Thunderstorm': '⛈',
    'Drizzle': '🌦',
    'Mist': '🌫'
}

# Dictionary of meme templates with names and corresponding template IDs
MEME_TEMPLATES = {
    'drake': '181913649',
    'two_buttons': '87743020',
    'distracted_boyfriend': '112126428',
    'bernie_support': '222403160',
    'exit_ramp': '124822590',
    'balloon': '131087935',
    'uno_draw25': '217743513',
    'change_my_mind': '129242436',
    'sad_pablo': '80707627',
    'epic_handshake': '135256802',
    'marked_safe': '161865971',
    'grus_plan': '131940431',
    'waiting_skeleton': '4087833',
    'always_has_been': '252600902',
    'batman_robin': '438680',
    'anakin_padme': '322841258',
    'disaster_girl': '97984',
    'buff_doge': '247375501',
    'woman_yelling_cat': '188390779',
    'trade_offer': '309868304',
    'x_everywhere': '91538330',
    'thinking_about_other_women': '110163934',
    'mocking_spongebob': '102156234',
    'expanding_brain': '93895088',
    'one_does_not_simply': '61579',
    'success_kid': '61544',
    'winnie_pooh': '178591752',
    'bike_fall': '79132341',
    'monkey_puppet': '148909805',
    'got_any_more': '124055727',
    'ancient_aliens': '101470',
    'same_picture': '180190441',
    'trophy_if_i_had_one': '3218037',
    'harold': '27813981',
    'clown_makeup': '195515965',  # Your current meme
    'is_this_a_pigeon': '100777631',
    'boardroom_meeting': '1035805',
    'oprah_you_get_a': '28251713',
    'megamind_peeking': '370867422',
    'blank_nut_button': '119139145',
    'you_guys_getting_paid': '177682295',
    'flex_tape': '166969924',
    'this_is_fine': '55311130',
    'sleeping_shaq': '99683372',
    'laughing_leo': '259237855',
    'inhaling_seagull': '114585149',
    'three_headed_dragon': '187102311',
    'evil_kermit': '84341851',
    'surprised_pikachu': '155067746',
    'the_rock_driving': '21735',
    'the_scroll_of_truth': '123999232',
    'grandma_finds_internet': '61556',
    'spiderman_pointing': '110133729',
    'look_at_me': '29617627',
    'charlie_conspiracy': '92084495'
}




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)





async def inspire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random inspirational quote."""
    quote = random.choice(INSPIRATIONAL_QUOTES)
    await update.message.reply_text(f"✨ {quote}")

async def syria_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fact about Syria."""
    fact = random.choice(SYRIA_FACTS)
    await update.message.reply_text(f"🇸🇾 Did you know? {fact}")

async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send current time in Lebanon."""
    lebanon_time = datetime.now(LEBANON_TZ).strftime("%I:%M %p")
    await update.message.reply_text(f"🕒 Current time in Lebanon: {lebanon_time}")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get weather information for a specified city."""
    if len(context.args) < 1:
        await update.message.reply_text("Please specify a city. Usage: /weather <city>")
        return

    city = ' '.join(context.args)
    API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if response.status == 200:
                    temp = data['main']['temp']
                    condition = data['weather'][0]['main']
                    emoji = WEATHER_EMOJIS.get(condition, '🌍')
                    await update.message.reply_text(
                        f"{emoji} Weather in {city}:\n"
                        f"Temperature: {temp}°C\n"
                        f"Condition: {condition}"
                    )
                else:
                    await update.message.reply_text("City not found. Please check the spelling.")
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch weather information.")

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a poll."""
    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /poll 'question' 'option1' 'option2' ...\n"
            "Example: /poll 'Favorite food?' 'Pizza' 'Burger' 'Shawarma'"
        )
        return

    question = context.args[0]
    options = context.args[1:]
    await update.message.reply_poll(question, options)

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll a dice."""
    result = random.randint(1, 6)
    await update.message.reply_dice()

async def flipcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin."""
    result = random.choice(['Heads', 'Tails'])
    await update.message.reply_text(f"🪙 The coin shows: {result}")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set a reminder."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /remind <minutes> <message>\n"
            "Example: /remind 5 Check the laundry"
        )
        return

    try:
        minutes = int(context.args[0])
        message = ' '.join(context.args[1:])
        
        if minutes <= 0:
            await update.message.reply_text("Please specify a positive number of minutes.")
            return

        await update.message.reply_text(f"I'll remind you about '{message}' in {minutes} minutes!")
        
        await asyncio.sleep(minutes * 60)
        await update.message.reply_text(
            f"⏰ Reminder for {update.message.from_user.mention_html()}:\n"
            f"{message}",
            parse_mode='HTML'
        )
    except ValueError:
        await update.message.reply_text("Please provide a valid number of minutes.")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple calculator."""
    if len(context.args) < 1:
        await update.message.reply_text(
            "Usage: /calc <expression>\n"
            "Example: /calc 2 + 2"
        )
        return

    expression = ' '.join(context.args)
    try:
        # Safely evaluate mathematical expression
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression")
        
        result = eval(expression)
        await update.message.reply_text(f"{expression} = {result}")
    except Exception as e:
        await update.message.reply_text("Invalid expression. Please try again.")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JOKES))

def create_meme(template_id, top_text, bottom_text):
    url = 'https://api.imgflip.com/caption_image'
    params = {
        'template_id': template_id,
        'username': IMGFLIP_USERNAME,
        'password': IMGFLIP_PASSWORD,
        'text0': top_text,
        'text1': bottom_text
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        json_data = response.json()
        if json_data['success']:
            return json_data['data']['url']
        else:
            return "Failed to create meme."
    else:
        return "Error contacting meme API."

# Command handler for /makememe
async def makememe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text('Usage: /makememe <meme_name> <top_text> <bottom_text>')
        return
    
    meme_name = context.args[0].lower()
    top_text = ' '.join(context.args[1:len(context.args)//2+1])
    bottom_text = ' '.join(context.args[len(context.args)//2+1:])

    if meme_name not in MEME_TEMPLATES:
        await update.message.reply_text(f'Invalid meme name. Available templates: {", ".join(MEME_TEMPLATES.keys())}')
        return

    template_id = MEME_TEMPLATES[meme_name]
    meme_url = create_meme(template_id, top_text, bottom_text)
    await update.message.reply_text(meme_url)

# Message handler for keyword responses
async def respond_to_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    for keyword, response in KEYWORD_RESPONSES.items():
        if message_text.strip() == keyword:
            await update.message.reply_text(response)
            return  # Stop checking after the first match


# Start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Use /makememe <meme_name> <top_text> <bottom_text> to create a meme.')


async def templates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Format the dictionary into a readable string
    templates_list = "\n".join([f"'{name}': '{template_id}'" for name, template_id in MEME_TEMPLATES.items()])
    response_message = f"Available meme templates:\n\n{templates_list}"
    await update.message.reply_text(response_message)


async def dadjoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dad joke."""
    joke = random.choice(DAD_JOKES)
    await update.message.reply_text(f"👨 Dad says: {joke}")

async def pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random pickup line."""
    line = random.choice(PICKUP_LINES)
    await update.message.reply_text(f"😉 {line}")

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random roast."""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to someone's message to roast them!")
        return
    
    roast_text = random.choice(ROASTS)
    username = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"🔥 Hey {username}, {roast_text}")

async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random compliment."""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to someone's message to compliment them!")
        return
    
    compliment_text = random.choice(COMPLIMENTS)
    username = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"💝 Hey {username}, {compliment_text}")

async def would_you_rather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a would you rather poll."""
    question, option1, option2 = random.choice(WOULD_YOU_RATHER)
    await update.message.reply_poll(
        question,
        [option1, option2],
        is_anonymous=False,
        type='regular'
    )

async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random truth question."""
    question = random.choice(TRUTH_QUESTIONS)
    await update.message.reply_text(f"🤔 Truth: {question}")

async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dare challenge."""
    challenge = random.choice(DARE_CHALLENGES)
    await update.message.reply_text(f"😈 Dare: {challenge}")

async def fortune(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fortune prediction."""
    fortune_text = random.choice(FORTUNES)
    await update.message.reply_text(f"🔮 Your fortune: {fortune_text}")

async def twister(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random tongue twister."""
    twister_text = random.choice(TONGUE_TWISTERS)
    await update.message.reply_text(f"👅 Try saying this fast:\n{twister_text}")

async def randomchoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Make a random choice between given options."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /choose option1 option2 [option3 ...]")
        return
    
    choice = random.choice(context.args)
    await update.message.reply_text(f"🎲 I choose: {choice}")

async def party(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a virtual party."""
    party_message = "🎉 PARTY TIME! 🎉\n\n"
    party_message += "💃 " * random.randint(3, 7) + "\n"
    party_message += "🕺 " * random.randint(3, 7) + "\n"
    party_message += "🎵 " * random.randint(3, 7)
    await update.message.reply_text(party_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with all available commands."""
    help_text = """
🤖 Available Commands:

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
/dog - Get a random dog picture
/cat - Get a random cat picture
/fox - Get a random fox picture
/pokemon <name> - Get Pokemon info

For more details about any command, use: /<command> help
"""
    await update.message.reply_text(help_text)

async def get_random_dog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dog image."""
    async with aiohttp.ClientSession() as session:
        async with session.get(DOG_API) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(data['message'])
                await update.message.reply_text("🐕 Woof! Here's your random dog!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a dog image right now.")

async def get_random_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random cat image."""
    async with aiohttp.ClientSession() as session:
        async with session.get(CAT_API) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(data[0]['url'])
                await update.message.reply_text("🐱 Meow! Here's your random cat!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a cat image right now.")

async def get_random_fox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fox image."""
    async with aiohttp.ClientSession() as session:
        async with session.get(FOX_API) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(data['image'])
                await update.message.reply_text("🦊 What does the fox say?")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a fox image right now.")

async def get_anime_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random anime quote."""
    async with aiohttp.ClientSession() as session:
        async with session.get(ANIME_QUOTE_API) as response:
            if response.status == 200:
                data = await response.json()
                quote = f"'{data['quote']}'\n- {data['character']} from {data['anime']}"
                await update.message.reply_text(f"🎌 {quote}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch an anime quote right now.")

async def get_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get information about a Pokemon."""
    if not context.args:
        await update.message.reply_text("Please specify a Pokemon name or ID!\nExample: /pokemon pikachu")
        return

    pokemon = context.args[0].lower()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEMON_API}{pokemon}") as response:
            if response.status == 200:
                data = await response.json()
                # Create a formatted message with Pokemon info
                message = (
                    f"🎮 Pokemon: {data['name'].title()}\n"
                    f"📏 Height: {data['height']/10}m\n"
                    f"⚖️ Weight: {data['weight']/10}kg\n"
                    f"📋 Types: {', '.join(t['type']['name'] for t in data['types'])}\n"
                    f"💪 Base Experience: {data['base_experience']}"
                )
                # Send Pokemon sprite if available
                if data['sprites']['front_default']:
                    await update.message.reply_photo(data['sprites']['front_default'])
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Pokemon not found! Check the spelling or try a different one.")

async def generate_wanted_poster(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate a wanted poster for a user's profile picture."""
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    
    if not user.photo:
        await update.message.reply_text("User has no profile picture!")
        return

    photos = await context.bot.get_user_profile_photos(user.id, limit=1)
    if not photos.photos:
        await update.message.reply_text("Couldn't get the profile picture!")
        return

    photo_file = await context.bot.get_file(photos.photos[0][0].file_id)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_file.file_path) as response:
            if response.status == 200:
                img_data = await response.read()
                # Process the image (add wanted text, border, etc.)
                # Send back the processed image
                await update.message.reply_photo(
                    photo=img_data,
                    caption=f"WANTED\n{user.first_name}\nReward: 1,000,000 💰"
                )

async def get_anime_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for anime information."""
    if not context.args:
        await update.message.reply_text("Please specify an anime name!\nExample: /anime 'Naruto'")
        return

    search_query = ' '.join(context.args)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{JIKAN_API_BASE}/anime?q={quote(search_query)}&sfw=true") as response:
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    anime = data['data'][0]
                    # Create a formatted message with anime info
                    message = (
                        f"🎯 Title: {anime['title']}\n"
                        f"🎬 Type: {anime['type']}\n"
                        f"⭐ Rating: {anime['score']}/10\n"
                        f"📅 Episodes: {anime['episodes']}\n"
                        f"📺 Status: {anime['status']}\n\n"
                        f"📝 Synopsis:\n{anime['synopsis'][:300]}...\n\n"
                        f"🔗 More info: {anime['url']}"
                    )
                    if anime['images']['jpg']['image_url']:
                        await update.message.reply_photo(
                            anime['images']['jpg']['image_url'],
                            caption=message
                        )
                    else:
                        await update.message.reply_text(message)
                else:
                    await update.message.reply_text("No anime found with that name!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch anime information right now.")

async def get_random_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random anime recommendation."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{JIKAN_API_BASE}/random/anime") as response:
            if response.status == 200:
                data = await response.json()
                anime = data['data']
                message = (
                    f"🎲 Random Anime Recommendation:\n\n"
                    f"🎯 Title: {anime['title']}\n"
                    f"🎬 Type: {anime['type']}\n"
                    f"⭐ Rating: {anime['score']}/10\n"
                    f"📅 Episodes: {anime['episodes']}\n"
                    f"📺 Status: {anime['status']}\n\n"
                    f"📝 Synopsis:\n{anime['synopsis'][:300]}...\n\n"
                    f"🔗 More info: {anime['url']}"
                )
                if anime['images']['jpg']['image_url']:
                    await update.message.reply_photo(
                        anime['images']['jpg']['image_url'],
                        caption=message
                    )
                else:
                    await update.message.reply_text(message)
            else:
                await update.message.reply_text("Sorry, couldn't fetch a random anime right now.")

async def get_seasonal_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current season's popular anime."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{JIKAN_API_BASE}/seasons/now") as response:
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    top_anime = data['data'][:5]  # Get top 5 seasonal anime
                    message = "🌸 Current Season's Popular Anime:\n\n"
                    for i, anime in enumerate(top_anime, 1):
                        message += (
                            f"{i}. {anime['title']}\n"
                            f"⭐ Rating: {anime['score']}/10\n"
                            f"📅 Episodes: {anime['episodes']}\n"
                            f"➡️ {anime['url']}\n\n"
                        )
                    await update.message.reply_text(message)
                else:
                    await update.message.reply_text("No seasonal anime information available!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch seasonal anime right now.")

async def get_waifu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random waifu image."""
    categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'pat', 'smug', 'bonk', 'smile', 'wave']
    category = random.choice(categories)
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{WAIFU_API}/{category}") as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(
                    data['url'],
                    caption=f"🌸 Here's your {category} waifu!"
                )
            else:
                await update.message.reply_text("Sorry, couldn't fetch a waifu image right now.")

async def search_character(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for an anime character."""
    if not context.args:
        await update.message.reply_text("Please specify a character name!\nExample: /character 'Naruto'")
        return

    search_query = ' '.join(context.args)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{JIKAN_API_BASE}/characters?q={quote(search_query)}") as response:
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    char = data['data'][0]
                    message = (
                        f"👤 Character: {char['name']}\n"
                        f"🎯 Nicknames: {', '.join(char['nicknames']) if char['nicknames'] else 'None'}\n"
                        f"👍 Favorites: {char['favorites']}\n\n"
                        f"📝 About:\n{char['about'][:300]}...\n\n"
                        f"🔗 More info: {char['url']}"
                    )
                    if char['images']['jpg']['image_url']:
                        await update.message.reply_photo(
                            char['images']['jpg']['image_url'],
                            caption=message
                        )
                    else:
                        await update.message.reply_text(message)
                else:
                    await update.message.reply_text("No character found with that name!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch character information right now.")

async def top_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get top anime rankings."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{JIKAN_API_BASE}/top/anime") as response:
            if response.status == 200:
                data = await response.json()
                if data['data']:
                    top_list = data['data'][:10]  # Get top 10 anime
                    message = "🏆 Top 10 Anime of All Time:\n\n"
                    for i, anime in enumerate(top_list, 1):
                        message += (
                            f"{i}. {anime['title']}\n"
                            f"⭐ Rating: {anime['score']}/10\n"
                            f"👥 Members: {anime['members']:,}\n"
                            f"➡️ {anime['url']}\n\n"
                        )
                    await update.message.reply_text(message)
                else:
                    await update.message.reply_text("Couldn't fetch top anime list!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch top anime right now.")

async def get_random_snake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random snake image."""
    # Since the Unsplash API requires authentication, let's use a list of snake images instead
    snake_images = [
        "https://images.unsplash.com/photo-1531386151447-fd76ad50012f",
        "https://images.unsplash.com/photo-1555583743-966c2e51c48d",
        "https://images.unsplash.com/photo-1557178985-891ca9b9b01c",
        "https://images.unsplash.com/photo-1544863082-22dca71e4d26",
        "https://images.unsplash.com/photo-1590691566921-c5e4f00f7d45",
        "https://images.unsplash.com/photo-1531578950034-4398c73a6acb",
        "https://images.unsplash.com/photo-1599586120469-e994995f359f",
        "https://images.unsplash.com/photo-1570741066052-817c6de995c8",
        "https://images.unsplash.com/photo-1585095595205-e68d1b25fc76",
        "https://images.unsplash.com/photo-1531752074002-abf991376d04"
    ]
    
    try:
        # Choose a random snake image from the list
        snake_url = random.choice(snake_images)
        await update.message.reply_photo(snake_url)
        
        # Send a fun snake-related message
        snake_messages = [
            "🐍 Ssssssurprise! Here's your snake!",
            "🐍 Slithering into your chat!",
            "🐍 Don't worry, this one doesn't bite!",
            "🐍 A magnificent serpent appears!",
            "🐍 Look at this beautiful noodle!"
        ]
        await update.message.reply_text(random.choice(snake_messages))
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a snake image right now. Try again later! 🐍")

async def get_random_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random joke."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['JOKE_API']) as response:
            if response.status == 200:
                data = await response.json()
                if data['type'] == 'single':
                    joke = data['joke']
                else:
                    joke = f"{data['setup']}\n\n{data['delivery']}"
                await update.message.reply_text(f"😄 Here's a joke:\n\n{joke}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a joke right now.")

async def get_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random quote."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['QUOTE_API']) as response:
            if response.status == 200:
                data = await response.json()
                quote = f"💭 \"{data['content']}\"\n\n— {data['author']}"
                await update.message.reply_text(quote)
            else:
                await update.message.reply_text("Sorry, couldn't fetch a quote right now.")

async def get_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random activity suggestion."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['ACTIVITY_API']) as response:
            if response.status == 200:
                data = await response.json()
                activity = f"🎯 Activity Suggestion:\n\n{data['activity']}\n\nType: {data['type'].capitalize()}\nParticipants: {data['participants']}"
                await update.message.reply_text(activity)
            else:
                await update.message.reply_text("Sorry, couldn't fetch an activity right now.")

async def get_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get random advice."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['ADVICE_API']) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_text(f"🤔 Advice:\n\n{data['slip']['advice']}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch advice right now.")

async def get_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a trivia question."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['TRIVIA_API']) as response:
            if response.status == 200:
                data = await response.json()
                question = data['results'][0]
                options = question['incorrect_answers'] + [question['correct_answer']]
                random.shuffle(options)
                
                message = f"🎯 Category: {question['category']}\n"
                message += f"❓ Question: {html.unescape(question['question'])}\n\n"
                message += "Options:\n"
                for i, option in enumerate(options, 1):
                    message += f"{i}. {html.unescape(option)}\n"
                
                # Store correct answer in context
                context.user_data['trivia_answer'] = question['correct_answer']
                
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Sorry, couldn't fetch a trivia question right now.")

async def check_trivia_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check trivia answer."""
    if 'trivia_answer' not in context.user_data:
        await update.message.reply_text("No active trivia question! Use /trivia to get a question first.")
        return
    
    user_answer = ' '.join(context.args)
    correct_answer = context.user_data['trivia_answer']
    
    if user_answer.lower() == correct_answer.lower():
        await update.message.reply_text("🎉 Correct! Well done!")
    else:
        await update.message.reply_text(f"❌ Sorry, the correct answer was: {correct_answer}")
    
    del context.user_data['trivia_answer']

async def get_number_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random math fact."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['NUMBER_API']) as response:
            if response.status == 200:
                fact = await response.text()
                await update.message.reply_text(f"🔢 {fact}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a number fact right now.")

async def analyze_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze a name for gender, age, and nationality."""
    if not context.args:
        await update.message.reply_text("Please provide a name!\nUsage: /analyzename John")
        return
    
    name = context.args[0]
    results = {}
    
    async with aiohttp.ClientSession() as session:
        # Get gender prediction
        async with session.get(f"{APIS['GENDER_API']}{name}") as response:
            if response.status == 200:
                data = await response.json()
                results['gender'] = f"{data['gender']} ({data['probability']:.0%})"
        
        # Get age prediction
        async with session.get(f"{APIS['AGE_API']}{name}") as response:
            if response.status == 200:
                data = await response.json()
                results['age'] = data['age']
        
        # Get nationality prediction
        async with session.get(f"{APIS['NATIONALITY_API']}{name}") as response:
            if response.status == 200:
                data = await response.json()
                top_countries = data['country'][:3]
                results['nationality'] = ', '.join([f"{c['country_id']} ({c['probability']:.0%})" for c in top_countries])
    
    message = f"📊 Analysis for '{name}':\n\n"
    message += f"👤 Gender: {results.get('gender', 'Unknown')}\n"
    message += f"🎂 Estimated Age: {results.get('age', 'Unknown')}\n"
    message += f"🌍 Likely Nationalities: {results.get('nationality', 'Unknown')}"
    
    await update.message.reply_text(message)

async def get_random_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get information about a random user."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['USER_API']) as response:
            if response.status == 200:
                data = await response.json()
                user = data['results'][0]
                
                message = "👤 Random User Profile:\n\n"
                message += f"Name: {user['name']['title']} {user['name']['first']} {user['name']['last']}\n"
                message += f"Gender: {user['gender'].capitalize()}\n"
                message += f"Age: {user['dob']['age']}\n"
                message += f"Location: {user['location']['city']}, {user['location']['country']}\n"
                message += f"Email: {user['email']}\n"
                
                await update.message.reply_photo(user['picture']['large'], caption=message)
            else:
                await update.message.reply_text("Sorry, couldn't fetch a random user profile right now.")

async def get_iss_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current location of the International Space Station."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['ISS_API']) as response:
            if response.status == 200:
                data = await response.json()
                lat = float(data['iss_position']['latitude'])
                lon = float(data['iss_position']['longitude'])
                
                message = "🛸 International Space Station Location:\n\n"
                message += f"Latitude: {lat}\n"
                message += f"Longitude: {lon}\n\n"
                message += "View on map: https://www.google.com/maps?q={},{}".format(lat, lon)
                
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Sorry, couldn't fetch ISS location right now.")

async def get_random_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random recipe."""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['RECIPE_API']) as response:
            if response.status == 200:
                data = await response.json()
                meal = data['meals'][0]
                
                # Get ingredients list
                ingredients = []
                for i in range(1, 21):
                    ingredient = meal[f'strIngredient{i}']
                    measure = meal[f'strMeasure{i}']
                    if ingredient and ingredient.strip():
                        ingredients.append(f"• {measure} {ingredient}")
                
                message = f"🍳 {meal['strMeal']}\n\n"
                message += f"Category: {meal['strCategory']}\n"
                message += f"Cuisine: {meal['strArea']}\n\n"
                message += "Ingredients:\n"
                message += '\n'.join(ingredients)
                message += f"\n\nInstructions:\n{meal['strInstructions']}"
                
                if meal['strMealThumb']:
                    await update.message.reply_photo(meal['strMealThumb'], caption=message[:1024])
                    if len(message) > 1024:
                        await update.message.reply_text(message[1024:])
                else:
                    await update.message.reply_text(message)
            else:
                await update.message.reply_text("Sorry, couldn't fetch a recipe right now.")


async def mistral_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /chat command to interact with Mistral LLM
    
    Usage: /chat Your prompt here
    """
    # Check if a prompt is provided
    if not context.args:
        await update.message.reply_text("Please provide a prompt. Usage: /chat Your question or prompt here")
        return

    # Combine all arguments into a single prompt
    prompt = ' '.join(context.args)

    try:
        # Log the incoming request
        logger.info(f"Received chat request: {prompt}")
        
        # Mistral API endpoint
        url = "https://api.mistral.ai/v1/chat/completions"
        
        # Headers for authentication
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        
        # Request payload
        payload = {
            "model": "mistral-small",  # Changed to mistral-small
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        # Send request to Mistral API
        logger.info("Sending request to Mistral API")
        response = requests.post(url, headers=headers, json=payload)
        
        # Log the full response for debugging
        logger.info(f"API Response Status Code: {response.status_code}")
        logger.info(f"API Response Content: {response.text}")
        
        # Check if request was successful
        if response.status_code == 200:
            # Extract the generated response
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            # Send the response back to the Telegram chat
            await update.message.reply_text(generated_text)
            logger.info("Successfully sent response to Telegram")
        else:
            # Handle API errors
            error_message = f"API Error: {response.status_code} - {response.text}"
            logger.error(error_message)
            await update.message.reply_text(f"Sorry, there was an API error: {response.text}")
    
    except requests.RequestException as e:
        # Handle request-specific exceptions
        logger.error(f"Request Exception: {str(e)}")
        await update.message.reply_text(f"Network error: {str(e)}")
    
    except KeyError as e:
        # Handle potential JSON parsing errors
        logger.error(f"Key Error in parsing response: {str(e)}")
        await update.message.reply_text("Sorry, I couldn't process the AI response correctly.")
    
    except Exception as e:
        # Catch and report any unexpected errors
        logger.error(f"Unexpected error: {str(e)}")
        await update.message.reply_text(f"An unexpected error occurred: {str(e)}")



async def word_scramble(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = {
        "PYTHON": "A programming language",
        "TELEGRAM": "A messaging app",
        "COMPUTER": "An electronic device",
        "KEYBOARD": "Used for typing",
        "INTERNET": "Global network"
    }
    
    word, hint = random.choice(list(words.items()))
    scrambled = ''.join(random.sample(word, len(word)))
    
    context.user_data['current_word'] = word
    await update.message.reply_text(
        f"🎮 Word Scramble!\n\nUnscramble this word: {scrambled}\n\nHint: {hint}\n\n"
        "Type /guess <word> to make a guess!"
    )

async def check_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide your guess! Example: /guess WORD")
        return
    
    guess = context.args[0].upper()
    correct_word = context.user_data.get('current_word')
    
    if not correct_word:
        await update.message.reply_text("No active word scramble game! Start one with /scramble")
        return
    
    if guess == correct_word:
        await update.message.reply_text("🎉 Correct! You won!")
        context.user_data.pop('current_word')
    else:
        await update.message.reply_text("❌ Not quite! Try again!")

# Number Guessing Game
async def number_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 100)
    context.user_data['number'] = number
    context.user_data['attempts'] = 0
    
    await update.message.reply_text(
        "🎲 Number Guessing Game!\n\n"
        "I'm thinking of a number between 1 and 100.\n"
        "Use /guess_number <number> to make a guess!"
    )

async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a number! Example: /guess_number 50")
        return
    
    try:
        guess = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Please enter a valid number!")
        return
    
    number = context.user_data.get('number')
    if not number:
        await update.message.reply_text("No active number game! Start one with /numbergame")
        return
    
    context.user_data['attempts'] += 1
    
    if guess == number:
        attempts = context.user_data['attempts']
        await update.message.reply_text(
            f"🎉 Correct! You got it in {attempts} attempts!"
        )
        context.user_data.pop('number')
        context.user_data.pop('attempts')
    elif guess < number:
        await update.message.reply_text("Higher! ⬆️")
    else:
        await update.message.reply_text("Lower! ⬇️")

async def hangman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = ["PYTHON", "TELEGRAM", "BOT", "GAME", "PROGRAMMING", "COMPUTER", "NETWORK"]
    word = random.choice(words)
    guessed_letters = set()
    max_attempts = 6
    
    context.user_data['hangman_word'] = word
    context.user_data['guessed_letters'] = guessed_letters
    context.user_data['attempts_left'] = max_attempts
    
    display = ' '.join('_' for _ in word)
    await update.message.reply_text(
        f"🎯 Hangman Game!\n\n"
        f"Word: {display}\n"
        f"Attempts left: {max_attempts}\n\n"
        "Use /guess_letter <letter> to guess a letter!"
    )

async def guess_letter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a letter! Example: /guess_letter A")
        return
    
    letter = context.args[0].upper()
    if len(letter) != 1:
        await update.message.reply_text("Please enter just one letter!")
        return
    
    word = context.user_data.get('hangman_word')
    if not word:
        await update.message.reply_text("No active hangman game! Start one with /hangman")
        return
    
    guessed_letters = context.user_data['guessed_letters']
    attempts_left = context.user_data['attempts_left']
    
    if letter in guessed_letters:
        await update.message.reply_text("You already guessed that letter!")
        return
    
    guessed_letters.add(letter)
    
    if letter not in word:
        attempts_left -= 1
        context.user_data['attempts_left'] = attempts_left
    
    display = ' '.join(letter if letter in guessed_letters else '_' for letter in word)
    
    if '_' not in display:
        await update.message.reply_text(
            f"🎉 Congratulations! You won!\nThe word was: {word}"
        )
        # Clear game data
        for key in ['hangman_word', 'guessed_letters', 'attempts_left']:
            context.user_data.pop(key)
    elif attempts_left == 0:
        await update.message.reply_text(
            f"Game Over! The word was: {word}"
        )
        # Clear game data
        for key in ['hangman_word', 'guessed_letters', 'attempts_left']:
            context.user_data.pop(key)
    else:
        await update.message.reply_text(
            f"Word: {display}\n"
            f"Guessed letters: {', '.join(sorted(guessed_letters))}\n"
            f"Attempts left: {attempts_left}"
        )

async def random_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch a random GIF based on search term"""
    # You'll need to get an API key from GIPHY
    GIPHY_API_KEY = "TlBJrLX2lAaeCEDx6ngZVdvoebbwKI1C"
    
    search_term = " ".join(context.args) if context.args else "random"
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag={search_term}"
    
    try:
        response = requests.get(url)
        data = response.json()
        gif_url = data['data']['images']['original']['url']
        await update.message.reply_animation(gif_url)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a GIF right now!")

async def create_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a meme with top and bottom text"""
    if not context.args or len(context.args) < 3:
        await update.message.reply_text(
            "Please provide: image URL, top text, and bottom text!\n"
            "Example: /meme https://example.com/image.jpg 'Top text' 'Bottom text'"
        )
        return
    
    try:
        # Parse arguments
        img_url = context.args[0]
        top_text = context.args[1]
        bottom_text = " ".join(context.args[2:])
        
        # Download image
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        
        # Add text to image
        draw = ImageDraw.Draw(img)
        # You'll need to add a font file to your project
        font = ImageFont.truetype("impact.ttf", 60)
        
        # Draw text
        draw.text((img.width/2, 10), top_text, font=font, fill='white', anchor="mt")
        draw.text((img.width/2, img.height-10), bottom_text, font=font, fill='white', anchor="mb")
        
        # Save and send
        bio = BytesIO()
        bio.name = 'meme.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await update.message.reply_photo(photo=bio)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't create the meme!")

async def random_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random sticker from a predefined set"""
    # You'll need to create a list of sticker set names
    sticker_sets = [
        "YourStickerSet1",
        "YourStickerSet2"
    ]
    
    try:
        sticker_set = await context.bot.get_sticker_set(random.choice(sticker_sets))
        sticker = random.choice(sticker_set.stickers)
        await update.message.reply_sticker(sticker=sticker.file_id)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't send a sticker!")

async def apply_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apply various filters to images"""
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Please reply to an image with /filter <effect_name>")
        return
    
    if not context.args:
        await update.message.reply_text("Please specify a filter: grayscale, sepia, blur, or invert")
        return
    
    try:
        # Get the photo file
        photo_file = await update.message.reply_to_message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        img = Image.open(BytesIO(photo_bytes))
        
        filter_name = context.args[0].lower()
        
        if filter_name == "grayscale":
            img = img.convert('L')
        elif filter_name == "sepia":
            width, height = img.size
            pixels = img.load()
            for x in range(width):
                for y in range(height):
                    r, g, b = img.getpixel((x, y))[:3]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    img.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
        elif filter_name == "invert":
            img = Image.eval(img, lambda x: 255 - x)
        
        # Save and send
        bio = BytesIO()
        bio.name = 'filtered_image.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await update.message.reply_photo(photo=bio)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't apply the filter!")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert text to speech using gTTS"""
    if not context.args:
        await update.message.reply_text("Please provide text to convert to speech!")
        return
    
    try:
        from gtts import gTTS
        
        text = " ".join(context.args)
        tts = gTTS(text=text, lang='en')
        
        # Save to BytesIO
        bio = BytesIO()
        tts.write_to_fp(bio)
        bio.seek(0)
        bio.name = "speech.mp3"
        
        await update.message.reply_voice(voice=bio)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't convert text to speech!")

async def mardini_transform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transform Mardini's photos in funny ways"""
    # Check if replying to a message with photo
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Reply to one of @OmarMardini's photos with /mardinitransform!")
        return
    
    # Check if the photo is from Mardini
    if update.message.reply_to_message.from_user.username != "OmarMardini":
        await update.message.reply_text("This command only works on @OmarMardini's photos! 📸")
        return

    try:
        # Get the photo file
        photo_file = await update.message.reply_to_message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        img = Image.open(BytesIO(photo_bytes))

        # Random transformation selection
        transform_type = random.choice([
            "superhero",
            "wanted",
            "magazine",
            "meme",
            "art",
            "emoji"
        ])

        if transform_type == "superhero":
            img = await superhero_transform(img)
        elif transform_type == "wanted":
            img = await wanted_transform(img)
        elif transform_type == "magazine":
            img = await magazine_transform(img)
        elif transform_type == "meme":
            img = await meme_transform(img)
        elif transform_type == "art":
            img = await art_transform(img)
        else:
            img = await emoji_transform(img)

        # Save and send the transformed image
        bio = BytesIO()
        bio.name = 'mardini_transformed.png'
        img.save(bio, 'PNG')
        bio.seek(0)

        await update.message.reply_photo(
            photo=bio,
            caption=f"Behold! Mardini has been transformed! ✨ ({transform_type.title()} Edition)"
        )

    except Exception as e:
        await update.message.reply_text("Oops! The transformation failed! Maybe Mardini is too powerful! 😅")

async def superhero_transform(img):
    """Transform Mardini into a superhero"""
    # Add cape effect
    img = img.convert('RGBA')
    
    # Enhance colors
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.5)
    
    # Add superhero mask overlay
    draw = ImageDraw.Draw(img)
    width, height = img.size
    draw.ellipse([width//3, height//8, 2*width//3, height//3], fill=(0,0,0,128))
    
    # Add glowing effect
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.2)
    
    return img

async def wanted_transform(img):
    """Transform Mardini into a wanted poster"""
    # Convert to sepia tone
    width, height = img.size
    img = img.convert('RGB')
    
    # Create wanted poster template
    wanted = Image.new('RGB', (width, height + 100), color='antiquewhite')
    wanted.paste(img, (0, 50))
    
    # Add text
    draw = ImageDraw.Draw(wanted)
    draw.text((width//2, 25), "WANTED", fill='black', anchor="mm")
    draw.text((width//2, height+75), 
              f"REWARD: {random.randint(100,999999)}$\nLast seen being awesome", 
              fill='black', anchor="mm", align="center")
    
    return wanted

async def magazine_transform(img):
    """Transform Mardini into a magazine cover"""
    width, height = img.size
    
    # Create magazine cover
    cover = Image.new('RGB', (width, height), color='white')
    cover.paste(img, (0, 0))
    
    # Add magazine elements
    draw = ImageDraw.Draw(cover)
    
    headlines = [
        "MARDINI: The Legend Continues",
        "Exclusive: A Day in the Life of Mardini",
        "Breaking: Mardini's Secret to Awesomeness",
        "The Mardini Effect: How One Person Changed Everything"
    ]
    
    draw.text((width//2, 30), random.choice(headlines), 
              fill='white', anchor="mm", stroke_width=2, stroke_fill='black')
    
    return cover

async def meme_transform(img):
    """Transform Mardini into a meme"""
    width, height = img.size
    
    # Create meme template
    meme = Image.new('RGB', (width, height + 100), color='white')
    meme.paste(img, (0, 0))
    
    # Add meme text
    draw = ImageDraw.Draw(meme)
    
    meme_texts = [
        "When someone says they don't know Mardini",
        "Mardini: *exists*\nEveryone: LEGEND",
        "Nobody:\nAbsolutely nobody:\nMardini: *being awesome*",
        "Level 999 Mardini Boss"
    ]
    
    draw.text((width//2, height+50), random.choice(meme_texts),
              fill='black', anchor="mm", align="center")
    
    return meme

async def art_transform(img):
    """Transform Mardini into art style"""
    # Convert to artistic effect
    img = img.convert('RGB')
    
    # Posterize effect
    img = ImageOps.posterize(img, 3)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    return img

async def emoji_transform(img):
    """Add random emoji overlays to Mardini"""
    img = img.convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    # Add random emojis around the image
    width, height = img.size
    for _ in range(10):
        x = random.randint(0, width)
        y = random.randint(0, height)
        emoji = random.choice(list(OVERLAYS.values()))
        draw.text((x, y), emoji, fill=(255,255,255,200))
    
    return img

def add_mardini_transform_handler(application):
    """Add the Mardini transform handler to the application"""
    application.add_handler(CommandHandler('mardinitransform', mardini_transform))
async def translate_text(session, text):
    """Translate text to Arabic using MyMemory API"""
    encoded_text = urllib.parse.quote(text)
    url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=en|ar"
    
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return data['responseData']['translatedText']
        return None

async def get_random_word(session):
    """Get a random word using DataMuse API"""
    # Get words that start with different letters to ensure variety
    start_letter = random.choice('abcdefghijklmnopqrstuvwxyz')
    url = f"https://api.datamuse.com/words?sp={start_letter}*&md=p&max=100"
    
    async with session.get(url) as response:
        if response.status == 200:
            words = await response.json()
            if words:
                # Choose a random word from the results
                word_data = random.choice(words)
                word = word_data['word']
                # Get part of speech if available, otherwise mark as 'unknown'
                tags = word_data.get('tags', [])
                word_type = next((tag for tag in tags if tag in ['n', 'v', 'adj']), 'unknown')
                
                # Convert tag to full word
                word_type_map = {
                    'n': 'noun',
                    'v': 'verb',
                    'adj': 'adjective',
                    'unknown': 'word'
                }
                
                return word, word_type_map.get(word_type, 'word')
    return None, None

async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random word with its definition and Arabic translation"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get random word from DataMuse
            word, word_type = await get_random_word(session)
            
            if not word:
                await update.message.reply_text("Sorry, couldn't get a random word. Please try again!")
                return
                
            # Get Arabic translation of the word
            arabic_word = await translate_text(session, word)
            
            # Get definition using Free Dictionary API
            async with session.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}') as dict_response:
                if dict_response.status == 200:
                    dict_data = await dict_response.json()
                    meanings = dict_data[0]['meanings']
                    definition = meanings[0]['definitions'][0]['definition']
                    part_of_speech = meanings[0]['partOfSpeech']
                    
                    # Get Arabic translation of the definition
                    arabic_definition = await translate_text(session, definition)
                    
                    message = (
                        f"📚 Word: *{word}*\n"
                        f"🌍 Arabic Translation: *{arabic_word}*\n"
                        f"🔤 Part of Speech: _{part_of_speech}_\n"
                        f"📝 English Definition: {definition}\n"
                        f"📝 Arabic Definition: {arabic_definition}"
                    )
                else:
                    # Fallback message if no definition is available
                    message = (
                        f"📚 Word: *{word}*\n"
                        f"🌍 Arabic Translation: *{arabic_word}*\n"
                        f"🔤 Type: _{word_type}_\n"
                        f"_(No detailed definition available)_"
                    )
                    
            await update.message.reply_text(message, parse_mode='Markdown')
                
    except Exception as e:
        await update.message.reply_text(f"Oops! Something went wrong: {str(e)}\nPlease try again!")

def add_random_word_handler(application):
    """Add the random word handler to the application"""
    application.add_handler(CommandHandler('randomword', random_word))


async def add_keyword_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command to add a new keyword and response to the KEYWORD_RESPONSES dictionary.
    Prevents OmarMardini from adding keywords.
    """
    # Check if the user is OmarMardini
    if update.effective_user.username == 'OmarMardini':
        await update.message.reply_text("Sorry, you are not allowed to add keywords.")
        return
    
    # Check if the command has enough arguments
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /addkeyword keyword response")
        return
    
    # Extract the keyword (first argument) and response (rest of the arguments)
    keyword = context.args[0].lower()
    response = " ".join(context.args[1:])
    
    # Add to the KEYWORD_RESPONSES dictionary
    KEYWORD_RESPONSES[keyword] = response
    
    # Confirm the addition
    await update.message.reply_text(f"Added keyword '{keyword}' with response: {response}")

async def recursive_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Special handling for /recursive command to trigger /dog without stopping further processing
    """
    # Send the /dog command
    await update.message.reply_text("/dog")
    
    # Explicitly return None to allow normal command processing to continue
    return None


if __name__ == '__main__':
    # Replace 'YOUR_TOKEN' with your bot's API token from Telegram
    application = ApplicationBuilder().token('TELEGRAM_BOT_TOKEN').build()

    # Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('makememe', makememe))
    application.add_handler(CommandHandler('templates', templates))  # Add templates command


    application.add_handler(CommandHandler('inspire', inspire))
    application.add_handler(CommandHandler('syriafact', syria_fact))
    application.add_handler(CommandHandler('time', time))
    application.add_handler(CommandHandler('weather', weather))
    application.add_handler(CommandHandler('poll', poll))
    application.add_handler(CommandHandler('dice', dice))
    application.add_handler(CommandHandler('flipcoin', flipcoin))
    application.add_handler(CommandHandler('remind', remind))
    application.add_handler(CommandHandler('calc', calculate))
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
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('dog', get_random_dog))
    application.add_handler(CommandHandler('cat', get_random_cat))
    application.add_handler(CommandHandler('fox', get_random_fox))
    application.add_handler(CommandHandler('anime', get_anime_quote))
    application.add_handler(CommandHandler('pokemon', get_pokemon))
    application.add_handler(CommandHandler('wanted', generate_wanted_poster))
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

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_keywords))
    application.add_handler(CommandHandler('joke', joke))
    application.add_handler(CommandHandler('scramble', word_scramble))
    application.add_handler(CommandHandler('guess', check_guess))
    application.add_handler(CommandHandler('numbergame', number_game))
    application.add_handler(CommandHandler('guess_number', check_number))
    application.add_handler(CommandHandler('hangman', hangman))
    application.add_handler(CommandHandler('guess_letter', guess_letter))
    application.add_handler(CommandHandler('gif', random_gif))
    application.add_handler(CommandHandler('meme', create_meme))
    application.add_handler(CommandHandler('sticker', random_sticker))
    application.add_handler(CommandHandler('filter', apply_filter))
    application.add_handler(CommandHandler('speak', text_to_speech))
    add_mardini_transform_handler(application)
    add_random_word_handler(application)
    application.add_handler(CommandHandler('addkeyword', add_keyword_response))
    application.add_handler(CommandHandler('recursive', recursive_command))

    # Start the bot
    application.run_polling()
