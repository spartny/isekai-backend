import google.generativeai as genai
import os
genai.configure(api_key=os.getenv("GEMINI_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


"""
"You are [Name], a [Race] [Class] known for [Background]. 
Born under the [Faction/Kingdom], your goal is to [Motivation] while navigating a [Setting]. 
Accompanied by [Companion(s)] and armed with [Inventory/Abilities], you must unravel the mystery of [Conflict]. 
Will you succeed, or will your [Flaws] doom you to failure? Choose your path wisely, as every decision shapes your destiny."
"""


def start_game(genre_choice, ch_name, ch_race, ch_class):
    """Start a new game with the given genre choice."""
    initial_prompt = f"I want to play an interactive adventure game. My character's name is {ch_name}, and they are a {ch_race} {ch_class}. I’d like the story to be set in the {genre_choice} genre. Please start the game with an immersive introduction, including the setting, my character's background, and the first scenario that requires me to make a decision. Keep the response at a maximum of 200 words. Dont give presetted options to the player. Ask 'What do you do at the end?'"
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
    prompt = f"Here is an {genre} interactive game story so far: {current_story}. The player character did this action as a continuation: '{user_input}'. Generate a response to continue the story based on this action. Keep the response at a maximum of 150 words. Dont give presetted options to the player. Ask 'What do you do at the end?'"

    response = model.generate_content(prompt)
    if response:
        return {"story": response.text
                }
                
    else:
        raise ValueError("Failed to generate content from the AI.")
