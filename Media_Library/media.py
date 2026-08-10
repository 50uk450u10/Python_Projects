import libManager

class Media():
    def __init__(self, titles, genre, watched, whereToWatch, inLibrary, location):
        self.titles = titles
        self.genre = genre
        self.watched = watched
        self.whereToWatch = whereToWatch
        self.inLibrary = inLibrary
        self.location = location

def mediaSelection(library_data):
    while True:
        try:
            watch_select = int(input("1. View watchlist\n2. Add to watchlist\n3. Manage watchlist\n4. Remove from watchlist\n5. Return to menu\n\n"))
        except ValueError:
            print("Invalid input.\n")
            continue

        match watch_select:
            case 1:
                viewWatchlist(library_data)
            case 2:
                addToWatchlist(library_data)
            case 3:
                manageWatchlist(library_data)
            case 4:
                removeFromWatchlist(library_data)
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

def chooseMedia(library_data, action):
    if not library_data["media"]:
        print("Your watchlist is empty.\n")
        return None

    for index, item in enumerate(library_data["media"], start=1):
        print(f"{index}. {', '.join(item['titles'])}")

    try:
        selection = int(input(f"\nSelect the media to {action}, or enter 0 to cancel:\n"))
    except ValueError:
        print("\nInvalid input.\n")
        return None

    if selection == 0:
        return None
    if selection not in range(1, len(library_data["media"]) + 1):
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

def viewWatchlist(library_data):
    print("\n=======Watchlist=======\n")

    if not library_data["media"]:
        print("Your watchlist is empty.\n")
        return

    for item in library_data["media"]:
        titles = ", ".join(item["titles"])
        watched = "Yes" if item["watched"] else "No"
        owned = "Yes" if item["inLibrary"] else "No"

        print(f"Title(s): {titles}")
        print(f"Genre(s): {item['genre']}")
        print(f"Watched?: {watched}")
        print(f"Owned?: {owned}")
        print(f"Where to Watch: {item['whereToWatch']}")
        print(f"Location: {item['location']}")
        print()

def addToWatchlist(library_data):
    print("\n=======Add To Watchlist=======\n")

    titles = getTitles("\nEnter title(s), separated by commas:\n")
    if not titles:
        print("\nAt least one title is required.\n")
        return

    for item in library_data["media"]:
        existing_titles = [title.lower() for title in item["titles"]]
    
        for new_title in titles:
            if new_title.lower() in existing_titles:
                print(f"\n'{new_title}' already exists in your watchlist.\n")
                return

    genres = input("\nEnter the genre(s):\n")

    watched = askYesNo("\nHave you watched this?")
    inLibrary = askYesNo("\nDo you own a copy of this?")
    if watched is None or inLibrary is None:
        print("\nInvalid input.\n")
        return

    if inLibrary:
        location = input("\nWhere is the copy stored?\n")
    else:
        location = "N/A"
    whereToWatch = input("\nWrite the service or link where to watch:\n")

    new_media = { 
        "titles": titles,
        "genre": genres,
        "watched": watched,
        "whereToWatch": whereToWatch,
        "inLibrary": inLibrary,
        "location": location
    }

    library_data["media"].append(new_media)
    libManager.save_library(library_data)
    print("\nMedia added successfully.\n")
        
def manageWatchlist(library_data):
    print("\n=======Manage Watchlist=======\n")

    index = chooseMedia(library_data, "edit")
    if index is None:
        return

    item = library_data["media"][index]
    titles = getTitles(f"\nEnter title(s), separated by commas [{', '.join(item['titles'])}]:\n")
    if not titles:
        titles = item["titles"]

    other_titles = {
        title.lower()
        for position, other_item in enumerate(library_data["media"])
        if position != index
        for title in other_item["titles"]
    }
    if any(title.lower() in other_titles for title in titles):
        print("\nOne of those titles already exists in your watchlist.\n")
        return

    genre = input(f"\nEnter the genre(s) [{item['genre']}]:\n").strip() or item["genre"]
    watched = askYesNo("\nHave you watched this?", item["watched"])
    inLibrary = askYesNo("\nDo you own a copy of this?", item["inLibrary"])
    if watched is None or inLibrary is None:
        print("\nInvalid input.\n")
        return

    if inLibrary:
        current_location = item["location"] if item["location"] != "N/A" else ""
        location = input(f"\nWhere is the copy stored? [{current_location}]:\n").strip() or current_location
    else:
        location = "N/A"

    where = input(f"\nWrite the service or link where to watch [{item['whereToWatch']}]:\n").strip()
    item.update({
        "titles": titles,
        "genre": genre,
        "watched": watched,
        "whereToWatch": where or item["whereToWatch"],
        "inLibrary": inLibrary,
        "location": location
    })
    libManager.save_library(library_data)
    print("\nMedia updated successfully.\n")

def removeFromWatchlist(library_data):
    print("\n=======Remove From Watchlist=======\n")

    index = chooseMedia(library_data, "remove")
    if index is None:
        return

    item = library_data["media"][index]
    confirmation = askYesNo(f"\nRemove {', '.join(item['titles'])}?")
    if confirmation:
        library_data["media"].pop(index)
        libManager.save_library(library_data)
        print("\nMedia removed successfully.\n")
    elif confirmation is False:
        print("\nRemoval cancelled.\n")
    else:
        print("\nInvalid input.\n")