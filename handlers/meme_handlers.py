"""
Meme and image manipulation command handlers
"""
import random
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
from telegram import Update
from telegram.ext import ContextTypes
from config import IMGFLIP_USERNAME, IMGFLIP_PASSWORD, MEME_TEMPLATES, OVERLAYS


def create_meme(template_id, top_text, bottom_text):
    """Create a meme using Imgflip API"""
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


async def makememe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a meme with specified template and text"""
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


async def templates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available meme templates"""
    templates_list = "\n".join([f"'{name}': '{template_id}'" for name, template_id in MEME_TEMPLATES.items()])
    response_message = f"Available meme templates:\n\n{templates_list}"
    await update.message.reply_text(response_message)


async def create_meme_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a meme with top and bottom text from an image URL"""
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
        
        # Try to use a default font, or create a simple text overlay
        try:
            # You might need to add a font file to your project
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Calculate text positions
        img_width, img_height = img.size
        top_pos = (img_width//2, 30)
        bottom_pos = (img_width//2, img_height - 30)
        
        # Draw text with outline for better visibility
        # Top text
        draw.text(top_pos, top_text, font=font, fill='white', anchor="mt")
        # Bottom text
        draw.text(bottom_pos, bottom_text, font=font, fill='white', anchor="mb")
        
        # Save and send
        bio = BytesIO()
        bio.name = 'meme.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await update.message.reply_photo(photo=bio)
    except Exception as e:
        await update.message.reply_text(f"Sorry, couldn't create the meme: {str(e)}")


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
            img = img.convert('RGB')
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
        elif filter_name == "blur":
            # Simple blur effect
            img = img.filter(ImageFilter.BLUR)
        else:
            await update.message.reply_text("Unknown filter. Available: grayscale, sepia, blur, invert")
            return
        
        # Save and send
        bio = BytesIO()
        bio.name = 'filtered_image.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        
        await update.message.reply_photo(photo=bio)
    except Exception as e:
        await update.message.reply_text(f"Sorry, couldn't apply the filter: {str(e)}")


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
    except ImportError:
        await update.message.reply_text("gTTS library not installed. Install with: pip install gTTS")
    except Exception as e:
        await update.message.reply_text(f"Sorry, couldn't convert text to speech: {str(e)}")


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
