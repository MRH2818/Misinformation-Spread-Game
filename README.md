# 📰 Misinformation Spread Game

A single-player educational game that simulates how information can change and evolve as it's passed from person to person, potentially leading to misinformation. Players are given stories with political significance and must retell them in their own words.

## 🎮 Game Concept

Instead of the traditional "broken telephone" game where people pass along short phrases, this game focuses on **stories with political significance**. Players:

1. Read an original story and its political implications
2. Retell the story in their own words
3. Explain the political significance from their perspective
4. Track how information changes across rounds

## 🚀 Features

- **Modern UI**: Beautiful gradient design with responsive layout
- **Story Generation**: Integration ready for ChatGPT API to generate diverse stories
- **Game History**: Track all rounds and see how stories evolve
- **Political Focus**: Emphasizes the political implications of news stories
- **Single Player**: Perfect for educational settings or individual learning

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI Integration**: OpenAI ChatGPT API (ready for implementation)
- **Styling**: Custom CSS with modern gradients and animations

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd misinformation-spread-game
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration** (required for ChatGPT integration):
   ```bash
   # Edit the config.json file with your API key
   # Replace "your-api-key-here" with your actual OpenAI API key
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

## 🎯 How to Play

1. **Start the Game**: Click "Start New Game" to begin
2. **Read the Story**: Carefully read the provided story and its political significance
3. **Retell the Story**: Write the story in your own words
4. **Explain Significance**: Describe the political implications from your perspective
5. **Submit**: Click "Submit Story" to save your version
6. **Continue**: Get a new story for the next round
7. **Review History**: Click "View History" to see how your stories evolved

## 🔧 ChatGPT Integration

The game now uses ChatGPT for dynamic story generation. The integration is already implemented:

1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/)
2. **Add your API key** to the `config.json` file:
   ```json
   {
       "openai_api_key": "your-api-key-here",
       "max_tokens": 300,
       "temperature": 0.7,
       "model": "gpt-3.5-turbo"
   }
   ```
3. **The game will automatically generate unique stories** for each round

The ChatGPT integration is configured to generate:
- Detailed stories with specific names, relationships, and financial details
- Complex political scenarios with multiple layers of intrigue
- Realistic but dramatic content suitable for educational purposes
- Stories that allow for personal interpretation rather than predetermined political analysis

## 📁 Project Structure

```
misinformation-spread-game/
├── app.py                 # Main Flask application
├── config.json            # Configuration file with API keys
├── chatgpt_integration.py # ChatGPT API integration
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Main game interface
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile devices
- **Modern Gradients**: Beautiful purple-blue gradient background
- **Smooth Animations**: Hover effects and transitions
- **Clear Typography**: Easy-to-read fonts and spacing
- **Intuitive Navigation**: Simple, clear interface

## 🔮 Future Enhancements

- **Multiplayer Mode**: Allow multiple players to pass stories between each other
- **Story Categories**: Different types of political stories (environmental, economic, social)
- **Analytics**: Track how specific details change across rounds
- **Export Functionality**: Save game results for analysis
- **Custom Story Input**: Allow users to input their own stories

## 🎓 Educational Value

This game helps players understand:
- How information can change when retold
- The importance of accurate news reporting
- How political narratives can evolve
- Critical thinking about information sources
- Media literacy skills

## 🤝 Contributing

Feel free to contribute to this project! Some areas for improvement:
- Add more story templates
- Implement multiplayer functionality
- Enhance the UI/UX
- Add more educational features

## 📄 License

This project is open source and available under the MIT License.

---

**Note**: This is a wireframe/prototype. For production use, consider adding proper error handling, input validation, and security measures. 