from flask import Flask, render_template, request, jsonify, session
import json
import random
from datetime import datetime
import os
from chatgpt_integration import generate_story_with_chatgpt

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

# Set OpenAI API key from config
import openai
api_key = config.get('openai_api_key')
if not api_key:
    raise ValueError("openai_api_key not found in config.json. Please check your configuration file.")
openai.api_key = api_key

app = Flask(__name__)
app.secret_key = 'misinformation-game-secret-key-2025'

@app.route('/')
def index():
    """Main game page"""
    return render_template('index.html')

@app.route('/start_game')
def start_game():
    """Start a new game session"""
    try:
        # Generate a new story using ChatGPT
        story = generate_story_with_chatgpt()
        session['current_story'] = story
        session['game_round'] = 1
        session['game_history'] = []
        
        return jsonify({
            'story': story,
            'round': session['game_round']
        })
    except Exception as e:
        print(f"Error generating story: {e}")
        # Fallback to a simple story if API fails
        fallback_story = {
            "title": "Corruption in Mayor's Office",
            "content": "A local community center faced budget cuts, affecting after-school programs for children. The mayor's office claimed the cuts were necessary due to declining tax revenue, but critics pointed out that the mayor had recently approved a $2 million renovation of his own office suite. The community center director, who had been vocal about the cuts, was fired shortly after speaking to the local newspaper about the impact on children."
        }
        session['current_story'] = fallback_story
        session['game_round'] = 1
        session['game_history'] = []
        
        return jsonify({
            'story': fallback_story,
            'round': session['game_round']
        })

@app.route('/submit_story', methods=['POST'])
def submit_story():
    """Submit player's version of the story"""
    data = request.get_json()
    player_story = data.get('story_content', '')
    player_significance = data.get('political_significance', '')
    
    # Store the player's version
    player_version = {
        'round': session['game_round'],
        'original_story': session['current_story'],
        'player_story': player_story,
        'player_significance': player_significance,
        'timestamp': datetime.now().isoformat()
    }
    
    session['game_history'].append(player_version)
    session['game_round'] += 1
    
    # Generate a "correction" for the next round
    correction = generate_correction(session['current_story'])
    session['correction'] = correction
    
    return jsonify({
        'success': True,
        'round': session['game_round'],
        'message': 'Story submitted successfully!',
        'correction': correction
    })

def generate_correction(story):
    """Generate a politically-charged correction to the story using AI, subverting the gist each time"""
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model=config.get('model', 'gpt-3.5-turbo'),
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI that generates corrections to news stories for an educational game about misinformation.\n\nYour task is to create a correction that:\n1. Is directly related to the specific story content\n2. Introduces politically-charged details that could change interpretation\n3. Focuses on details like race, education, criminal history, political affiliation, financial background, or connections\n4. Is realistic but dramatic enough to be engaging\n5. Each correction must SUBVERT THE GIST of the previous story or correction in a plausible way, so the overall message is changed or reversed in some way.\nReturn a JSON object with:\n- \"original\": a brief description of what was \"originally reported\"\n- \"correction\": the \"corrected\" version with new details. Each new correction should subvert or reverse the main message of the previous version with new juicy facts. Make the correction 1 short sentence long, and it shouldn't explain political rhetoric."""
                },
                {
                    "role": "user",
                    "content": f"""Generate a correction for this story, adding new details and/or changing specific details to subvert the gist of the story:\n\nTitle: {story['title']}\nContent: {story['content']}\n\nIf this is already a correction, subvert the gist of the previous correction. Make the correction 1 sentence long."""
                }
            ],
            max_tokens=config.get('max_tokens', 300),
            temperature=config.get('temperature', 0.7)
        )
        
        # Parse the response
        content = response.choices[0].message.content
        
        try:
            correction_data = json.loads(content)
            return correction_data
        except json.JSONDecodeError:
            # Fallback to a simple correction if JSON parsing fails
            return {
                "original": "the story",
                "correction": "the $2 million that reportedly went towards the mayor's office renovation was actually a series of donations to a nearby hospital.",
            }
            
    except Exception as e:
        print(f"Error generating AI correction: {e}")
        # Fallback to a simple correction
        return {
            "original": "the story",
            "correction": "the $2 million that reportedly went towards the mayor's office renovation was actually a series of donations to a nearby hospital.",
        }

