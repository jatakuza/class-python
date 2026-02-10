import os

BOOKS_FILE = "books.txt"
USERS_FILE = "users.txt"
LIBRARIANS_FILE = "librarians.txt"

class Book:
    def __init__(self, title, author, status="available"):
        self._title = title
        self._author = author
        self._status = status

    def is_available(self):
        return self._status == "available"

    def take(self):
        self._status = "taken"

    def return_book(self):
        self._status = "available"

    def to_string(self):
        return f"{self._title} | {self._author} | {self._status}"

    @staticmethod
    def from_string(line):
        title, author, status = line.strip().split("|")
        return Book(title, author, status)


class Person:
    def __init__(self, name):
        self._name = name


class User(Person):
    def __init__(self, name, borrowed_books=None):
        super().__init__(name)
        self._borrowed_books = borrowed_books or []

    def menu(self, library):
        while True:
            print("\n1. View available books")
            print("2. Take a book")
            print("3. Return a book")
            print("4. My books")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                library.show_available_books()

            elif choice == "2":
                title = input("Book title: ")
                library.take_book(self, title)

            elif choice == "3":
                title = input("Book title: ")
                library.return_book(self, title)

            elif choice == "4":
                print("My books:", ", ".join(self._borrowed_books) or "none")

            elif choice == "0":
                break

    def to_string(self):
        books = ",".join(self._borrowed_books)
        return f"{self._name}|{books}"

    @staticmethod
    def from_string(line):
        name, books = line.strip().split("|")
        borrowed = books.split(",") if books else []
        return User(name, borrowed)


class Librarian(Person):
    def menu(self, library):
        while True:
            print("\n1. Add a new book")
            print("2. Remove a book")
            print("3. Register a new user")
            print("4. View all users")
            print("5. View all books")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                library.add_book(title, author)

            elif choice == "2":
                title = input("Book title: ")
                library.remove_book(title)

            elif choice == "3":
                name = input("User name: ")
                library.add_user(name)

            elif choice == "4":
                library.show_users()

            elif choice == "5":
                library.show_all_books()

            elif choice == "0":
                break


class Library:
    def __init__(self):
        self._books = []
        self._users = []
        self._librarians = []

    def load_data(self):
        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE) as f:
                self._books = [Book.from_string(line) for line in f]

        if os.path.exists(USERS_FILE):
            with open(USERS_FILE) as f:
                self._users = [User.from_string(line) for line in f]

        if os.path.exists(LIBRARIANS_FILE):
            with open(LIBRARIANS_FILE) as f:
                self._librarians = [Person(line.strip()) for line in f]

    def save_data(self):
        with open(BOOKS_FILE, "w") as f:
            for book in self._books:
                f.write(book.to_string() + "\n")

        with open(USERS_FILE, "w") as f:
            for user in self._users:
                f.write(user.to_string() + "\n")

        with open(LIBRARIANS_FILE, "w") as f:
            for librarian in self._librarians:
                f.write(librarian._name + "\n")

    def add_book(self, title, author):
        self._books.append(Book(title, author))
        print("Book added successfully")

    def remove_book(self, title):
        self._books = [b for b in self._books if b._title != title]
        print("Book removed successfully")

    def add_user(self, name):
        self._users.append(User(name))
        print("User registered successfully")

    def show_users(self):
        for user in self._users:
            print(user._name)

    def show_all_books(self):
        for book in self._books:
            print(f"{book._title} - {book._author} ({book._status})")

    def show_available_books(self):
        for book in self._books:
            if book.is_available():
                print(f"{book._title} - {book._author}")

    def take_book(self, user, title):
        for book in self._books:
            if book._title == title:
                if book.is_available():
                    book.take()
                    user._borrowed_books.append(title)

                    print("Book has been taken")
                else:
                    print("Book is already taken")

                return
        print("Book not found")

    def return_book(self, user, title):
        if title in user._borrowed_books:
            for book in self._books:
                if book._title == title:
                    book.return_book()
                    user._borrowed_books.remove(title)

                    print("Book returned successfully")
                    return

        print("You don't have this book")

def main():
    library = Library()
    library.load_data()

    print("1. Librarian")
    print("2. User")
    role = input("Choose role: ")

    name = input("Enter name: ")

    if role == "1":
        librarian = Librarian(name)
        library._librarians.append(librarian)
        librarian.menu(library)

    elif role == "2":
        user = next((u for u in library._users if u._name == name), None)

        if not user:
            print("User not found")
            return

        user.menu(library)

    library.save_data()

if __name__ == "__main__":
    main()
