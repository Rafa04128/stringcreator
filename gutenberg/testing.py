import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def sanitize_filename(title):
    # Remove invalid file name characters and whitespace characters
    invalid_chars = '<>:"/\\|?*\r\n'
    for char in invalid_chars:
        title = title.replace(char, '')
    # Replace spaces with underscores for consistency
    title = title.replace(' ', '_')
    # Limit the length of the title to avoid filesystem errors
    return title[:200]


def download_pdf(pdf_url, download_directory, file_name):
    # Download the PDF file
    pdf_response = requests.get(pdf_url)
    full_path = os.path.join(download_directory, file_name)
    with open(full_path, 'wb') as file:
        file.write(pdf_response.content)
    print(f"Downloaded and saved '{file_name}'")


def download_books_from_page(url, download_directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    book_items = soup.find_all('li', class_='booklink')
    print(f"Found {len(book_items)} books on page")

    for item in book_items:
        link = item.find('a')
        if link and 'href' in link.attrs:
            book_title = link.get_text().strip()
            sanitized_title = sanitize_filename(book_title)
            print(f"Located book: {book_title}")

            book_page_url = urljoin(url, link['href'])
            book_page_response = requests.get(book_page_url)
            book_page_soup = BeautifulSoup(book_page_response.content, 'html.parser')

            # Find the PDF download link (the selector might be different)
            pdf_link = book_page_soup.find('a', class_='link')
            if pdf_link:
                pdf_url = urljoin(url, pdf_link['href'])
                file_name = sanitized_title + '.pdf'  # Append '.pdf' extension to the sanitized title
                download_pdf(pdf_url, download_directory, file_name)

    # Find the 'Next' link and return its URL if it exists
    next_link = soup.find('a', text='Next')
    if next_link and 'href' in next_link.attrs:
        next_page_url = urljoin(url, next_link['href'])
        return next_page_url
    else:
        return None

def download_gutenberg_books(start_url):
    current_page_url = start_url
    download_directory = "gutenberg_books"

    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    while current_page_url:
        print(f"Processing page: {current_page_url}")
        try:
            next_page_url = download_books_from_page(current_page_url, download_directory)
            current_page_url = next_page_url
        except Exception as e:
            print(f"Error during processing page {current_page_url}: {e}")
            break

if __name__ == "__main__":
    base_url = "https://www.gutenberg.org"
    bookshelf_url = f"{base_url}/ebooks/bookshelf/102"
    download_gutenberg_books(bookshelf_url)
