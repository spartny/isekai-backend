from .models import Game
import datetime
from transformers import pipeline

def start_game(user, genre):
    game = Game.objects.create(
        user=user,
        genre=genre,
        current_context="",
        chat_log=[]
    )
    return game


def update_game(game, user_input, model_response, model_state=None):
    # Update chat log
    chat_entry = {
        "user_input": user_input,
        "response": model_response,
        "timestamp": datetime.datetime.now().isoformat()
    }
    game.chat_log.append(chat_entry)
    
    # Update story context
    game.current_context += f" {model_response}"
    
    # Optional: Save model state if supported
    if model_state:
        game.model_state = model_state
    
    game.save()

def resume_game(game_id):
    game = Game.objects.get(id=game_id)
    # Use `game.current_context` for your prompt
    return game

summarizer = pipeline("summarization")  # Hugging Face summarizer

def summarize_context(context, max_length=300):
    summary = summarizer(context, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

def truncate_context_if_needed(game):
    max_context_length = 4000  # Adjust based on model's token limit
    if len(game.current_context) > max_context_length:
        game.current_context = summarize_context(game.current_context)
        game.save()

# prompt = f"Continue the {game.genre.lower()} story based on this input: '{user_input}'. Here is the story so far: {game.current_context}"
# response = model.generate_content(prompt)
