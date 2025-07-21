import os
import logging
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from pdf import extract_text  # <-- your PDF text extraction logic here

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE_MB = 25
MAX_CONTENT_LENGTH = MAX_FILE_SIZE_MB * 1024 * 1024  # 25 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = "supersecretkey"  # Needed for flash messaging

logging.basicConfig(level=logging.INFO)

# --- Utility Functions ---

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_files' not in request.files:
        flash('No files part in the request.')
        return redirect(request.url)
    
    files = request.files.getlist('pdf_files')
    if not files or files[0].filename == '':
        flash('No PDF files selected.')
        return redirect(request.url)

    extracted_texts = dict()
    for file in files:
        filename = secure_filename(file.filename)
        logging.info(f"[{filename}] Processing...")

        # File size limit check (browser should prevent oversized files, but double check)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > MAX_CONTENT_LENGTH:
            msg = f"File '{filename}' exceeds {MAX_FILE_SIZE_MB} MB limit."
            logging.warning(f"[{filename}] {msg}")
            extracted_texts[filename] = (msg,)
            continue

        if not allowed_file(filename):
            msg = "Invalid file type (only PDF allowed)."
            extracted_texts[filename] = (msg,)
            continue

        try:
            text = extract_text(file, logging, source=filename)
            if not text.strip():
                extracted_texts[filename] = ("No extractable text found in this file.",)
            else:
                extracted_texts[filename] = (text,)
            logging.info(f"[{filename}] Extraction successful.")
        except Exception as e:
            logging.error(f"[{filename}] Error: {str(e)}")
            extracted_texts[filename] = (f"Extraction failed: {str(e)}",)

    return render_template('results.html', extracted_texts=extracted_texts)

# --- Error Handling Routes ---

@app.errorhandler(413)
def too_large(e):
    flash(f"File too large. Max size is {MAX_FILE_SIZE_MB} MB per file!")
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', error_message="A server error occurred."), 500

# --- Run / Entrypoint ---

if __name__ == '__main__':
    app.run(debug=True)
