import json
import os

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.json")

DEFAULT_LIBRARY = {
    "media": [],
    "games": [],
    "books": []
}

def load_library():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError

                for category in DEFAULT_LIBRARY:
                    if not isinstance(data.get(category), list):
                        data[category] = []

                print("library.json loaded successfully.\n")
                return data
        except (json.JSONDecodeError, FileNotFoundError, OSError, ValueError):
            print("library.json was invalid. Creating a new one.\n")

    data = {category: [] for category in DEFAULT_LIBRARY}

    save_library(data)

    return data

def save_library(data):
    temporary_file = f"{FILE_NAME}.tmp"
    with open(temporary_file, "w") as file:
        json.dump(data, file, indent=4)
    os.replace(temporary_file, FILE_NAME)