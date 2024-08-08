import sqlite3
import streamlit as st
from datetime import datetime

# Database setup
def create_tables():
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')
    
    # Create documents table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        content BLOB,
        format TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create user_history table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        query TEXT,
        response TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Register new user
def register_user(username, password):
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

# Authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

# Insert document into database and return its ID
def insert_document(user_id, filename, content, content_type):
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO documents (user_id, filename, content, format)
        VALUES (?, ?, ?, ?)
        ''', (user_id, filename, sqlite3.Binary(content), content_type))
        doc_id = cursor.lastrowid
        conn.commit()
        return doc_id
    finally:
        conn.close()

# Record user interaction
def record_user_interaction(user_id, query, response):
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user_history (user_id, query, response, timestamp)
    VALUES (?, ?, ?, ?)
    ''', (user_id, query, response, timestamp))
    conn.commit()
    conn.close()

# Query documents
def query_documents(user_query):
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, content FROM documents')
    documents = cursor.fetchall()
    
    results = []
    for doc_id, filename, content in documents:
        try:
            content_text = content.decode('utf-8', errors='ignore')
            if user_query.lower() in content_text.lower():
                results.append((doc_id, filename, content_text))
        except Exception as e:
            print(f"Error decoding content for file {filename}: {e}")
    
    conn.close()
    return results

# Get user history
def get_user_history(user_id):
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_history WHERE user_id = ?', (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

# Get document by ID
def get_document_by_id(doc_id):
    conn = sqlite3.connect('document_query_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, content FROM documents WHERE id = ?', (doc_id,))
    document = cursor.fetchone()
    conn.close()
    return document

# Download chat history
def download_chat_history(user_id, history):
    import pandas as pd
    from io import BytesIO

    df = pd.DataFrame(history, columns=['ID', 'User ID', 'Query', 'Response', 'Timestamp'])
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Chat History",
        data=csv,
        file_name=f'chat_history_{user_id}.csv',
        mime='text/csv'
    )

# Streamlit app
def main():
    st.title('Document Query Application')
    
    # Sidebar for user authentication
    st.sidebar.header('User Authentication')
    auth_action = st.sidebar.selectbox('Choose Action', ['Login', 'Register'])
    username = st.sidebar.text_input('Username')
    password = st.sidebar.text_input('Password', type='password')
    
    if auth_action == 'Register':
        if st.sidebar.button('Register'):
            user_id = register_user(username, password)
            if user_id:
                st.sidebar.success('Registration successful! Please log in.')
            else:
                st.sidebar.error('Username already exists. Please choose another.')
    elif auth_action == 'Login':
        if st.sidebar.button('Login'):
            user_id = authenticate_user(username, password)
            if user_id:
                st.sidebar.success('Login successful!')
                st.session_state.user_id = user_id
            else:
                st.sidebar.error('Invalid username or password.')
    
    # Main content area
    if 'user_id' in st.session_state:
        user_id = st.session_state.user_id
        st.sidebar.write(f'Logged in as User ID: {user_id}')
        
        # Document upload section
        st.sidebar.header('Upload Documents')
        uploaded_file = st.sidebar.file_uploader('Upload .pdf, .docx, or .txt files', type=['pdf', 'docx', 'txt'])
        if uploaded_file:
            content = uploaded_file.read()
            doc_id = insert_document(user_id, uploaded_file.name, content, uploaded_file.type)
            st.sidebar.success(f'Document uploaded successfully! Assigned ID: {doc_id}')
        
        # User interaction section
        st.sidebar.header('User Interaction')
        search_option = st.sidebar.selectbox('Search by:', ['Query', 'Document ID'])
        
        if search_option == 'Query':
            user_query = st.sidebar.text_input('Enter your question:')
            if st.sidebar.button('Search') and user_query:
                results = query_documents(user_query)
                if results:
                    st.subheader('Results:')
                    for doc_id, filename, content_text in results:
                        st.write("Document ID:", doc_id)
                        st.write("Filename:", filename)
                        st.write("Content:", content_text[:500])  # Displaying the first 500 characters of content
                        record_user_interaction(user_id, user_query, content_text[:500])
                else:
                    st.write('No results found.')
        elif search_option == 'Document ID':
            doc_id = st.sidebar.number_input('Enter Document ID:', min_value=1, step=1)
            if st.sidebar.button('Search by ID'):
                document = get_document_by_id(doc_id)
                if document:
                    doc_id, filename, content = document
                    st.subheader(f'Document ID: {doc_id}')
                    st.write("Filename:", filename)
                    st.write("Content:", content.decode('utf-8', errors='ignore')[:500])  # Displaying the first 500 characters of content
                    record_user_interaction(user_id, f'Search by ID: {doc_id}', content.decode('utf-8', errors='ignore')[:500])
                else:
                    st.write('No document found with that ID.')
        
        # Display user's chat history
        history = get_user_history(user_id)
        if history:
            st.sidebar.subheader('Your Chat History:')
            for entry in history:
                st.sidebar.write("Query:", entry[2])
                st.sidebar.write("Response:", entry[3])
                st.sidebar.write("Timestamp:", entry[4])
            download_chat_history(user_id, history)
        else:
            st.sidebar.write('No chat history found for user ID:', user_id)
    else:
        st.write('Please log in to use the application.')

if __name__ == '__main__':
    create_tables()
    main()
