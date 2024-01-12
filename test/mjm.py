import os
import fitz  # PyMuPDF
import re
import time
from concurrent.futures import ThreadPoolExecutor

# Pre-compiled regular expressions for efficiency
regex_non_alphanum = re.compile(r'[^a-zA-Z0-9\s]')
regex_spaces = re.compile(r'\s+')

def generate_txt_path(pdf_path, output_dir):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return os.path.join(output_dir, f"{pdf_name}_otro_new_output.txt")

def clean_text(text):
    text = regex_non_alphanum.sub('', text)
    return regex_spaces.sub(' ', text).strip()

def pdf_to_text(pdf_path, txt_path):
    import fitz  # PyMuPDF

def pdf_to_text(pdf_path, txt_path):
    try:
        doc = fitz.open(pdf_path)
        all_text = []

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            page_text = (f"Text: {span['text']}, Font: {span['font']}, Size: {span['size']}"
                         for b in blocks if b['type'] == 0
                         for line in b["lines"]
                         for span in line["spans"])
            all_text.extend(page_text)

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write('\n'.join(all_text))
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_batch(pdf_files, pdf_directory, output_directory):
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        txt_path = generate_txt_path(pdf_path, output_directory)
        pdf_to_text(pdf_path, txt_path)

def ensure_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

if __name__ == "__main__":
    pdf_directory = r"C:\Users\R. García\Desktop\Projects\MrKlean\stringcreator\pdf"
    output_directory = r"C:\Users\R. García\Desktop\Projects\MrKlean\stringcreator\otro_new_output"
    ensure_output_directory(output_directory)

    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        batches = [pdf_files[i:i + 5] for i in range(0, len(pdf_files), 5)]
        executor.map(lambda batch: convert_batch(batch, pdf_directory, output_directory), batches)
    end_time = time.time()

    total_time = end_time - start_time

    print(f"\nTotal PDF files converted: {len(pdf_files)}")
    print(f"Total time taken: {total_time:.2f} seconds")

    # Size calculations can be refactored into a function if needed elsewhere
    output_size = sum(os.path.getsize(os.path.join(output_directory, f)) for f in os.listdir(output_directory))
    pdf_size = sum(os.path.getsize(os.path.join(pdf_directory, f)) for f in pdf_files)
    print(f"Total size of the output directory: {output_size / (1024 ** 2):.2f} MB")
    print(f"Total size of the PDF directory: {pdf_size / (1024 ** 2):.2f} MB")
