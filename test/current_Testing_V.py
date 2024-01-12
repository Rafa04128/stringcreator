import os
import fitz  # PyMuPDF
import re
import time
from concurrent.futures import ThreadPoolExecutor

def generate_txt_path(pdf_path, output_dir):
    """
    Generate the path for the output text file based on the PDF path and output directory.
    """
    pdf_basename = os.path.basename(pdf_path)
    pdf_name, _ = os.path.splitext(pdf_basename)
    txt_path = os.path.join(output_dir, f"{pdf_name}_output.txt")
    return txt_path

def clean_text(text):
    """
    Clean the extracted text by removing non-alphanumeric characters and extra spaces.
    """
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

def pdf_to_text(pdf_path, txt_path):
    try:
        doc = fitz.open(pdf_path)
        all_text = []
        for i, page in enumerate(doc):
            print(f"Processing page {i + 1}/{len(doc)}")
            blocks = page.get_text("dict")["blocks"]
            page_text = []
            for b in blocks:
                if b['type'] == 0:
                    for line in b["lines"]:
                        for span in line["spans"]:
                            page_text.append(f"Text: {span['text']}, Font: {span['font']}, Size: {span['size']}")
            all_text.append('\n'.join(page_text))

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write('\n\n'.join(all_text))
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_batch(pdf_files, pdf_directory, output_directory):
    """
    Convert a batch of PDF files to text.
    """
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        txt_path = generate_txt_path(pdf_path, output_directory)
        pdf_to_text(pdf_path, txt_path)
        print(f"Conversion completed for {pdf_file}. Text saved to {txt_path}")

def ensure_output_directory(output_directory):
    """
    Ensure that the output directory exists, and if not, create it.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

if __name__ == "__main__":
    pdf_directory = r"C:\Users\R. García\Desktop\Projects\MrKlean\stringcreator\pdf"
    output_directory = r"C:\Users\R. García\Desktop\Projects\MrKlean\stringcreator\new_output"
    ensure_output_directory(output_directory)

    pdf_files = [pdf_file for pdf_file in os.listdir(pdf_directory) if pdf_file.endswith(".pdf")]

    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        batch_size = 5
        for i in range(0, len(pdf_files), batch_size):
            batch = pdf_files[i:i + batch_size]
            executor.map(lambda pdf_batch: convert_batch(pdf_batch, pdf_directory, output_directory), [batch])

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTotal PDF files converted: {len(pdf_files)}")
    print(f"Total time taken: {total_time:.2f} seconds")

    # Calculate and display the total size of the output and PDF directories
    if os.path.exists(output_directory):
        total_size_output = sum(os.path.getsize(os.path.join(output_directory, file)) for file in os.listdir(output_directory))
        print(f"Total size of the output directory: {total_size_output / (1024 ** 2):.2f} MB")

    total_size_pdf = sum(os.path.getsize(os.path.join(pdf_directory, file)) for file in pdf_files)
    print(f"Total size of the PDF directory: {total_size_pdf / (1024 ** 2):.2f} MB")