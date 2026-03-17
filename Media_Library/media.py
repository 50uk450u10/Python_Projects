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
    try:
        watch_select = int(input("1. View watchlist\n2. Add to watchlist\n3. Manage watchlist\n4. Remove from watchlist\n5. Return to menu\n\n"))
    except ValueError:
            print("Invalid input.\n")
            return
            
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
        case _:
            print ("Invalid input.\n\n")

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

    titlesInput = input("\nEnter title(s), separated by commas:\n")
    titles = [title.strip() for title in titlesInput.split(",")]

    for item in library_data["media"]:
        existing_titles = [title.lower() for title in item["titles"]]
    
        for new_title in titles:
            if new_title.lower() in existing_titles:
                print(f"\n'{new_title}' already exists in your watchlist.\n")
                return

    genres = input("\nEnter the genre(s):\n")

    try:
        watched = int(input("\nHave you watched this?\n1. Yes\n2. No\n"))
        inLibrary = int(input("\nDo you own a copy of this?\n1. Yes\n2. No\n"))
    except ValueError:
        print("\nInvalid input.\n")
        return
    
    if watched not in (1, 2) or inLibrary not in (1, 2):
        print("\nInvalid input.\n")
        return
    
    watched = watched == 1
    inLibrary = inLibrary == 1

    if inLibrary:
        location = input("\nWhere is the copy stored?\n")
        whereToWatch = input("\nWrite the service or link where to watch:\n")
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

def removeFromWatchlist(library_data):
    print("\n=======Remove From Watchlist=======\n")