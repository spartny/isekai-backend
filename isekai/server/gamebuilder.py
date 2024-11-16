import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyCpLTttZ7OyMDYVSRSUWBBz0pr-kEbmBZ0")

model = genai.GenerativeModel("gemini-1.5-flash")

print("Welcome to the interactive story generator!")
print("Choose a genre to begin your adventure:")
print("1. Fantasy")
print("2. Science Fiction")
print("3. Mystery")
print("4. Adventure")
print("5. Horror")
print("6. Romance")
print("7. Historical Fiction")
print("8. Thriller")
print("9. Superhero")
print("10. Comedy")
print("11. Drama")

genre_choice = input("Enter the number corresponding to your choice: ")

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

genre = genre_dict.get(genre_choice, "Fantasy")  # Default to Fantasy if input is invalid
print(f"You chose: {genre}")

initial_prompt = f"Please start an interactive {genre.lower()} story for me."
response = model.generate_content(initial_prompt)

try:
    print(response.text)
    story = response.text  
except ValueError:
    print("The content generated was flagged and cannot be displayed. Please try starting the story again.")
    exit()
while True:
    user_input = input("Enter what you would like to do (or type 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Thank you for playing!")
        break
    prompt = f"Continue the {genre.lower()} story based on this input: '{user_input}'. Here is the story so far: {story}"
    
    try:
        response = model.generate_content(prompt)
        print(response.text)
        story += " " + response.text
    except ValueError as e:
        print("The content generated was flagged and cannot be displayed. Please try entering a different input.")

