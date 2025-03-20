import streamlit as st
import pandas as pd
import pickle  # For saving and loading books
import os

# File to save books data
BOOKS_FILE = "books_data.pkl"

# Load books from file (if exists)
def load_books():
    try:
        if os.path.exists(BOOKS_FILE):
            with open(BOOKS_FILE, "rb") as file:
                return pickle.load(file)
    except Exception as e:
        st.error(f"Error loading books: {e}")
    return []

# Save books to file
def save_books():
    try:
        with open(BOOKS_FILE, "wb") as file:
            pickle.dump(st.session_state.books, file)
        st.success("📁 All books have been saved successfully!")
    except Exception as e:
        st.error(f"Error saving books: {e}")

# Initialize session state
if "books" not in st.session_state:
    st.session_state.books = load_books()

if "selected_book" not in st.session_state:
    st.session_state.selected_book = None

# Sidebar Menu
st.sidebar.title("📖 Menu")
options = st.sidebar.radio("Select an option:", [
    "Add a book", "Remove a book", "Search for a book", "Display all books",
    "Display Statistics", "Save Books", "Exit"
])

st.title("📚 Personal Library Manager")

# Add a book
if options == "Add a book":
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        publication_year = st.number_input("Publication Year", min_value=1000, max_value=2025, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Mark As Read")
        book_image = st.file_uploader("Upload Book Cover", type=["png", "jpg", "jpeg"])
        submit = st.form_submit_button("Add Book")
        
        if submit:
            if not title or not author or not genre or not publication_year:
                st.error("⚠️ Please fill out all required fields before submitting.")
            else:
                st.session_state.books.append({
                    "Title": title,
                    "Author": author,
                    "Year": publication_year,
                    "Genre": genre,
                    "Read": "✅ Read" if read_status else "❌ Not Read",
                    "Image": book_image.read() if book_image else None
                })
                st.success(f"✅ '{title}' added successfully!")

# Display all books
elif options == "Display all books":
    st.subheader("📚 All Books in Library")

    if not st.session_state.books:
        st.warning("No books added yet. Please add a book first.")
    else:
        df = pd.DataFrame([{key: book[key] for key in book if key != "Image"} for book in st.session_state.books])
        selected_title = st.selectbox("Select a book to view details:", df["Title"].tolist())
        st.dataframe(df)

        # Display details of the selected book
        selected_book = next((book for book in st.session_state.books if book["Title"] == selected_title), None)
        if selected_book:
            st.subheader(f"📖 Details of '{selected_title}'")
            st.write(f"**Author:** {selected_book['Author']}")
            st.write(f"**Publication Year:** {selected_book['Year']}")
            st.write(f"**Genre:** {selected_book['Genre']}")
            st.write(f"**Read Status:** {selected_book['Read']}")

            # Display book image if available
            if selected_book["Image"]:
                st.image(selected_book["Image"], caption=selected_title, use_column_width=True)
            else:
                st.write("No image available for this book.")

# Remove a book
elif options == "Remove a book":
    if not st.session_state.books:
        st.warning("No books available to remove. Please add a book first.")
    else:
        book_to_remove = st.text_input("Enter Book Title to Remove")

        if st.button("Remove Book"):
            books_filtered = [book for book in st.session_state.books if book["Title"].lower() != book_to_remove.lower()]

            if len(books_filtered) < len(st.session_state.books):
                st.session_state.books = books_filtered
                st.success(f"✅ '{book_to_remove}' has been removed successfully!")
            else:
                st.error(f"⚠️ No book found with the title '{book_to_remove}'. Please check the title and try again.")

# 🔥 FIXED: Search for a book
elif options == "Search for a book":  
    search_query = st.text_input("Enter Title or Author Name to Search")  

    if search_query:
        results = [
            {key: book[key] for key in book if key != "Image"}  # 🔥 EXCLUDING IMAGE
            for book in st.session_state.books
            if search_query.lower() in book["Title"].lower() or search_query.lower() in book["Author"].lower()
        ]

        if results:
            df_results = pd.DataFrame(results)
            st.dataframe(df_results)
        else:
            st.warning("No books found matching your search.")

# Display statistics
elif options == "Display Statistics":
    total_books = len(st.session_state.books)
    read_books = sum(1 for book in st.session_state.books if book["Read"] == "✅ Read")
    unread_books = total_books - read_books

    st.subheader("📊 Library Statistics")
    st.write(f"**Total Books:** {total_books}")
    st.write(f"**Read Books:** {read_books} ({(read_books/total_books)*100 if total_books > 0 else 0:.2f}%)")
    st.write(f"**Unread Books:** {unread_books} ({(unread_books/total_books)*100 if total_books > 0 else 0:.2f}%)")

# Save Books
elif options == "Save Books":
    save_books()


