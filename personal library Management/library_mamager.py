import json
import streamlit as st

# File to store library data
LIBRARY_FILE = "library.txt"

def load_library():
    """Load library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Save library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    """Add a new book to the library."""
    library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
    save_library(library)
    st.success("Book added successfully!")

def remove_book(library, title):
    """Remove a book by title."""
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            st.success("Book removed successfully!")
            return
    st.error("Book not found.")

def search_books(library, keyword, search_by):
    """Search for books by title or author."""
    results = [book for book in library if keyword.lower() in book[search_by].lower()]
    return results

def display_books(library):
    """Display all books in the library."""
    if not library:
        st.write("Your library is empty.")
    else:
        for book in library:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

def display_statistics(library):
    """Display statistics about the library."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

def main():
    """Streamlit UI for the Personal Library Manager."""
    st.title("📚 Personal Library Manager")
    library = load_library()
    
    menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add Book":
        st.subheader("Add a New Book")
        title = st.text_input("Enter the book title")
        author = st.text_input("Enter the author")
        year = st.number_input("Enter the publication year", min_value=0, step=1)
        genre = st.text_input("Enter the genre")
        read_status = st.checkbox("Have you read this book?")
        if st.button("Add Book"):
            add_book(library, title, author, year, genre, read_status)
    
    elif choice == "Remove Book":
        st.subheader("Remove a Book")
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            remove_book(library, title)
    
    elif choice == "Search Book":
        st.subheader("Search for a Book")
        search_by = st.radio("Search by", ("title", "author"))
        keyword = st.text_input("Enter search keyword")
        if st.button("Search"):
            results = search_books(library, keyword, search_by)
            if results:
                for book in results:
                    st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
            else:
                st.write("No matching books found.")
    
    elif choice == "Display All Books":
        st.subheader("Your Library")
        display_books(library)
    
    elif choice == "Statistics":
        st.subheader("Library Statistics")
        display_statistics(library)

if __name__ == "__main__":
    main()
