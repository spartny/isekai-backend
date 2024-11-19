import google.generativeai as genai
import os
genai.configure(api_key=os.getenv("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def start_game(genre_choice):
    """Start a new game with the given genre choice."""
    initial_prompt = f"Please start an interactive {genre_choice.lower()} story for me."
    print(initial_prompt)
    response = model.generate_content(initial_prompt)

    if response:
        return {
            "genre": genre_choice,
            "story": response.text
        }
    else:
        raise ValueError("Failed to generate content from the AI.")

def continue_game(user_input, genre, current_story):
    """Continue the story based on user input."""
    prompt = f"Continue the {genre.lower()} story based on this input: '{user_input}'. Here is the story so far: {current_story}"

    response = model.generate_content(prompt)
    if response:
        return {"story": response.text
                }
                
    else:
        raise ValueError("Failed to generate content from the AI.")
