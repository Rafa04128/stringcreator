import os
import requests
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=5):
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query={query}&max_results={max_results}"

    response = requests.get(base_url + search_query)
    if response.status_code == 200:
        return response.text
    else:
        return None

def save_metadata(metadata, output_folder):
    for entry in metadata.findall('.//entry'):
        identifier = entry.find('.//id').text.split(':')[-1]
        title = entry.find('.//title').text
        authors = [author.find('.//name').text for author in entry.findall('.//author')]
        summary = entry.find('.//summary').text

        metadata_content = f"Title: {title}\nAuthors: {', '.join(authors)}\nSummary: {summary}\n"

        metadata_filename = os.path.join(output_folder, f"{identifier}_metadata.txt")
        with open(metadata_filename, 'w', encoding='utf-8') as metadata_file:
            metadata_file.write(metadata_content)

def main():
    query = "cat:cs.AI"  # Example query for articles in the computer science category (Artificial Intelligence)
    max_results = 5
    output_folder = "metadata"

    # Ensure the existence of the output directory
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    result = search_arxiv(query, max_results)
    if result:
        root = ET.fromstring(result)
        save_metadata(root, output_folder)
        print(f"Metadata saved to {output_folder}")
    else:
        print("Failed to retrieve data from arXiv API")

if __name__ == "__main__":
    main()
