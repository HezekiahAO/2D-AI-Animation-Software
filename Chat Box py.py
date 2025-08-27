# =======================
# Book Recommendation Chatbot
# =======================

# Sample list of books
books = [
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "genre": "Fantasy",
        "age_group": "Teen",
        "tags": ["magic", "school", "adventure"]
    },
    {
        "title": "The Hound of the Baskervilles",
        "author": "Arthur Conan Doyle",
        "genre": "Mystery",
        "age_group": "Adult",
        "tags": ["detective", "crime", "classic"]
    },
    {
        "title": "The Very Hungry Caterpillar",
        "author": "Eric Carle",
        "genre": "Children",
        "age_group": "Kids",
        "tags": ["animals", "learning", "illustration"]
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": "Fiction",
        "age_group": "Adult",
        "tags": ["race", "justice", "classic"]
    },
    {
        "title": "Percy Jackson & The Olympians",
        "author": "Rick Riordan",
        "genre": "Fantasy",
        "age_group": "Teen",
        "tags": ["mythology", "adventure", "magic"]
    },
    {
        "title": "Nancy Drew: The Secret of the Old Clock",
        "author": "Carolyn Keene",
        "genre": "Mystery",
        "age_group": "Kids",
        "tags": ["detective", "adventure", "girls"]
    }
]

# Extract genre and age group from user input
def extract_intent(user_input):
    input_words = user_input.lower().split()
    genres = ["fantasy", "mystery", "children", "fiction"]
    age_groups = ["kids", "teen", "adult"]

    genre = None
    age_group = None

    for word in input_words:
        if word in genres:
            genre = word.capitalize()
        if word in age_groups:
            age_group = word.capitalize()

    return genre, age_group

# Recommend matching books
def recommend_books(genre=None, age_group=None):
    recommendations = []
    for book in books:
        if genre and genre != book['genre']:
            continue
        if age_group and age_group != book['age_group']:
            continue
        recommendations.append(book)
    return recommendations[:3]  # Limit to top 3

# Main chatbot function
def chatbot():
    print("📚 Welcome to BookBot! Ask me for a book recommendation.")
    print("You can say things like 'Suggest a fantasy book for teens' or 'Give me a mystery novel'.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("BookBot: Bye! Happy reading! 📖")
            break

        genre, age_group = extract_intent(user_input)
        recommendations = recommend_books(genre, age_group)

        if recommendations:
            print("\nBookBot: Here's what I recommend:")
            for book in recommendations:
                print(f" - \"{book['title']}\" by {book['author']} [{book['genre']} | {book['age_group']}]")
        else:
            print("\nBookBot: Hmm... I couldn't find a match. Try mentioning a genre (like 'fantasy') or age group (like 'teen').")

        print()  # extra space between messages

# Run chatbot
if __name__ == "__main__":
    chatbot()
