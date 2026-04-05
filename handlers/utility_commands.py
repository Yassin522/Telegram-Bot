"""
Utility command handlers
"""
import aiohttp
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes
from config import LEBANON_TZ, WEATHER_EMOJIS, OPENWEATHER_API_KEY
import pytz


async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send current time in Lebanon"""
    lebanon_time = datetime.now(LEBANON_TZ).strftime("%I:%M %p")
    await update.message.reply_text(f"🕒 Current time in Lebanon: {lebanon_time}")


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get weather information for a specified city"""
    if len(context.args) < 1:
        await update.message.reply_text("Please specify a city. Usage: /weather <city>")
        return

    city = ' '.join(context.args)
    api_key = OPENWEATHER_API_KEY if OPENWEATHER_API_KEY != "YOUR_OPENWEATHER_API_KEY" else "demo"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

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
    """Create a poll"""
    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /poll 'question' 'option1' 'option2' ...\n"
            "Example: /poll 'Favorite food?' 'Pizza' 'Burger' 'Shawarma'"
        )
        return

    question = context.args[0]
    options = context.args[1:]
    await update.message.reply_poll(question, options)


async def _send_reminder(context) -> None:
    """Job callback: sends the deferred reminder message."""
    data = context.job.data
    await context.bot.send_message(
        chat_id=data['chat_id'],
        text=f"⏰ Reminder for {data['mention']}:\n{data['text']}",
        parse_mode='HTML'
    )


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set a reminder using job_queue."""
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

        context.job_queue.run_once(
            _send_reminder,
            when=timedelta(minutes=minutes),
            data={
                'chat_id': update.effective_chat.id,
                'mention': update.message.from_user.mention_html(),
                'text': message,
            }
        )
        await update.message.reply_text(f"I'll remind you about '{message}' in {minutes} minute(s)!")
    except ValueError:
        await update.message.reply_text("Please provide a valid number of minutes.")


async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple calculator"""
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


async def qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate QR code for text"""
    if not context.args:
        await update.message.reply_text("📱 Usage: /qr_code Your text here")
        return
    
    from urllib.parse import quote
    text = " ".join(context.args)
    encoded_text = quote(text)
    
    # Using QR Server API (free)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}"
    
    try:
        await update.message.reply_photo(
            photo=qr_url,
            caption=f"📱 QR Code for: {text}"
        )
    except Exception as e:
        await update.message.reply_text("❌ Error generating QR code!")


async def ip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get information about an IP address"""
    if not context.args:
        await update.message.reply_text("🌐 Usage: /ip_info 8.8.8.8")
        return
    
    ip = context.args[0]
    try:
        async with aiohttp.ClientSession() as session:
            url = f"http://ip-api.com/json/{ip}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('status') == 'success':
                        message = f"🌐 **IP Information: {ip}**\n\n"
                        message += f"🏳️ **Country:** {data.get('country', 'Unknown')}\n"
                        message += f"🏙️ **City:** {data.get('city', 'Unknown')}\n"
                        message += f"📍 **Region:** {data.get('regionName', 'Unknown')}\n"
                        message += f"🏢 **ISP:** {data.get('isp', 'Unknown')}\n"
                        message += f"⏰ **Timezone:** {data.get('timezone', 'Unknown')}\n"
                        message += f"📮 **Zip:** {data.get('zip', 'Unknown')}"
                        
                        await update.message.reply_text(message, parse_mode='Markdown')
                    else:
                        await update.message.reply_text("❌ Invalid IP address or lookup failed!")
                else:
                    await update.message.reply_text("❌ Could not lookup IP!")
    except Exception as e:
        await update.message.reply_text("❌ Error looking up IP!")


async def github_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get GitHub user information"""
    if not context.args:
        await update.message.reply_text("👨‍💻 Usage: /github_user username")
        return
    
    username = context.args[0]
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.github.com/users/{username}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    message = f"👨‍💻 **GitHub Profile: {username}**\n\n"
                    message += f"👤 **Name:** {data.get('name', 'N/A')}\n"
                    message += f"🏢 **Company:** {data.get('company', 'N/A')}\n"
                    message += f"📍 **Location:** {data.get('location', 'N/A')}\n"
                    message += f"📊 **Public Repos:** {data.get('public_repos', 0)}\n"
                    message += f"👥 **Followers:** {data.get('followers', 0)}\n"
                    message += f"👤 **Following:** {data.get('following', 0)}\n"
                    message += f"📅 **Joined:** {data.get('created_at', 'Unknown')[:10]}\n"
                    
                    if data.get('bio'):
                        message += f"📝 **Bio:** {data.get('bio')[:100]}...\n"
                    
                    message += f"\n🔗 **Profile:** {data.get('html_url')}"
                    
                    await update.message.reply_text(message, parse_mode='Markdown')
                elif response.status == 404:
                    await update.message.reply_text(f"❌ GitHub user '{username}' not found!")
                else:
                    await update.message.reply_text("❌ Could not fetch GitHub data!")
    except Exception as e:
        await update.message.reply_text("❌ Error fetching GitHub user!")
