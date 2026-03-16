class Media():
    def __init__(self, titles, genre, watched, whereToWatch, inLibrary, location):
        self.titles = titles
        self.genre = genre
        self.watched = watched
        self.whereToWatch = whereToWatch
        self.inLibrary = inLibrary
        self.location = location

def mediaSelection():
    try:
        watch_select = int(input("1. View watchlist\n2. Add to watchlist\n3. Manage watchlist\n4. Remove from watchlist\n5. Return to menu\n\n"))
    except ValueError:
            print("Invalid input.\n")
            
    match watch_select:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            print("Returning to menu.\n\n")
        case _:
            print ("Invalid input.\n\n")
