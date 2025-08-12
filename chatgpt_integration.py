"""
ChatGPT Integration for Misinformation Spread Game

This file handles the integration with OpenAI's ChatGPT API to generate
dynamic stories for the game. The configuration is loaded from config.json.
"""

import openai
import json
import os

# Load configuration from config file
def load_config():
    try:
        with open('config.json', 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError("config.json file not found. Please create a config.json file with your settings.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in config.json file. Please check the file format.")

# Load configuration
config = load_config()

# Set up OpenAI API
api_key = config.get('openai_api_key')
if not api_key:
    raise ValueError("openai_api_key not found in config.json. Please check your configuration file.")
openai.api_key = api_key

def generate_story_with_chatgpt():
    """
    Generate a story with political significance using ChatGPT.
    
    Returns:
        dict: A dictionary containing 'title', 'content', and 'political_significance'
    """
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model=config.get('model', 'gpt-3.5-turbo'),
            messages=[
                {
                    "role": "system", 
                    "content": """You are an educational game content generator specializing in politically charged news stories.
                    Create detailed, specific stories with complex political implications that include:
                    - Specific names, relationships, and connections between people
                    - Financial details, donations, and quid-pro-quo arrangements
                    - Multiple layers of political intrigue and corruption
                    - Specific consequences and investigations
                    - Realistic but dramatic political scenarios
                    
                    Each story should be engaging and show how information can be interpreted differently."""
                },
                {
                    "role": "user", 
                    "content": """Generate a detailed news story with juicy political/corporate details including:
                    1. A catchy title
                    2. A story (3-4 sentences) with specific names, relationships, financial details, and political connections
                    
                    Format the response as a JSON object with keys: title, content

                    No need to make it realistic. Do not discuss possible interpretations, just give the facts. The story should be rich with details but let the reader interpret its meaning themselves."""
                }
            ],
            max_tokens=config.get('max_tokens', 300),
            temperature=config.get('temperature', 0.7)
        )
        
        # Parse the response
        content = response.choices[0].message.content
        
        # Try to parse as JSON, fallback to text parsing if needed
        try:
            story_data = json.loads(content)
            return story_data
        except json.JSONDecodeError:
            # Fallback: parse the text manually
            return parse_story_text(content)
            
    except Exception as e:
        print(f"Error generating story: {e}")
        # Return a fallback story
        return {
            "title": "Sample Story",
            "content": "A local community center faced budget cuts, affecting after-school programs for children. The mayor's office claimed the cuts were necessary due to declining tax revenue, but critics pointed out that the mayor had recently approved a $2 million renovation of his own office suite. The community center director, who had been vocal about the cuts, was fired shortly after speaking to the local newspaper about the impact on children."
        }

def parse_story_text(text):
    """
    Parse story text when JSON parsing fails.
    
    Args:
        text (str): The raw text response from ChatGPT
        
    Returns:
        dict: Parsed story data
    """
    # Simple parsing logic - you might want to improve this
    lines = text.split('\n')
    title = ""
    content = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith('"title"') or line.startswith('title'):
            title = line.split(':')[1].strip().strip('",')
        elif line.startswith('"content"') or line.startswith('content'):
            content = line.split(':')[1].strip().strip('",')
    
    return {
        "title": title or "Generated Story",
        "content": content or "A story was generated but could not be parsed properly."
    }

def generate_multiple_stories(count=5):
    """
    Generate multiple stories for variety.
    
    Args:
        count (int): Number of stories to generate
        
    Returns:
        list: List of story dictionaries
    """
    stories = []
    for i in range(count):
        story = generate_story_with_chatgpt()
        stories.append(story)
        print(f"Generated story {i+1}: {story['title']}")
    
    return stories

# Example usage
if __name__ == "__main__":
    # Test the integration
    print("Testing ChatGPT integration...")
    story = generate_story_with_chatgpt()
    print(json.dumps(story, indent=2))
    
    # Generate multiple stories
    print("\nGenerating multiple stories...")
    stories = generate_multiple_stories(3)
    for i, story in enumerate(stories):
        print(f"\nStory {i+1}:")
        print(f"Title: {story['title']}")
        print(f"Content: {story['content']}") 