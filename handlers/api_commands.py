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
    JIKAN_API_BASE, WAIFU_API, APIS, SNAKE_IMAGES, SNAKE_MESSAGES,
    DRUM_IMAGES, MISTRAL_API_KEY, GIPHY_API_KEY
)
import requests


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


async def get_random_snake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random snake image"""
    try:
        snake_url = random.choice(SNAKE_IMAGES)
        await update.message.reply_photo(snake_url)
        
        snake_message = random.choice(SNAKE_MESSAGES)
        await update.message.reply_text(snake_message)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a snake image right now. Try again later! 🐍")


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


async def get_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random activity suggestion"""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['ACTIVITY_API']) as response:
            if response.status == 200:
                data = await response.json()
                activity = f"🎯 Activity Suggestion:\n\n{data['activity']}\n\nType: {data['type'].capitalize()}\nParticipants: {data['participants']}"
                await update.message.reply_text(activity)
            else:
                await update.message.reply_text("Sorry, couldn't fetch an activity right now.")


async def get_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get random advice"""
    async with aiohttp.ClientSession() as session:
        async with session.get(APIS['ADVICE_API']) as response:
            if response.status == 200:
                data = await response.json()
                await update.message.reply_text(f"🤔 Advice:\n\n{data['slip']['advice']}")
            else:
                await update.message.reply_text("Sorry, couldn't fetch advice right now.")


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


async def analyze_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze a name for gender, age, and nationality"""
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
    """Get information about a random user"""
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
    """Get current location of the International Space Station"""
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
    """Get a random recipe"""
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
    """Handle the /chat command to interact with Mistral LLM"""
    if not context.args:
        await update.message.reply_text("Please provide a prompt. Usage: /chat Your question or prompt here")
        return

    prompt = ' '.join(context.args)

    try:
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
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            await update.message.reply_text(generated_text)
        else:
            await update.message.reply_text(f"Sorry, there was an API error: {response.text}")
    
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


async def get_drum_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a drum photo"""
    try:
        # Send a "typing" action to show bot is working
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="upload_photo"
        )
        
        # Use fallback drum images
        selected_image = random.choice(DRUM_IMAGES)
        
        # Send the photo
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=selected_image,
            caption="🥁 Here's a drum photo for you!",
            parse_mode='HTML'
        )
        
    except Exception as e:
        await update.message.reply_text(
            "❌ An unexpected error occurred. Please try again."
        )


async def random_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetch a random GIF based on search term"""
    if GIPHY_API_KEY == "YOUR_GIPHY_API_KEY":
        await update.message.reply_text("GIPHY API key not configured!")
        return
    
    search_term = " ".join(context.args) if context.args else "random"
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_API_KEY}&tag={search_term}"
    
    try:
        response = requests.get(url)
        data = response.json()
        gif_url = data['data']['images']['original']['url']
        await update.message.reply_animation(gif_url)
    except Exception as e:
        await update.message.reply_text("Sorry, couldn't fetch a GIF right now!")


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


async def useless_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get a random useless fact"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://uselessfacts.jsph.pl/random.json?language=en"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    fact = data.get('text', 'No fact available')
                    await update.message.reply_text(f"🤓 **Random Useless Fact:**\n\n{fact}")
                else:
                    await update.message.reply_text("❌ Could not fetch a fact right now!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching fact!")


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


async def urban_dict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Look up word in Urban Dictionary"""
    if not context.args:
        await update.message.reply_text("📚 Usage: /urban_dict word")
        return
    
    word = " ".join(context.args)
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.urbandictionary.com/v0/define?term={quote(word)}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    definitions = data.get('list', [])
                    
                    if definitions:
                        definition = definitions[0]
                        text = f"📚 **Urban Dictionary - {word.title()}**\n\n"
                        text += f"**Definition:**\n{definition.get('definition', 'No definition')[:400]}...\n\n"
                        text += f"**Example:**\n{definition.get('example', 'No example')[:200]}...\n\n"
                        text += f"👍 {definition.get('thumbs_up', 0)} | 👎 {definition.get('thumbs_down', 0)}"
                        
                        await update.message.reply_text(text, parse_mode='Markdown')
                    else:
                        await update.message.reply_text(f"❌ No definition found for '{word}'")
                else:
                    await update.message.reply_text("❌ Could not access Urban Dictionary!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching definition!")


async def color_palette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate random color palette"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "http://colormind.io/api/"
            data = {"model": "default"}
            
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    colors = result.get('result', [])
                    
                    if colors:
                        message = "🎨 **Random Color Palette:**\n\n"
                        for i, color in enumerate(colors, 1):
                            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                            rgb = f"RGB({color[0]}, {color[1]}, {color[2]})"
                            message += f"**Color {i}:** {hex_color}\n{rgb}\n\n"
                        
                        await update.message.reply_text(message, parse_mode='Markdown')
                    else:
                        await update.message.reply_text("❌ Could not generate color palette!")
                else:
                    await update.message.reply_text("❌ Color service unavailable!")
    except Exception as e:
        await update.message.reply_text("❌ Error generating colors!")


async def bored_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get activity suggestion when bored"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://www.boredapi.com/api/activity"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    activity = data.get('activity', 'No activity found')
                    activity_type = data.get('type', 'Unknown').title()
                    participants = data.get('participants', 1)
                    price = data.get('price', 0)
                    
                    price_emoji = "💰" * int(price * 5) if price > 0 else "🆓"
                    
                    message = f"🎯 **Activity Suggestion:**\n\n"
                    message += f"📝 **Activity:** {activity}\n"
                    message += f"🏷️ **Type:** {activity_type}\n"
                    message += f"👥 **Participants:** {participants}\n"
                    message += f"💸 **Cost:** {price_emoji}"
                    
                    await update.message.reply_text(message, parse_mode='Markdown')
                else:
                    await update.message.reply_text("❌ Could not fetch activity suggestion!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching activity!")


async def programming_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get random programming quote"""
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://programming-quotes-api.herokuapp.com/Quotes/random"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    quote = data.get('en', 'No quote available')
                    author = data.get('author', 'Unknown')
                    
                    await update.message.reply_text(f"{quote}")
                else:
                    await update.message.reply_text("❌ Could not fetch programming quote!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching quote!")


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
