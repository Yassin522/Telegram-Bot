# Telegram Bot - Multi-Functional Bot

A comprehensive Telegram bot with multiple features including fun commands, games, API integrations, meme creation, and more.

## 🚀 Features

### Fun & Entertainment
- **Jokes & Humor**: Random jokes, dad jokes, pickup lines, roasts, and compliments
- **Games**: Word scramble, hangman, number guessing, truth or dare
- **Interactive**: Would you rather polls, party mode, fortune telling

### Utility Commands
- **Time & Weather**: Current time in Lebanon, weather information for any city
- **Calculations**: Simple calculator, QR code generator
- **Information**: IP lookup, GitHub user info, IP geolocation

### API Integrations
- **Animals**: Random dog, cat, fox, and snake images
- **Anime**: Anime quotes, Pokemon information, waifu images
- **Entertainment**: Chuck Norris facts, NASA picture of the day, useless facts
- **Finance**: Cryptocurrency prices
- **AI Chat**: Integration with Mistral AI for conversations

### Image & Media
- **Meme Creation**: Create memes with popular templates
- **Image Filters**: Apply grayscale, sepia, blur, and invert effects
- **Special Effects**: Transform photos with Mardini-specific effects
- **Text-to-Speech**: Convert text to voice messages

### Content Moderation
- **Keyword Responses**: Automatic responses to specific keywords
- **Content Filtering**: Filter inappropriate content with warnings
- **Insult Detection**: Track and moderate inappropriate language

## 📁 Project Structure

```
Telegram-Bot/
├── main.py                 # Main entry point
├── config.py              # Configuration and environment variables
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (not in git)
├── data/
│   └── static_data.py    # Static data (jokes, quotes, etc.)
├── handlers/
│   ├── fun_commands.py   # Fun and entertainment commands
│   ├── utility_commands.py # Utility and helper commands
│   ├── api_commands.py   # API-based commands
│   ├── message_handlers.py # Message processing handlers
│   └── meme_handlers.py  # Meme and image manipulation
└── utils/
    ├── text_utils.py     # Text processing utilities
    └── data_manager.py   # Data file management
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Telegram-Bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Telegram Bot Configuration
   BOT_TOKEN=your_bot_token_here
   
   # API Keys
   MISTRAL_API_KEY=your_mistral_api_key
   IMGFLIP_USERNAME=your_imgflip_username
   IMGFLIP_PASSWORD=your_imgflip_password
   GIPHY_API_KEY=your_giphy_api_key
   
   # Optional API Keys
   UNSPLASH_ACCESS_KEY=your_unsplash_key
   PEXELS_API_KEY=your_pexels_key
   NEWS_API_KEY=your_news_api_key
   OPENWEATHER_API_KEY=your_openweather_key
   
   # Bot Configuration
   LEBANON_TZ=Asia/Beirut
   AUTHORIZED_USERS=username1,username2,username3
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Required API Keys
- **Telegram Bot Token**: Get from [@BotFather](https://t.me/botfather)
- **Mistral AI Key**: For AI chat functionality
- **Imgflip Credentials**: For meme creation

### Optional API Keys
- **OpenWeather**: For weather information
- **GIPHY**: For GIF search
- **Unsplash/Pexels**: For high-quality images

## 📚 Usage

### Basic Commands
- `/start` - Start the bot
- `/help` - Show all available commands
- `/joke` - Get a random joke
- `/time` - Get current time in Lebanon

### Game Commands
- `/scramble` - Start word scramble game
- `/hangman` - Start hangman game
- `/numbergame` - Start number guessing game

### Utility Commands
- `/weather <city>` - Get weather for a city
- `/calc <expression>` - Simple calculator
- `/qr_code <text>` - Generate QR code

### API Commands
- `/dog` - Random dog image
- `/cat` - Random cat image
- `/pokemon <name>` - Pokemon information
- `/chat <message>` - Chat with AI

### Meme Commands
- `/makememe <template> <top> <bottom>` - Create a meme
- `/templates` - Show available meme templates
- `/meme <url> <top> <bottom>` - Create custom meme

## 🚨 Content Moderation

The bot includes automatic content moderation features:
- **Keyword Filtering**: Automatic responses to specific keywords
- **Inappropriate Content**: Warning system for banned words
- **User Tracking**: Leaderboard for moderation statistics

## 🔒 Security

- Environment variables are stored in `.env` file (not committed to git)
- API keys are loaded securely from environment variables
- User authorization for sensitive commands
- Content filtering to prevent abuse

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🤝 Support

For support or questions:
- Create an issue in the repository
- Check the `/help` command in the bot
- Review the configuration and environment setup

## 🔄 Updates

The bot is actively maintained with regular updates:
- New commands and features
- Bug fixes and improvements
- API integrations and enhancements
- Performance optimizations