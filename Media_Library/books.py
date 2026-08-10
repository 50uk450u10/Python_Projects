import libManager

class Book():

    def __init__(self, title, genre, author, read, inLibrary, location): #Constructor initializes class Book with title, author, isbn, and availability
        self.title = title
        self.author = author
        self.genre = genre
        self.read = read
        self.inLibrary = inLibrary
        self.location = location

def bookSelection(library_data):
    while True:
        try:
            selection = int(input("1. View reading list\n2. Add to reading list\n3. Manage reading list\n4. Remove from reading list\n5. Return to menu\n\n"))
        except ValueError:
            print("Invalid input.\n")
            continue

        match selection:
            case 1:
                viewBooks(library_data)
            case 2:
                addBook(library_data)
            case 3:
                manageBooks(library_data)
            case 4:
                removeBook(library_data)
            case 5:
                print("Returning to menu.\n\n")
                return
            case _:
                print("Invalid input.\n")

def chooseBook(library_data, action):
    if not library_data["books"]:
        print("Your reading list is empty.\n")
        return None
    for index, item in enumerate(library_data["books"], start=1):
        print(f"{index}. {item['title']} by {item['author']}")
    try:
        selection = int(input(f"\nSelect the book to {action}, or enter 0 to cancel:\n"))
    except ValueError:
        print("\nInvalid input.\n")
        return None
    if selection == 0:
        return None
    if selection not in range(1, len(library_data["books"]) + 1):
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

def viewBooks(library_data):
    print("\n=======Reading List=======\n")
    if not library_data["books"]:
        print("Your reading list is empty.\n")
        return
    for item in library_data["books"]:
        print(f"Title: {item['title']}")
        print(f"Author: {item['author']}")
        print(f"Genre(s): {item['genre']}")
        print(f"Read?: {'Yes' if item['read'] else 'No'}")
        print(f"Owned?: {'Yes' if item['inLibrary'] else 'No'}")
        print(f"Location: {item['location']}\n")

def addBook(library_data):
    print("\n=======Add To Reading List=======\n")
    title = input("Enter the title:\n").strip()
    if not title:
        print("\nA title is required.\n")
        return
    if any(title.lower() == item["title"].lower() for item in library_data["books"]):
        print(f"\n'{title}' already exists in your reading list.\n")
        return
    author = input("\nEnter the author:\n").strip()
    genre = input("\nEnter the genre(s):\n").strip()
    read = askYesNo("\nHave you read this?")
    inLibrary = askYesNo("\nDo you own a copy of this?")
    if read is None or inLibrary is None:
        print("\nInvalid input.\n")
        return
    location = input("\nWhere is the copy stored?\n").strip() if inLibrary else "N/A"
    library_data["books"].append({
        "title": title,
        "author": author,
        "genre": genre,
        "read": read,
        "inLibrary": inLibrary,
        "location": location
    })
    libManager.save_library(library_data)
    print("\nBook added successfully.\n")

def manageBooks(library_data):
    print("\n=======Manage Reading List=======\n")
    index = chooseBook(library_data, "edit")
    if index is None:
        return
    item = library_data["books"][index]
    title = input(f"\nEnter the title [{item['title']}]:\n").strip() or item["title"]
    if any(position != index and title.lower() == other["title"].lower() for position, other in enumerate(library_data["books"])):
        print(f"\n'{title}' already exists in your reading list.\n")
        return
    author = input(f"\nEnter the author [{item['author']}]:\n").strip() or item["author"]
    genre = input(f"\nEnter the genre(s) [{item['genre']}]:\n").strip() or item["genre"]
    read = askYesNo("\nHave you read this?", item["read"])
    inLibrary = askYesNo("\nDo you own a copy of this?", item["inLibrary"])
    if read is None or inLibrary is None:
        print("\nInvalid input.\n")
        return
    if inLibrary:
        current_location = item["location"] if item["location"] != "N/A" else ""
        location = input(f"\nWhere is the copy stored? [{current_location}]:\n").strip() or current_location
    else:
        location = "N/A"
    item.update({"title": title, "author": author, "genre": genre, "read": read, "inLibrary": inLibrary, "location": location})
    libManager.save_library(library_data)
    print("\nBook updated successfully.\n")

def removeBook(library_data):
    print("\n=======Remove From Reading List=======\n")
    index = chooseBook(library_data, "remove")
    if index is None:
        return
    item = library_data["books"][index]
    confirmation = askYesNo(f"\nRemove {item['title']}?")
    if confirmation:
        library_data["books"].pop(index)
        libManager.save_library(library_data)
        print("\nBook removed successfully.\n")
    elif confirmation is False:
        print("\nRemoval cancelled.\n")
    else:
        print("\nInvalid input.\n")