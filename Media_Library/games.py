import libManager

class Game():
    def __init__(self, titles, genre, finished, inLibrary, location): #Constructor initializes class Book with title, author, isbn, and availability
        self.titles = titles
        self.genre = genre
        self.finished = finished
        self.inLibrary = inLibrary
        self.location = location

def gameSelection(library_data):
    try:
        watch_select = int(input("1. View playlist\n2. Add to playlist\n3. Manage playlist\n4. Remove from playlist\n5. Return to menu\n\n"))
    except ValueError:
            print("Invalid input.\n")
            return
            
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
        case _:
            print ("Invalid input.\n\n")

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

    titlesInput = input("\nEnter title(s), separated by commas:\n")
    titles = [title.strip() for title in titlesInput.split(",")]

    for item in library_data["games"]:
        existing_titles = [title.lower() for title in item["titles"]]
    
        for new_title in titles:
            if new_title.lower() in existing_titles:
                print(f"\n'{new_title}' already exists in your playlist.\n")
                return

    genres = input("\nEnter the genre(s):\n")

    try:
        finished = int(input("\nHave you finished this?\n1. Yes\n2. No\n"))
        inLibrary = int(input("\nDo you own a copy of this?\n1. Yes\n2. No\n"))
    except ValueError:
        print("\nInvalid input.\n")
        return
    
    if finished not in (1, 2) or inLibrary not in (1, 2):
        print("\nInvalid input.\n")
        return
    
    finished = finished == 1
    inLibrary = inLibrary == 1

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

def removeFromPlaylist(library_data):
    pass