@app.route('/get_game_history')
def get_game_history():
    """Get the game history for display"""
    return jsonify({
        'history': session.get('game_history', []),
        'current_round': session.get('game_round', 1)
    })

@app.route('/get_game_summary')
def get_game_summary():
    """Get a summary of the game session"""
    history = session.get('game_history', [])
    
    if not history:
        return jsonify({
            'total_rounds': 0,
            'corrections_made': 0,
            'summary': 'No game data available.'
        })
    
    total_rounds = len(history)
    corrections_made = sum(1 for item in history if item.get('is_corrected', False))
    
    # Analyze how stories changed
    story_changes = []
    for i, item in enumerate(history):
        if i > 0:  # Skip first round
            prev_item = history[i-1]
            if item.get('is_corrected', False):
                story_changes.append(f"Round {item['round']}: Story was 'corrected' with new details")
            else:
                story_changes.append(f"Round {item['round']}: New story introduced")
    
    # Create summary text
    summary_parts = [
        f"You played {total_rounds} rounds in this game.",
        f"Of those, {corrections_made} rounds included 'corrections' to the stories.",
        "",
        "Key observations:",
        "• Each 'correction' introduced new details that could change how you interpreted the story",
        "• Details like race, education, criminal history, and political affiliations were added",
        "• This simulates how real news can be 'corrected' in ways that change the narrative",
        "",
        "Educational insights:",
        "• Information changes as it's passed along, even with 'corrections'",
        "• Specific details can dramatically alter how we interpret events",
        "• Critical thinking about what information is emphasized or omitted is crucial",
        "• The order and framing of information matters as much as the facts themselves"
    ]
    
    summary = "\n".join(summary_parts)
    
    return jsonify({
        'total_rounds': total_rounds,
        'corrections_made': corrections_made,
        'story_changes': story_changes,
        'summary': summary
    })

@app.route('/submit_corrected_story', methods=['POST'])
def submit_corrected_story():
    """Submit player's corrected version of the story, then generate another correction and continue the loop forever"""
    data = request.get_json()
    corrected_story = data.get('story_content', '')
    corrected_significance = data.get('political_significance', '')

    # Store the corrected version
    corrected_version = {
        'round': session['game_round'],
        'original_story': session['current_story'],
        'correction': session.get('correction', {}),
        'player_story': corrected_story,
        'player_significance': corrected_significance,
        'timestamp': datetime.now().isoformat(),
        'is_corrected': True
    }

    session['game_history'].append(corrected_version)
    session['game_round'] += 1

    # Instead of ending the game, always generate a new correction that subverts the previous correction
    # Use the last correction as the new 'story' for the next correction
    last_correction = session.get('correction', {})
    if last_correction and 'correction' in last_correction:
        new_story = {'title': session['current_story']['title'], 'content': last_correction['correction']}
    else:
        new_story = session['current_story']
    new_correction = generate_correction(new_story)
    session['correction'] = new_correction
    session['current_story'] = new_story

    return jsonify({
        'success': True,
        'round': session['game_round'],
        'message': 'Corrected story submitted successfully! Here is another correction that subverts the previous one.',
        'correction': new_correction,
        'game_over': False
    })

@app.route('/generate_story')
def generate_story():
    """Generate a new story using ChatGPT API"""
    try:
        story = generate_story_with_chatgpt()
        return jsonify({'story': story})
    except Exception as e:
        print(f"Error generating story: {e}")
        # Fallback story
        fallback_story = {
            "title": "Emergency Story",
            "content": "A local community center faced budget cuts, affecting after-school programs for children. The mayor's office claimed the cuts were necessary due to declining tax revenue, but critics pointed out that the mayor had recently approved a $2 million renovation of his own office suite. The community center director, who had been vocal about the cuts, was fired shortly after speaking to the local newspaper about the impact on children."
        }
        return jsonify({'story': fallback_story})

if __name__ == '__main__':
    app.run(debug=True)
