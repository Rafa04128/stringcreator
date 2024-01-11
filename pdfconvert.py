import os
import fitz  # PyMuPDF
import re
import time
from concurrent.futures import ThreadPoolExecutor

def generate_txt_path(pdf_path, output_dir):
    pdf_basename = os.path.basename(pdf_path)
    pdf_name, _ = os.path.splitext(pdf_basename)
    txt_path = os.path.join(output_dir, f"{pdf_name}_output.txt")
    return txt_path

def pdf_to_text(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count

    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
            clean_text = re.sub(r'\s+', ' ', clean_text)

            txt_file.write(clean_text.strip())

def convert_batch(pdf_files, pdf_directory, output_directory):
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        txt_path = generate_txt_path(pdf_path, output_directory)
        pdf_to_text(pdf_path, txt_path)
        print(f"Conversion completed for {pdf_file}. Text saved to {txt_path}")

def ensure_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

if __name__ == "__main__":
    pdf_directory = r"C:\Users\LINES\Desktop\project\stringcreator\pdf"
    output_directory = r"C:\Users\LINES\Desktop\project\stringcreator\output"

    # Ensure the existence of the output directory
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
    print(f"\nTotal time taken: {total_time:.2f} seconds")

    # Get the total size of the output directory if it exists
    if os.path.exists(output_directory):
        total_size_output = sum(os.path.getsize(os.path.join(output_directory, file)) for file in os.listdir(output_directory))
        total_size_output_mb = total_size_output / (1024 ** 2)
        print(f"Total size of the output directory: {total_size_output_mb:.2f} MB")
    else:
        print("Output directory not found.")

    total_size_pdf = sum(os.path.getsize(os.path.join(pdf_directory, file)) for file in pdf_files)
    total_size_pdf_mb = total_size_pdf / (1024 ** 2)
    print(f"Total size of the PDF directory: {total_size_pdf_mb:.2f} MB")
