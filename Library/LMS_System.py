import json

class Book():

    def __init__(self, title, author, isbn, available = True): #Constructor initializes class Book with title, author, isbn, and availability
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def display_info(self): #Function to display all information about a book
        status = "Available" if self.available else "Unavailable"
        print(f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\nStatus: {status}\n")

class Library():
    def __init__(self):
        self.books = [] #Creates an empty list on initializing to store books

    def add_book(self, book):
        self.books.append(book) #Appends books to the aforementioned list
        print(f"Book '{book.title}' added to the library.\n")
    
    def borrow_book(self, isbn):
        for book in self.books: #Loop to sift through the list for a matching ISBN
            if book.isbn == isbn:
                if book.available:
                    book.available = False #Set availability to false since the book will be checked out
                    print(f"{book.title} checked out, enjoy!\n")
                    return
                else:
                    print("Sorry, that book is already checked out.\n")
                    return
        print("Book not found in the library.\n")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.available: #Check to make sure the isbn entered is actually checked out before checking in
                    book.available = True
                    print(f"{book.title} checked back in.\n")
                    return
                else:
                    print("Book not checked out.\n")
                    return
        print("Book not found in the library.\n")
    
    def display_books(self): #Functions shows all books stored in the library
        if not self.books:
            print("There are no books in the library.\n")
        else:
            print("Library book list:\n")
            for book in self.books:
                book.display_info()
            print()
    
    def save_to_file(self, filename): #JSON formatted save system records book information in list "data"
        try:
            data = [
                {"title": b.title, "author": b.author, "isbn": b.isbn, "available": b.available}
                for b in self.books
            ]
            with open(filename, "w") as file:
                json.dump(data, file, indent = 4)
            print(f"Library saved to {filename}")
        except Exception as e:
            print("Error saving file:", e)

    def load_from_file(self, filename): #Loads all stored books from a JSON format
        try: #Try/Except handling for various errors
            with open(filename, "r") as file:
                data = json.load(file)
                self.books = [Book(**item) for item in data] #**item unpacks all the data for each book in the list
            print(f"Library loaded from {filename}.")
        except FileNotFoundError:
            print(f"No file named '{filename}' found.")
        except json.JSONDecodeError:
            print("Error reading file: file may be corrupted.")
        except Exception as e:
            print("Error loading file:", e)

def main():
    library = Library()

    while True:
        print("\n=======Library Management System=======\n")
        choice = input("1. Add Book\n2. Borrow Book\n3. Return Book\n4. View All Books\n5. Save Library to File\n6. Load Library from File\n7. Exit\n").strip()
        match choice: #Simple match/case option menu
            case "1":
                title = input("Enter title:\n")
                author = input("\nEnter author:\n")
                isbn = input("\nEnter ISBN:\n")
                library.add_book(Book(title, author, isbn))
            case "2":
                isbn = input("Enter ISBN to check a book out:\n")
                library.borrow_book(isbn)
            case "3":
                isbn = input("Enter ISBN to check a book back in:\n")
                library.return_book(isbn)
            case "4":
                library.display_books()
            case "5":
                filename = input("Enter filename to store data (e.g. Library.json):\n")
                library.save_to_file(filename)
            case "6":
                filename = input("Enter filename to pull data from:\n")
                library.load_from_file(filename)
            case "7":
                print("\nExiting Library Management System.\n")
                break
            case _:
                print("Invalid input, Please enter a number between 1 and 7.\n")

main() #Run main