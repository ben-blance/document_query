# Document Query Application

![image](https://github.com/user-attachments/assets/43fa9ac6-037d-4e17-95b6-94c98502cfac)

![image](https://github.com/user-attachments/assets/811e574b-21cb-428a-b8c9-d55928852682)

![image](https://github.com/user-attachments/assets/8ec71c2e-466c-4645-9a97-f725e457104f)



## Overview

The Document Query Application is a Streamlit-based web app that allows users to upload, query, and manage documents. The application supports user registration and authentication, document management, and querying of document contents. It also records user interactions and provides the ability to download chat history.

## Features

- **User Authentication**: Register and log in to manage documents and interact with the system.
- **Document Upload**: Upload documents in `.pdf`, `.docx`, or `.txt` formats. Each document is associated with the user who uploaded it.
- **Document Querying**: Search for documents based on their content or by document ID.
- **User Interaction Recording**: Record and store user interactions with the application.
- **Chat History Management**: View and download the history of user interactions with the application.

## Prerequisites

- Python 3.8 or higher
- Streamlit
- SQLite3
- Pandas (for exporting chat history)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/document-query-app.git
   cd document-query-app
   ```
## Features

- **User Authentication**: Register and log in to manage documents and interact with the system.
- **Document Upload**: Upload documents in `.pdf`, `.docx`, or `.txt` formats. Each document is associated with the user who uploaded it.
- **Document Querying**: Search for documents based on their content or by document ID.
- **User Interaction Recording**: Record and store user interactions with the application.
- **Chat History Management**: View and download the history of user interactions with the application.

## Prerequisites

- Python 3.8 or higher
- Streamlit
- SQLite3
- Pandas (for exporting chat history

## Instructions

### User Registration and Login

1. Open the application in your browser.
2. In the sidebar, select the **"Register"** tab.
3. Enter a username and password, then click **"Register"**. If successful, you will see a confirmation message to log in.
4. To log in, switch to the **"Login"** tab in the sidebar.
5. Enter your registered username and password, then click **"Login"**. Upon successful login, you will see your User ID in the sidebar.

### Uploading Documents

1. Once logged in, navigate to the **"Upload Documents"** section in the sidebar.
2. Use the file uploader to select and upload documents in .pdf, .docx, or .txt formats.
3. After uploading, the document will be stored in the database and associated with your user ID. You will receive a confirmation message with the document ID.

### Searching for Documents

1. Go to the **"User Interaction"** section in the sidebar.
2. Select **"Query"** to search documents based on their content.
3. Enter your search query and click **"Search"**.
4. Results will be displayed, showing document IDs, filenames, and content snippets.
5. Alternatively, select **"Document ID"** to search by a specific document ID.
6. Enter the document ID and click **"Search by ID"**.
7. The document details will be shown, including filename and content snippet.

### Viewing and Downloading Chat History

1. If you want to view your chat history, scroll down to the **"Your Chat History"** section in the sidebar.
2. Your previous queries and responses will be listed. You can download this history by clicking the **"Download Chat History"** button.
3. This will generate a CSV file with your chat history, which you can save to your local machine.

### Database Schema

- **users table**: Stores user credentials (username and password).
- **documents table**: Stores document metadata and content, associated with a user ID.
- **user_history table**: Records user interactions with queries and responses.

### Contributing

Feel free to submit issues or pull requests if you have improvements or suggestions.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
