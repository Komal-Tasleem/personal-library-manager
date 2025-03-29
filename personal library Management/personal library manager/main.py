import streamlit as st
import json
from collections import Counter

# File to store library data
LIBRARY_FILE = "library.txt"

def load_library():
    """Loads the library from a file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Saves the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    """Adds a new book to the library."""
    library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
    save_library(library)
    st.success("Book added successfully!")

def remove_book(library, title):
    """Removes a book by title."""
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            st.success("Book removed successfully!")
            return
    st.warning("Book not found.")

def search_books(library, query, search_by):
    """Searches for books by title or author."""
    results = [book for book in library if query.lower() in book[search_by].lower()]
    if results:
        for book in results:
            status = "Read" if book["read"] else "Unread"
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.warning("No matching books found.")

def display_books(library):
    """Displays all books in the library with sorting options."""
    if not library:
        st.write("Your library is empty.")
        return
    
    sort_option = st.selectbox("Sort books by", ["Title", "Author", "Year", "Genre", "Read Status"], index=0)
    
    if sort_option == "Title":
        library.sort(key=lambda x: x["title"].lower())
    elif sort_option == "Author":
        library.sort(key=lambda x: x["author"].lower())
    elif sort_option == "Year":
        library.sort(key=lambda x: x["year"], reverse=True)
    elif sort_option == "Genre":
        library.sort(key=lambda x: x["genre"].lower())
    elif sort_option == "Read Status":
        library.sort(key=lambda x: x["read"], reverse=True)
    
    for book in library:
        status = "Read" if book["read"] else "Unread"
        st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}")

def display_statistics(library):
    """Displays statistics about the library, including most common genres and authors."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books else 0
    
    genres = [book["genre"] for book in library]
    authors = [book["author"] for book in library]
    
    most_common_genre = Counter(genres).most_common(1)
    most_common_author = Counter(authors).most_common(1)
    
    st.write(f"**Total books:** {total_books}")
    st.write(f"**Percentage read:** {percentage_read:.2f}%")
    
    if most_common_genre:
        st.write(f"**Most common genre:** {most_common_genre[0][0]} ({most_common_genre[0][1]} books)")
    if most_common_author:
        st.write(f"**Most read author:** {most_common_author[0][0]} ({most_common_author[0][1]} books)")

def main():
    """Main function to run the Streamlit app."""
    st.title("📚 Personal Library Manager")
    library = load_library()
    
    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Add a Book":
        with st.form("add_book_form"):
            title = st.text_input("Enter the book title")
            author = st.text_input("Enter the author")
            year = st.number_input("Enter the publication year", min_value=0, step=1)
            genre = st.text_input("Enter the genre")
            read_status = st.checkbox("Have you read this book?")
            submit = st.form_submit_button("Add Book")
            
            if submit and title and author and genre:
                add_book(library, title, author, year, genre, read_status)
    
    elif choice == "Remove a Book":
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            remove_book(library, title)
    
    elif choice == "Search for a Book":
        search_by = st.radio("Search by", ["title", "author"])
        query = st.text_input(f"Enter {search_by}")
        if st.button("Search"):
            search_books(library, query, search_by)
    
    elif choice == "Display All Books":
        display_books(library)
    
    elif choice == "Display Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()
