# PDF Text Extractor API & Web App

A straightforward Flask application designed to extract text from PDF files. It provides both a simple web interface for direct user uploads and a RESTful API for programmatic access. The application is built to be robust, with features like file validation, comprehensive logging, and a production-ready setup using Gunicorn and Docker for easy deployment.



---

## Features

-   **Dual Interface**: Access the service through a user-friendly web interface or a simple REST API.
-   **Multi-File Upload**: The web UI supports uploading and processing multiple PDF files simultaneously.
-   **File Validation**: Implements checks to ensure that uploaded files are in PDF format and do not exceed the maximum size limit of 25MB.
-   **Robust Logging**: All processes are logged with a unique request ID for easy tracking and debugging. Logs are automatically rotated to manage disk space.
-   **API & Web Separation**: The core logic is separated from the interface, allowing for independent use and testing of the text extraction functionality.
-   [cite_start]**Deployment Ready**: Comes configured with `gunicorn` for production use [cite: 2] and a `heroku.yml` file for easy deployment to Heroku using Docker.

---

## Tech Stack & Dependencies

-   [cite_start]**Backend**: Python 3.11.5 [cite: 3][cite_start], Flask [cite: 2]
-   [cite_start]**PDF Processing**: `pdfminer.six` [cite: 2]
-   [cite_start]**WSGI Server**: `gunicorn` [cite: 2]
-   **Deployment**: Docker, Heroku
-   **Frontend**: Basic HTML5

[cite_start]Key dependencies are listed in the `requirements.txt` file[cite: 2].

---

## Installation and Local Setup

To get this project running on your local machine, follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run

You can run the application using the standard Flask development server or a production-grade server like Gunicorn.

-   **For development:**
    ```bash
    flask run
    ```
    The app will be available at `http://127.0.0.1:5000`.

-   **For production (using Gunicorn):**
    ```bash
    gunicorn --bind 0.0.0.0:5000 main:app
    ```

---

## Using the Application

### Web Interface

1.  Navigate to the root URL: `http://127.0.0.1:5000/`.
2.  Click the "Choose Files" button to select one or more PDF files from your local machine.
3.  Click the "Upload" button to process the files.
4.  The next page will display the extracted text for each successfully processed file or an error message if a file could not be processed.

### API Endpoint

The application provides a RESTful endpoint for text extraction. This is useful for integrating the service into other applications.

**Endpoint:** `/upload_file`
**Method:** `POST`
**Body:** `multipart/form-data`

The request must contain a single file part named `file`.

**Example using cURL:**

```bash
curl -X POST -F "file=@/path/to/your/document.pdf" [http://127.0.0.1:5000/upload_file](http://127.0.0.1:5000/upload_file)
