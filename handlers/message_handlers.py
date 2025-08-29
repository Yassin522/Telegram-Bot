"""
Message handlers for the Telegram Bot
"""
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from data.static_data import KEYWORD_RESPONSES
from utils.text_utils import filter_inappropriate_words
from utils.data_manager import DataManager
from config import AUTHORIZED_USERS

logger = logging.getLogger(__name__)
data_manager = DataManager()


async def respond_to_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Message handler for keyword responses"""
    message_text = update.message.text.lower()
    for keyword, response in KEYWORD_RESPONSES.items():
        if message_text.strip() == keyword:
            await update.message.reply_text(response)
            return  # Stop checking after the first match


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Message handler to check for insults with improved detection"""
    if not update.message or not update.message.text:
        return
    
    message_text = update.message.text
    insults = data_manager.load_insults()
    
    if not insults:
        return  # No insults to check against
    
    # Use word-by-word approach for better accuracy
    words = message_text.split()
    detected_words = []
    final_sanitized_words = []
    
    for word in words:
        word_detected = False
        normalized_word = word.lower()
        
        for insult in insults:
            if insult in normalized_word:
                detected_words.append(word)
                final_sanitized_words.append('*' * len(word))
                word_detected = True
                break
        
        if not word_detected:
            final_sanitized_words.append(word)
    
    # If insults were detected
    if detected_words:
        sanitized_message = ' '.join(final_sanitized_words)
        
        # Update counter
        username = update.effective_user.username or "unknown"
        current_count = data_manager.increment_counter(username)
        
        # Delete the original message
        try:
            await update.message.delete()
        except BadRequest:
            logger.warning(f"Could not delete message: {update.message.message_id}")
        
        # Send warning message with current count
        user = update.effective_user.mention_html()
        warning = f"⚠️ {user}, المُسْلِمُ مَنْ سَلِمَ المُسْلِمُونَ مِنْ لِسَانِهِ وَيَدِهِ رواه البخاري"
        warning += f"\nلقد بلغت شتائمك الـ ({current_count})! شتائم"
        warning += "\nهل ترضى لحسناتك أن تنقص لنطق ببعض الكلام الغير مفيد؟"
        warning += "\nاستغفر الله العظيم ، استغفر الله العظيم، استغفر الله العظيم"
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=warning,
            parse_mode='HTML'
        )
        
        # Send the sanitized message (without bad words)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=sanitized_message,
            parse_mode='HTML'
        )


async def filter_inappropriate_words_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Filter messages containing variations of banned words like 'قص'"""
    message_text = update.message.text
    
    if message_text and filter_inappropriate_words(message_text):
        try:
            # First send the warning message BEFORE deleting the original
            warning_msg = await update.message.reply_text(
                "⚠️ *WARNING:* انت غالبا مارديني لهيك حاج ولدنة احسن ماتشوف شي مابيعجبك",
                parse_mode='Markdown'
            )
            
            # Now delete the original message
            await update.message.delete()
            
            # Delete the warning message after 4 seconds
            await asyncio.sleep(4)
            await warning_msg.delete()
            
            # Log the incident
            user = update.effective_user
            chat = update.effective_chat
            logger.info(
                f"Removed inappropriate message from user {user.id} ({user.first_name}) in chat {chat.id}"
            )
            
            return True  # Indicate we've handled this message
            
        except BadRequest as e:
            logger.error(f"Failed to delete message: {e}")
        except Exception as e:
            logger.error(f"Error in filter_inappropriate_words: {e}")
    
    return None  # Allow other handlers to process this message


async def add_keyword_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to add a new keyword and response to the KEYWORD_RESPONSES dictionary"""
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


async def add_insult(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command handler to add new insult words to the dataset"""
    user = update.effective_user.username
    
    if user not in AUTHORIZED_USERS:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("Please provide a word to add to the insults list.")
        return
    
    word = ' '.join(context.args).lower()
    
    if data_manager.add_insult(word):
        await update.message.reply_text(f"Added '{word}' to the insults list.")
    else:
        await update.message.reply_text("This word is already in the list.")


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command handler to show the insult counter leaderboard"""
    leaderboard = data_manager.get_leaderboard()
    
    if not leaderboard:
        await update.message.reply_text("No insults recorded yet.")
        return
    
    # Create leaderboard message
    leaderboard_text = "🏆 Insult Leaderboard:\n\n"
    for i, (username, count) in enumerate(leaderboard.items(), 1):
        leaderboard_text += f"{i}. {username}: {count} insults\n"
    
    await update.message.reply_text(leaderboard_text)


async def recursive_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Special handling for /recursive command to trigger /dog without stopping further processing"""
    # Send the /dog command
    await update.message.reply_text("/dog")
    
    # Explicitly return None to allow normal command processing to continue
    return None
