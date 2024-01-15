import os
import requests
from bs4 import BeautifulSoup

def sanitize_filename(title):
    # Remove invalid file name characters and whitespace characters
    invalid_chars = '<>:"/\\|?*\r\n'
    for char in invalid_chars:
        title = title.replace(char, '')
    # Replace spaces with underscores for consistency
    title = title.replace(' ', '_')
    # Limit the length of the title to avoid filesystem errors
    return title[:200]


def download_gutenberg_books():
    base_url = "https://www.gutenberg.org"
    bookshelf_url = "https://www.gutenberg.org/ebooks/bookshelf/102"
    download_directory = "gutenberg_books"

    # Create the directory if it does not exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    try:
        # Fetch the content of the bookshelf page
        response = requests.get(bookshelf_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all book links with the 'booklink' class
        book_items = soup.find_all('li', class_='booklink')
        print(f"Found {len(book_items)} books")

        # Iterate over each book link item
        for item in book_items:
            # Find the 'a' element within each 'booklink' item
            link = item.find('a')
            if link and 'href' in link.attrs:
                book_title = link.get_text().strip()
                sanitized_title = sanitize_filename(book_title)
                print(f"Located book: {book_title}")

                book_page_url = base_url + link['href']
                book_page_response = requests.get(book_page_url)
                book_page_soup = BeautifulSoup(book_page_response.content, 'html.parser')

                # Find the PDF download link (the selector might be different)
                pdf_link = book_page_soup.find('a', class_='link')
                if pdf_link:
                    pdf_url = base_url + pdf_link['href']
                    pdf_response = requests.get(pdf_url)
                    file_name = sanitized_title + '.pdf'  # Append '.pdf' extension to the sanitized title

                    # Save the PDF file in the specified directory
                    full_path = os.path.join(download_directory, file_name)
                    with open(full_path, 'wb') as file:
                        file.write(pdf_response.content)
                    print(f"Downloaded and saved '{book_title}' as '{file_name}'")

    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    download_gutenberg_books()
