"""
API-based command handlers
"""
import random
import aiohttp
import html
from urllib.parse import quote
from telegram import Update
from telegram.ext import ContextTypes
from config import (
    DOG_API, CAT_API, FOX_API, ANIME_QUOTE_API, POKEMON_API,
    JIKAN_API_BASE, WAIFU_API, APIS, MISTRAL_API_KEY, GIPHY_API_KEY,
    UNSPLASH_ACCESS_KEY
)

async def get_random_dog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dog image"""
    async with aiohttp.ClientSession() as session:
        async with session.get(DOG_API) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(data['message'])
                await update.message.reply_text("🐕 Woof! Here's your random dog!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a dog image right now.")


async def get_random_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random cat image"""
    async with aiohttp.ClientSession() as session:
        async with session.get(CAT_API) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(data[0]['url'])
                await update.message.reply_text("🐱 Meow! Here's your random cat!")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a cat image right now.")


async def get_random_fox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fox image"""
    async with aiohttp.ClientSession() as session:
        async with session.get(FOX_API) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_photo(data['image'])
                await update.message.reply_text("🦊 What does the fox say?")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a fox image right now.")


async def get_anime_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random anime quote"""
    async with aiohttp.ClientSession() as session:
        async with session.get(ANIME_QUOTE_API) as response:
            if response.status == 200:
                data = await response.json()
                quote = f"'{data['quote']}'\n- {data['character']} from {data['anime']}"
                await update.message.reply_text(f"🎌 {quote}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch an anime quote right now.")


async def get_pokemon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get information about a Pokemon"""
    if not context.args:
        await update.message.reply_text("Please specify a Pokemon name or ID!\nExample: /pokemon pikachu")
        return

    pokemon = context.args[0].lower()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEMON_API}{pokemon}") as response:
            if response.status == 200:
                data = await response.json()
                message = (
                    f"🎮 Pokemon: {data['name'].title()}\n"
                    f"📏 Height: {data['height']/10}m\n"
                    f"⚖️ Weight: {data['weight']/10}kg\n"
                    f"📋 Types: {', '.join(t['type']['name'] for t in data['types'])}\n"
                    f"💪 Base Experience: {data['base_experience']}"
                )
                if data['sprites']['front_default']:
                    await update.message.reply_photo(data['sprites']['front_default'])
                await update.message.reply_text(message)
            else:
                await update.message.reply_text("Pokemon not found! Check the spelling or try a different one.")



async def get_random_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random joke"""
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
    """Get a random quote"""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['QUOTE_API']) as response:
            if response.status == 200:
                data = await response.json()
                quote = f"💭 \"{data['content']}\"\n\n— {data['author']}"
                await update.message.reply_text(quote)
            else:
                await update.message.reply_text("Sorry, couldn't fetch a quote right now.")



