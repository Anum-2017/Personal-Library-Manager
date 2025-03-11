import streamlit as st 
import json

st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📖", layout="wide")

# Function to load the library data from a file
def load_library(filename="library.json"):
    try:
        with open(filename, "r") as file:
            library = json.load(file)
        return library
    except FileNotFoundError:
        return []

# Function to save the library data to a file
def save_library(library, filename="library.json"):
    with open(filename, "w") as file:
        json.dump(library, file)

# Function to display the statistics
def display_statistics(library):
    total_books = len(library)
    if total_books > 0:
        read_books = sum(1 for book in library if book['read_status'])
        percentage_read = (read_books / total_books) * 100
        
        # Create two columns for statistics and percentage side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"📚 Total books: <br><span style='font-size: 40px;'>{total_books}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"✅ Percentage read: <br><span style='font-size: 40px;'>{percentage_read:.2f}%</span>", unsafe_allow_html=True)
        
        st.progress(percentage_read / 100)  
    else:
        st.write("❌ No books to display statistics for.")

# Streamlit App layout
st.markdown("<h1 style='text-align: center;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

library = load_library()

# Add an image in the sidebar, with error handling
try:
    st.sidebar.image("book_icon.png", use_container_width=True)
except:
    st.sidebar.write("⚠️ Image not found: 'book_icon.png'")

# Sidebar for navigation with icons
menu_options = {
    "Homepage": "🏠 Homepage",
    "Add a New book": "📚 Add a book",
    "Remove a book": "🗑️ Remove a book",
    "Search for a book": "🔍 Search for a book",
    "Display all books": "📖 Display all books",
    "Display statistics": "📊 Display statistics",
}

menu = st.sidebar.selectbox("Choose an option", list(menu_options.values()))

# Homepage content
if menu == menu_options["Homepage"]:
    # Center the text and add image to the homepage
    st.markdown("<h3 style='text-align: center;'>Welcome to Your Personal Library Manager! 📚</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>This app allows you to manage your book collection, track your reading progress, and keep everything organized.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Use the sidebar to add, remove, search, or view books. You can also check out your reading stats!</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enjoy your reading journey! 😄</p>", unsafe_allow_html=True)
    
    # Adding image, with error handling
    try:
        st.image("homepage.jpg", use_container_width=True)
    except:
        st.warning("⚠️ Image not found: 'homepage.jpg'")

elif menu == menu_options["Add a New book"]:
    st.subheader("📝 Add a New Book")
    title = st.text_input("**📚 Enter the book title**")
    author = st.text_input("**✍️ Enter the author**")
    year = st.number_input("**📅 Enter the publication year**", min_value=1, max_value=2025, value=2023)
    genre = st.text_input("**📚 Enter the genre**")
    read_status = st.radio("**🤔 Have you read this book?**", ("Yes ✅", "No ❌"))
    
    if st.button("Add Book ➕"):
        if title and author and genre:
            read_status_bool = read_status == "Yes ✅"
            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read_status": read_status_bool
            }
            library.append(book)
            save_library(library)  
            st.success(f"📘 Book '{title}' added successfully!")
        else:
            st.warning("⚠️ Please fill in all fields to add the book.")

elif menu == menu_options["Remove a book"]:
    st.subheader("🗑️ Remove a Book")
    title_to_remove = st.text_input("**📚 Enter the title of the book to remove**")
    
    if st.button("Remove Book 🗑️"):
        book_found = False
        for book in library:
            if book['title'].lower() == title_to_remove.lower():
                library.remove(book)
                save_library(library)  # Save library after removing a book (step 8: Save Library)
                st.success(f"📖 Book '{title_to_remove}' removed successfully!")
                book_found = True
                break
        
        if not book_found:
            st.warning(f"⚠️ Book with title '{title_to_remove}' not found.")

elif menu == menu_options["Search for a book"]:
    st.subheader("🔍 Search for a Book")
    search_by = st.selectbox("**Search by**📜", ["Title", "Author"])
    search_query = st.text_input(f"**Enter the {search_by.lower()}🧐** ")
    
    if st.button("Search 🔎"):
        if search_by == "Title":
            found_books = [book for book in library if search_query.lower() in book['title'].lower()]
        else:
            found_books = [book for book in library if search_query.lower() in book['author'].lower()]
        
        if found_books:
            st.write("📚 Matching Books:")
            for book in found_books:
                status = " Read ✔️" if book['read_status'] else "Unread ❌"
                st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning("⚠️ No books found.")

elif menu == menu_options["Display all books"]:
    st.subheader("📚 All Books in Your Library")
    
    if library:
        for i, book in enumerate(library, 1):
            status = " Read ✔️" if book['read_status'] else "Unread ❌"
            st.write(f"{i}. 📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.warning("⚠️ Your library is empty.")

elif menu == menu_options["Display statistics"]:
    st.subheader("📊 Library Statistics")
    display_statistics(library)

# Footer with icon
st.markdown(""" 
    <hr>
    <p style='text-align: center; font-size: 14px;'>Developed by Anum Kamal 💜 | Powered by Streamlit 🚀</p>
""", unsafe_allow_html=True)

