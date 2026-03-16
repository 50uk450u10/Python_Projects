import json
import os

FILE_NAME = "library.json"

def load_library():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                print(f"{FILE_NAME} loaded successfully.\n")
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            print(f"{FILE_NAME} was invalid. Creating a new one.\n")

    data = {
        "media": [],
        "games": [],
        "books": []
    }

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

    return data

def save_library(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)