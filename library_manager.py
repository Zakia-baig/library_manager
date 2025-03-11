import json
import os
import base64
import streamlit as st
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Library Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #f0f2f6;
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    
    .stTitle {
        color: #1a1a1a;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: white;
    }
    
    .book-card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 8px solid #6B73FF;
        transition: transform 0.2s ease;
    }
    
    .book-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        background-color: #6B73FF;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        transition: background-color 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #000DFF;
    }
    
    .stButton>button:active {
        background-color: #4B50B2;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for library if it doesn't exist
if 'library' not in st.session_state:
    st.session_state.library = []

def save_library():
    """Save library to a JSON file"""
    with open('library.json', 'w') as f:
        json.dump(st.session_state.library, f)

def load_library():
    """Load library from JSON file"""
    if os.path.exists('library.json'):
        with open('library.json', 'r') as f:
            st.session_state.library = json.load(f)

def add_book(title, author, year, genre, read_status):
    """Add a new book to the library"""
    book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read_status
    }
    st.session_state.library.append(book)
    save_library()

def remove_book(title):
    """Remove a book from the library"""
    st.session_state.library = [book for book in st.session_state.library 
                               if book['title'].lower() != title.lower()]
    save_library()

def search_books(search_term, search_by):
    """Search for books by title or author"""
    search_term = search_term.lower()
    return [book for book in st.session_state.library 
            if search_term in book[search_by].lower()]

def calculate_statistics():
    """Calculate library statistics"""
    total_books = len(st.session_state.library)
    read_books = len([book for book in st.session_state.library if book['read']])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

# Load existing library data
load_library()

# Predefined genre options
genres = [
    "Fiction", "Non-Fiction", "Mystery", "Thriller", "Science Fiction",
    "Fantasy", "Romance", "Horror", "Biography", "History", "Self-Help",
    "Poetry", "Drama", "Comedy", "Adventure", "Children's", "Young Adult",
    "Classic", "Crime", "Philosophy", "Religion", "Science", "Technology"
]

# Streamlit UI
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #2c3e50; font-size: 3.5rem; font-weight: 700;'>
            📚 Personal Library Manager
        </h1>
    </div>
""", unsafe_allow_html=True)

# Sidebar with custom styling
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <h2 style='color: #2c3e50;'>Menu Options</h2>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.selectbox(
        '',
        ['➕ Add Book', '❌ Remove Book', '🔍 Search Books', '📚 Display All Books', '📊 Statistics', '🚪 Exit']
    )

# Main content area
if menu == '➕ Add Book':
    st.header('➕ Add a New Book')
    title = st.text_input('📕 Title')  # Red book icon
    author = st.text_input('✍️ Author')
    year = st.number_input('📅 Publication Year', min_value=0, max_value=2025, value=2025)
    genre = st.selectbox('🏷️ Genre', genres)  # Dropdown for genre selection
    read_status = st.checkbox('📚 Have you read this book?')
    if st.button('Add Book', key='add_book'):
        if title and author:
            add_book(title, author, year, genre, read_status)
            st.success('✅ Book added successfully!')
        else:
            st.error('❌ Title and Author are required!')

elif menu == '❌ Remove Book':
    st.header('❌ Remove a Book')
    title = st.text_input('Enter the title of the book to remove')
    if st.button('Remove Book', key='remove_book'):
        if title:
            remove_book(title)
            st.success('✅ Book removed successfully!')
        else:
            st.error('❌ Please enter a title!')

elif menu == '🔍 Search Books':
    st.header('🔍 Search Books')
    search_by = st.radio('Search by:', ['title', 'author'])
    search_term = st.text_input('Enter search term')
    if search_term:
        results = search_books(search_term, search_by)
        if results:
            for book in results:
                st.write(f"📚 {book['title']} by {book['author']} ({book['year']}) - {book['genre']}")
                st.write(f"Status: {'Read ✓' if book['read'] else 'Unread ✗'}")
                st.write('---')
        else:
            st.info('No books found.')

elif menu == '📚 Display All Books':
    st.header('📚 Library Collection')
    if st.session_state.library:
        for book in st.session_state.library:
            st.write(f"📚 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read ✓' if book['read'] else 'Unread ✗'}")
    else:
        st.info('Your library is empty.')

elif menu == '📊 Statistics':
    st.header('📊 Library Statistics')
    total_books, read_percentage = calculate_statistics()
    st.write(f"📖 Total Books: {total_books}")
    st.write(f"✅ Books Read: {read_percentage:.1f}%")

elif menu == '🚪 Exit':
    st.write('Thank you for using the Library Manager! 👋')