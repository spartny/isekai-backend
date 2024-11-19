import google.generativeai as genai

genai.configure(api_key="AIzaSyCpLTttZ7OyMDYVSRSUWBBz0pr-kEbmBZ0")

model = genai.GenerativeModel("gemini-1.5-flash")

genre_dict = {
    "1": "Fantasy",
    "2": "Science Fiction",
    "3": "Mystery",
    "4": "Adventure",
    "5": "Horror",
    "6": "Romance",
    "7": "Historical Fiction",
    "8": "Thriller",
    "9": "Superhero",
    "10": "Comedy",
    "11": "Drama"
}

def start_game(genre_choice):
    """Start a new game with the given genre choice."""
    genre = genre_dict.get(genre_choice, "Fantasy")  # Default to Fantasy
    initial_prompt = f"Please start an interactive {genre.lower()} story for me."
    response = model.generate_content(initial_prompt)

    if response:
        return {
            "genre": genre,
            "story": response.text
        }
    else:
        raise ValueError("Failed to generate content from the AI.")

def continue_game(user_input, genre, current_story):
    """Continue the story based on user input."""
    prompt = f"Continue the {genre.lower()} story based on this input: '{user_input}'. Here is the story so far: {current_story}"

    response = model.generate_content(prompt)
    if response:
        return response.text
    else:
        raise ValueError("Failed to generate content from the AI.")
