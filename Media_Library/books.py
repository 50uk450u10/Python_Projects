class Book():

    def __init__(self, title, genre, author, read, inLibrary, location): #Constructor initializes class Book with title, author, isbn, and availability
        self.title = title
        self.author = author
        self.genre = genre
        self.read = read
        self.inLibrary = inLibrary
        self.location = location

def display_info(self): #Function to display all information about a book
    status = "Available" if self.available else "Unavailable"
    print(f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\nStatus: {status}\n")

def bookSelection():
    pass