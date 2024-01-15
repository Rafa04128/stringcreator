import os
import fitz  # PyMuPDF
import re
import time
from concurrent.futures import ThreadPoolExecutor
import traceback

# Precompile regular expressions for efficiency
ALPHANUMERIC_REGEX = re.compile(r'[^a-zA-Z0-9\s]')
SPACES_REGEX = re.compile(r'\s+')

def generate_txt_path(pdf_path, output_dir):
    """
    Generate the path for the output text file based on the PDF path and output directory.
    """
    pdf_basename = os.path.basename(pdf_path)
    pdf_name, _ = os.path.splitext(pdf_basename)
    txt_path = os.path.join(output_dir, f"{pdf_name}_output.html")
    return txt_path


def clean_text(text):
    """
    Clean the extracted text by removing non-alphanumeric characters and extra spaces.
    """
    clean_text = ALPHANUMERIC_REGEX.sub('', text)
    clean_text = SPACES_REGEX.sub(' ', clean_text)
    return clean_text.strip()


def pdf_to_html(pdf_path, html_path):
    try:
        doc = fitz.open(pdf_path)
        all_html = ['<style>body { font-family: Arial, sans-serif; } p { margin: 0; }</style>']  # Add some basic styles

        for page in doc:
            html = page.get_text("html")
            # You could add additional processing here to insert or modify styles
            all_html.append(html)

        doc.close()

        full_html = '<!DOCTYPE html><html><head></head><body>' + ''.join(all_html) + '</body></html>'

        with open(html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(full_html)

    except Exception as e:
        print(f"An error occurred: {e}")



def convert_pdf_file(pdf_path, output_directory):
    """
    Helper function to process a single PDF file.
    """
    txt_path = generate_txt_path(pdf_path, output_directory)
    pdf_to_html(pdf_path, txt_path)
    print(f"Conversion completed for {os.path.basename(pdf_path)}. Text saved to {txt_path}")


def process_batch(batch, pdf_directory, output_directory, executor):
    """
    Process a batch of PDF files in parallel.
    Each file in the batch is submitted to the executor for parallel processing.
    """
    # Create a list of futures for parallel execution
    futures = [executor.submit(convert_pdf_file, os.path.join(pdf_directory, pdf_file), output_directory) for pdf_file in batch]
    
    # Wait for all futures in the batch to complete
    for future in futures:
        future.result()

def ensure_output_directory(output_directory):
    """
    Ensure that the output directory exists, and if not, create it.
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

if __name__ == "__main__":

    # ... [previous code initializing directories and pdf_files list] ...
    pdf_directory = r"C:\Users\LINES\Desktop\project\stringcreator\pdf"
    output_directory = r"C:\Users\LINES\Desktop\project\stringcreator\new_output"
    ensure_output_directory(output_directory)
    pdf_files = [pdf_file for pdf_file in os.listdir(pdf_directory) if pdf_file.endswith(".pdf")]


    start_time = time.time()

    # Create a ThreadPoolExecutor for managing parallel tasks
    with ThreadPoolExecutor() as executor:
        batch_size = 5
        futures = []  # List to store future objects

        # Divide the pdf_files into batches and submit each batch for processing
        for i in range(0, len(pdf_files), batch_size):
            batch = pdf_files[i:i + batch_size]
            # Submit the batch for processing and store the future
            future = executor.submit(process_batch, batch, pdf_directory, output_directory, executor)
            futures.append(future)

        # Wait for all futures to complete and handle exceptions
        for future in futures:
            try:
                future.result()  # Wait for the result and potentially raise an exception
            except Exception as e:
                print(f"An error occurred: {e}")
                traceback.print_exc()  # Print detailed traceback of the exception
        

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTotal PDF files converted: {len(pdf_files)}")
    print(f"Total time taken: {total_time:.2f} seconds")

    if os.path.exists(output_directory):
        total_size_output = sum(os.path.getsize(os.path.join(output_directory, file)) for file in os.listdir(output_directory))
        print(f"Total size of the output directory: {total_size_output / (1024 ** 2):.2f} MB")

    total_size_pdf = sum(os.path.getsize(os.path.join(pdf_directory, file)) for file in pdf_files)
    print(f"Total size of the PDF directory: {total_size_pdf / (1024 ** 2):.2f} MB")
