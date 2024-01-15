import requests
from bs4 import BeautifulSoup

def scrape_books(url, topic):
    # Send a request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the web page")
        return

    # Parse the content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find elements related to the topic - this will vary depending on the website's structure
    # For example, finding all titles of books (this is a hypothetical example)
    books = soup.find_all('div', class_='book-title')  # Adjust the tag and class based on actual website structure

    # Extract and print book titles or other relevant information
    for book in books:
        title = book.get_text()
        print(title)

# Replace with the actual topic you are interested in
topic = "Computer Science"
url = "https://archive.org/details/books"

scrape_books(url, topic)