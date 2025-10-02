"""
Configuration for the Telegram Bot. Values are loaded from environment variables.
Use a `.env` file during development.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

# Bot Configuration (required)
BOT_TOKEN = require_env('BOT_TOKEN')

# API Keys (some required by features that use them)
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
IMGFLIP_USERNAME = os.getenv('IMGFLIP_USERNAME')
IMGFLIP_PASSWORD = os.getenv('IMGFLIP_PASSWORD')
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')

# Optional API Keys
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Bot Configuration
LEBANON_TZ = os.getenv('LEBANON_TZ', 'Asia/Beirut')
AUTHORIZED_USERS = set(filter(None, (os.getenv('AUTHORIZED_USERS', '').split(','))))

# API Endpoints
DOG_API = "https://dog.ceo/api/breeds/image/random"
CAT_API = "https://api.thecatapi.com/v1/images/search"
FOX_API = "https://randomfox.ca/floof/"
ANIME_QUOTE_API = "https://animechan.xyz/api/random"
POKEMON_API = "https://pokeapi.co/api/v2/pokemon/"
JIKAN_API_BASE = "https://api.jikan.moe/v4"
WAIFU_API = "https://api.waifu.pics/sfw"
TRACE_MOE_API = "https://api.trace.moe/search"

# General APIs
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

# Emoji overlays for image transformations
OVERLAYS = {
    "crown": "👑",
    "sunglasses": "😎",
    "hearts": "❤️",
    "stars": "⭐",
    "fire": "🔥"
}

# Weather emojis
WEATHER_EMOJIS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧',
    'Snow': '🌨',
    'Thunderstorm': '⛈',
    'Drizzle': '🌦',
    'Mist': '🌫'
}

# Meme templates
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
    'clown_makeup': '195515965',
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