async def get_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a trivia question"""
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
    """Check trivia answer"""
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
    """Get a random math fact"""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['NUMBER_API']) as response:
            if response.status == 200:
                fact = await response.text()
                await update.message.reply_text(f"🔢 {fact}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch a number fact right now.")


async def mistral_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /chat command to interact with Mistral LLM"""
    if not context.args:
        await update.message.reply_text("Please provide a prompt. Usage: /chat Your question or prompt here")
        return

    prompt = ' '.join(context.args)

    try:
        if not MISTRAL_API_KEY:
            await update.message.reply_text("Mistral API key not configured!")
            return
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        }
        
        payload = {
            "model": "mistral-small",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    generated_text = result['choices'][0]['message']['content']
                    await update.message.reply_text(generated_text)
                else:
                    error_text = await response.text()
                    await update.message.reply_text(f"Sorry, there was an API error: {error_text}")
    
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")



async def nasa_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get NASA's Astronomy Picture of the Day"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    message = f"🚀 **NASA Picture of the Day**\n\n"
                    message += f"📅 **Date:** {data.get('date', 'Unknown')}\n"
                    message += f"🌟 **Title:** {data.get('title', 'Unknown')}\n\n"
                    message += f"📝 **Description:**\n{data.get('explanation', 'No description available')[:500]}..."
                    
                    if data.get('media_type') == 'image':
                        await update.message.reply_photo(
                            photo=data.get('url'),
                            caption=message,
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text(
                            message + f"\n\n🔗 **Link:** {data.get('url')}",
                            parse_mode='Markdown'
                        )
                else:
                    await update.message.reply_text("❌ Could not fetch NASA picture right now!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching NASA data!")


async def crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get cryptocurrency prices"""
    if not context.args:
        await update.message.reply_text("💰 Usage: /crypto_price bitcoin\nSupported: bitcoin, ethereum, dogecoin, litecoin, cardano")
        return
    
    crypto = context.args[0].lower()
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd,eur"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if crypto in data:
                        price_usd = data[crypto].get('usd', 'N/A')
                        price_eur = data[crypto].get('eur', 'N/A')
                        
                        await update.message.reply_text(
                            f"💰 **{crypto.title()} Price:**\n\n"
                            f"💵 USD: ${price_usd:,}\n"
                            f"💶 EUR: €{price_eur:,}"
                        )
                    else:
                        await update.message.reply_text("❌ Cryptocurrency not found!")
                else:
                    await update.message.reply_text("❌ Could not fetch crypto prices!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching crypto data!")


async def chuck_norris(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get random Chuck Norris joke"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.chucknorris.io/jokes/random"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    joke = data.get('value', 'No joke available')
                    await update.message.reply_text(f"💪 **Chuck Norris Fact:**\n\n{joke}")
                else:
                    await update.message.reply_text("❌ Could not fetch Chuck Norris joke!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching joke!")




async def dog_breed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get random dog breed information with image"""
    try:
        async with aiohttp.ClientSession() as session:
            # Get random breed
            url = "https://dog.ceo/api/breeds/list/all"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    breeds = list(data.get('message', {}).keys())
                    
                    if breeds:
                        breed = random.choice(breeds)
                        
                        # Get breed image
                        img_url = f"https://dog.ceo/api/breed/{breed}/images/random"
                        async with session.get(img_url) as img_response:
                            if img_response.status == 200:
                                img_data = await img_response.json()
                                image_url = img_data.get('message')
                                
                                await update.message.reply_photo(
                                    photo=image_url,
                                    caption=f"🐕 **Random Dog Breed: {breed.title()}**\n\nIsn't this {breed} adorable? 🥰"
                                )
                            else:
                                await update.message.reply_text(f"🐕 **Random Dog Breed: {breed.title()}**")
                    else:
                        await update.message.reply_text("❌ Could not fetch dog breeds!")
                else:
                    await update.message.reply_text("❌ Could not fetch dog data!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching dog breed!")


async def get_random_snake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random snake image"""
    try:
        async with aiohttp.ClientSession() as session:
            # Using a snake image API
            if not UNSPLASH_ACCESS_KEY:
                await update.message.reply_text("Unsplash access key not configured!")
                return
            url = f"https://api.unsplash.com/photos/random?query=snake&client_id={UNSPLASH_ACCESS_KEY}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get('urls', {}).get('regular')
                    if image_url:
                        await update.message.reply_photo(image_url)
                        await update.message.reply_text("🐍 Hiss! Here's your random snake!")
                    else:
                        await update.message.reply_text("Sorry, couldn't fetch a snake image right now.")
                else:
                    await update.message.reply_text("Sorry, couldn't fetch a snake image right now.")
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a snake image right now.")


async def get_random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random word with definition"""
    try:
        async with aiohttp.ClientSession() as session:
            # Using WordsAPI for random word
            url = "https://wordsapiv1.p.rapidapi.com/words/?random=true"
            headers = {
                "X-RapidAPI-Key": "DEMO_KEY",
                "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
            }
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    word = data.get('word', 'Unknown')
                    definitions = data.get('results', [])
                    
                    if definitions:
                        definition = definitions[0].get('definition', 'No definition available')
                        message = f"📚 **Random Word:** {word.title()}\n\n"
                        message += f"**Definition:** {definition}"
                        await update.message.reply_text(message, parse_mode='Markdown')
                    else:
                        await update.message.reply_text(f"📚 **Random Word:** {word.title()}\n\nNo definition available.")
                else:
                    await update.message.reply_text("Sorry, couldn't fetch a random word right now.")
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a random word right now.")


async def get_drum_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random drum photo"""
    try:
        async with aiohttp.ClientSession() as session:
            # Using Unsplash API for drum photos
            if not UNSPLASH_ACCESS_KEY:
                await update.message.reply_text("Unsplash access key not configured!")
                return
            url = f"https://api.unsplash.com/photos/random?query=drum&client_id={UNSPLASH_ACCESS_KEY}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get('urls', {}).get('regular')
                    if image_url:
                        await update.message.reply_photo(image_url)
                        await update.message.reply_text("🥁 Here's your drum photo!")
                    else:
                        await update.message.reply_text("Sorry, couldn't fetch a drum photo right now.")
                else:
                    await update.message.reply_text("Sorry, couldn't fetch a drum photo right now.")
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a drum photo right now.")
