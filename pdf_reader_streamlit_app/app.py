import streamlit as st
import fitz  
import pytesseract
from pdf2image import convert_from_bytes
import base64

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure Streamlit page
st.set_page_config(page_title="PDF Text Extractor", layout="wide")

# Sidebar Information
with st.sidebar:
    st.title("PDF OCR Tool")
    st.write("""
    This tool can:
    - Extract text from regular PDFs
    - Use OCR to extract text from scanned PDFs

    **Instructions:**
    1. Upload a PDF file
    2. Wait for processing
    3. View or download the extracted text
    """)
    st.markdown("---")
    st.caption("Built with Streamlit, PyMuPDF, and Tesseract")

# Main page
st.title("PDF Text Extractor")
st.write("Extract text from both digital and scanned PDFs easily.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Function to extract text
def extract_text(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    pages_text = []
    
    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text()

        if text.strip():
            content = f"\n--- Page {i + 1} ---\n{text}"
        else:
            st.info(f"No text detected on Page {i + 1}, applying OCR...")
            images = convert_from_bytes(file_bytes, first_page=i+1, last_page=i+1)
            ocr_text = pytesseract.image_to_string(images[0])
            content = f"\n--- Page {i + 1} (OCR) ---\n{ocr_text}"

        full_text += content
        pages_text.append(content)

    return full_text, pages_text

# Function to generate download link
def download_link(text, filename="extracted_text.txt"):
    b64_text = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64_text}" download="{filename}">Download Extracted Text</a>'

# Main app logic
if uploaded_file:
    with st.spinner("Processing..."):
        try:
            file_bytes = uploaded_file.read()
            text, pages = extract_text(file_bytes)

            st.success("Extraction completed.")

            view_option = st.radio("View mode", ["All Text", "By Page"], horizontal=True)

            if view_option == "All Text":
                st.text_area("Extracted Text", value=text, height=500)
            else:
                for page_text in pages:
                    st.text_area("Page", value=page_text, height=300)

            st.markdown(download_link(text), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a PDF file to begin.")

