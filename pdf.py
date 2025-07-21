import re
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text_to_fp
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import io

def extract_text(file, logging, source):
    logging.info(f'{source}:- Setting up PDF text extraction')
    
    try:
        # Reset file pointer to beginning
        file.seek(0)
        
        # Extract text using pdfminer
        output_string = io.StringIO()
        
        with file.stream as fp:
            extract_text_to_fp(fp, output_string, 
                             laparams=LAParams(
                                 boxes_flow=0.5,
                                 word_margin=0.1,
                                 char_margin=2.0,
                                 line_margin=0.5
                             ))
        
        text = output_string.getvalue()
        
        # Clean and format the text
        text = clean_extracted_text(text)
        
        logging.info(f'{source}:- Successfully extracted {len(text)} characters from {file.filename}')
        return text
        
    except Exception as e:
        logging.error(f'{source}:- Error extracting text: {str(e)}')
        raise

def clean_extracted_text(text):
    """Clean and format extracted text for better readability"""
    
    # Remove excessive whitespace and control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize line breaks
    text = re.sub(r'\r\n|\r', '\n', text)
    
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Fix spacing issues
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
    text = re.sub(r' +\n', '\n', text)   # Remove trailing spaces
    text = re.sub(r'\n +', '\n', text)   # Remove leading spaces on new lines
    
    # Try to preserve paragraph structure
    text = re.sub(r'([.!?])\s*\n\s*([A-Z])', r'\1\n\n\2', text)
    
    return text.strip()
