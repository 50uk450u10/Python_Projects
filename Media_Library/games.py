import libManager

class Game():
    def __init__(self, titles, genre, finished, inLibrary, location): #Constructor initializes class Book with title, author, isbn, and availability
        self.titles = titles
        self.genre = genre
        self.finished = finished
        self.inLibrary = inLibrary
        self.location = location

def gameSelection(library_data):
    while True:
        try:
            watch_select = int(input("1. View playlist\n2. Add to playlist\n3. Manage playlist\n4. Remove from playlist\n5. Return to menu\n\n"))
        except ValueError:
            print("Invalid input.\n")
            continue

        match watch_select:
            case 1:
                viewPlaylist(library_data)
            case 2:
                addToPlaylist(library_data)
            case 3:
                managePlaylist(library_data)
            case 4:
                removeFromPlaylist(library_data)
            case 5:
                print("Returning to menu.\n\n")
                return
            case _:
                print("Invalid input.\n\n")

def getTitles(prompt):
    titles = []
    for title in input(prompt).split(","):
        title = title.strip()
        if title and title.lower() not in [saved.lower() for saved in titles]:
            titles.append(title)
    return titles

def chooseGame(library_data, action):
    if not library_data["games"]:
        print("Your playlist is empty.\n")
        return None
    for index, item in enumerate(library_data["games"], start=1):
        print(f"{index}. {', '.join(item['titles'])}")
    try:
        selection = int(input(f"\nSelect the game to {action}, or enter 0 to cancel:\n"))
    except ValueError:
        print("\nInvalid input.\n")
        return None
    if selection == 0:
        return None
    if selection not in range(1, len(library_data["games"]) + 1):
        print("\nInvalid selection.\n")
        return None
    return selection - 1

def askYesNo(prompt, current=None):
    suffix = "\n1. Yes\n2. No\n"
    if current is not None:
        suffix += "Press Enter to keep the current value.\n"
    value = input(prompt + suffix).strip()
    if not value and current is not None:
        return current
    if value not in ("1", "2"):
        return None
    return value == "1"

def viewPlaylist(library_data):
    print("\n=======Playlist=======\n")

    if not library_data["games"]:
        print("Your playlist is empty.\n")
        return

    for item in library_data["games"]:
        titles = ", ".join(item["titles"])
        finished = "Yes" if item["finished"] else "No"
        owned = "Yes" if item["inLibrary"] else "No"

        print(f"Title(s): {titles}")
        print(f"Genre(s): {item['genre']}")
        print(f"Finished?: {finished}")
        print(f"Owned?: {owned}")
        print(f"Location: {item['location']}")
        print()

def addToPlaylist(library_data):
    print("\n=======Add To Playlist=======\n")

    titles = getTitles("\nEnter title(s), separated by commas:\n")
    if not titles:
        print("\nAt least one title is required.\n")
        return

    for item in library_data["games"]:
        existing_titles = [title.lower() for title in item["titles"]]
    
        for new_title in titles:
            if new_title.lower() in existing_titles:
                print(f"\n'{new_title}' already exists in your playlist.\n")
                return

    genres = input("\nEnter the genre(s):\n")

    finished = askYesNo("\nHave you finished this?")
    inLibrary = askYesNo("\nDo you own a copy of this?")
    if finished is None or inLibrary is None:
        print("\nInvalid input.\n")
        return

    if inLibrary:
        location = input("\nWhere is the copy stored?\n")
    else:
        location = "N/A"

    new_game = { 
        "titles": titles,
        "genre": genres,
        "finished": finished,
        "inLibrary": inLibrary,
        "location": location
    }

    library_data["games"].append(new_game)
    libManager.save_library(library_data)
    print("\nGame added successfully.\n")
        
def managePlaylist(library_data):
    print("\n=======Manage Playlist=======\n")

    index = chooseGame(library_data, "edit")
    if index is None:
        return
    item = library_data["games"][index]
    titles = getTitles(f"\nEnter title(s), separated by commas [{', '.join(item['titles'])}]:\n") or item["titles"]
    other_titles = {
        title.lower()
        for position, other_item in enumerate(library_data["games"])
        if position != index
        for title in other_item["titles"]
    }
    if any(title.lower() in other_titles for title in titles):
        print("\nOne of those titles already exists in your playlist.\n")
        return
    genre = input(f"\nEnter the genre(s) [{item['genre']}]:\n").strip() or item["genre"]
    finished = askYesNo("\nHave you finished this?", item["finished"])
    inLibrary = askYesNo("\nDo you own a copy of this?", item["inLibrary"])
    if finished is None or inLibrary is None:
        print("\nInvalid input.\n")
        return
    if inLibrary:
        current_location = item["location"] if item["location"] != "N/A" else ""
        location = input(f"\nWhere is the copy stored? [{current_location}]:\n").strip() or current_location
    else:
        location = "N/A"
    item.update({"titles": titles, "genre": genre, "finished": finished, "inLibrary": inLibrary, "location": location})
    libManager.save_library(library_data)
    print("\nGame updated successfully.\n")

def removeFromPlaylist(library_data):
    print("\n=======Remove From Playlist=======\n")
    index = chooseGame(library_data, "remove")
    if index is None:
        return
    item = library_data["games"][index]
    confirmation = askYesNo(f"\nRemove {', '.join(item['titles'])}?")
    if confirmation:
        library_data["games"].pop(index)
        libManager.save_library(library_data)
        print("\nGame removed successfully.\n")
    elif confirmation is False:
        print("\nRemoval cancelled.\n")
    else:
        print("\nInvalid input.\n")