# 📰 Misinformation Spread Game

This game is designed to test the continued influence effect: even after misinformation is corrected, the original message can still shape beliefs and memory. By repeatedly introducing corrections that subvert the gist of a story, the game demonstrates how difficult it is to fully erase the impact of initial information.

- Single-player browser game about how news stories change as they are retold and corrected
- Each round, you read a political story and retell it from memory
- After each retelling, a new "correction" is introduced that subverts the previous message
- The process repeats, showing how the story's meaning can shift with each correction
- Highlights how original misinformation can continue to influence thinking, even after many corrections

**To run the game, create a `config.json` file in the project folder with your OpenAI API key:**

```json
{
    "openai_api_key": "your-api-key-here",
    "max_tokens": 300,
    "temperature": 0.7,
    "model": "gpt-3.5-turbo"
}
```
