import media
import games
import books
import libManager

def main():
    library_data = libManager.load_library()

    while True:
        print("\n=======Media Library=======\n")
        try:
            selection = int(input("Welcome to your library! Please select your category.\n1. Anime, Movies, and TV\n2. Games\n3. Books\n4. Exit\n\n"))
        except ValueError:
            print("Invalid input.\n")
            continue
    

        match selection:
            case 1:
                media.mediaSelection(library_data)
            case 2:
                games.gameSelection(library_data)
            case 3:
                books.bookSelection(library_data)
            case 4:
                print("Exiting watchlist.\n\n")
                break
            case _:
                print("Invalid input.\n\n")
                continue

if __name__ == "__main__":
    main()