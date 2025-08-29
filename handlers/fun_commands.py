"""
Fun and entertainment command handlers
"""
import random
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from data.static_data import (
    JOKES, DAD_JOKES, PICKUP_LINES, ROASTS, COMPLIMENTS,
    WOULD_YOU_RATHER, TRUTH_QUESTIONS, DARE_CHALLENGES,
    FORTUNES, TONGUE_TWISTERS, INSPIRATIONAL_QUOTES,
    SYRIA_FACTS, SCRAMBLE_WORDS, HANGMAN_WORDS
)


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random Mardini joke"""
    await update.message.reply_text(random.choice(JOKES))


async def dadjoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dad joke"""
    joke = random.choice(DAD_JOKES)
    await update.message.reply_text(f"👨 Dad says: {joke}")


async def pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random pickup line"""
    line = random.choice(PICKUP_LINES)
    await update.message.reply_text(f"😉 {line}")


async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random roast"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to someone's message to roast them!")
        return
    
    roast_text = random.choice(ROASTS)
    username = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"🔥 Hey {username}, {roast_text}")


async def compliment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random compliment"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to someone's message to compliment them!")
        return
    
    compliment_text = random.choice(COMPLIMENTS)
    username = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"💝 Hey {username}, {compliment_text}")


async def would_you_rather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a would you rather poll"""
    question, option1, option2 = random.choice(WOULD_YOU_RATHER)
    await update.message.reply_poll(
        question,
        [option1, option2],
        is_anonymous=False,
        type='regular'
    )


async def truth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random truth question"""
    question = random.choice(TRUTH_QUESTIONS)
    await update.message.reply_text(f"🤔 Truth: {question}")


async def dare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random dare challenge"""
    challenge = random.choice(DARE_CHALLENGES)
    await update.message.reply_text(f"😈 Dare: {challenge}")


async def fortune(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fortune prediction"""
    fortune_text = random.choice(FORTUNES)
    await update.message.reply_text(f"🔮 Your fortune: {fortune_text}")


async def twister(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random tongue twister"""
    twister_text = random.choice(TONGUE_TWISTERS)
    await update.message.reply_text(f"👅 Try saying this fast:\n{twister_text}")


async def randomchoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Make a random choice between given options"""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /choose option1 option2 [option3 ...]")
        return
    
    choice = random.choice(context.args)
    await update.message.reply_text(f"🎲 I choose: {choice}")


async def party(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a virtual party"""
    party_message = "🎉 PARTY TIME! 🎉\n\n"
    party_message += "💃 " * random.randint(3, 7) + "\n"
    party_message += "🕺 " * random.randint(3, 7) + "\n"
    party_message += "🎵 " * random.randint(3, 7)
    await update.message.reply_text(party_message)


async def inspire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random inspirational quote"""
    quote = random.choice(INSPIRATIONAL_QUOTES)
    await update.message.reply_text(f"✨ {quote}")


async def syria_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random fact about Syria"""
    fact = random.choice(SYRIA_FACTS)
    await update.message.reply_text(f"🇸🇾 Did you know? {fact}")


async def flipcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin"""
    result = random.choice(['Heads', 'Tails'])
    await update.message.reply_text(f"🪙 The coin shows: {result}")


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll a dice"""
    await update.message.reply_dice()


async def word_scramble(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a word scramble game"""
    word, hint = random.choice(list(SCRAMBLE_WORDS.items()))
    scrambled = ''.join(random.sample(word, len(word)))
    
    context.user_data['current_word'] = word
    await update.message.reply_text(
        f"🎮 Word Scramble!\n\nUnscramble this word: {scrambled}\n\nHint: {hint}\n\n"
        "Type /guess <word> to make a guess!"
    )


async def check_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check word scramble guess"""
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


async def number_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a number guessing game"""
    number = random.randint(1, 100)
    context.user_data['number'] = number
    context.user_data['attempts'] = 0
    
    await update.message.reply_text(
        "🎲 Number Guessing Game!\n\n"
        "I'm thinking of a number between 1 and 100.\n"
        "Use /guess_number <number> to make a guess!"
    )


async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check number guessing game guess"""
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
    """Start a hangman game"""
    word = random.choice(HANGMAN_WORDS)
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
    """Guess a letter in hangman game"""
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
