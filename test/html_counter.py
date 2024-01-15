import os
import glob
from collections import Counter

def count_chars_in_directory(directory):
    total_size_bytes = 0
    all_chars = Counter()

    # Loop through all HTML files in the specified directory
    for filepath in glob.glob(os.path.join(directory, '*.html')):
        # Update the total size in bytes
        total_size_bytes += os.path.getsize(filepath)

        # Read the content of the file
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            # Update the character count
            all_chars.update(content)

    # Calculate the total number of characters
    total_chars = sum(all_chars.values())

    # Convert total size to megabytes
    total_size_mb = total_size_bytes / (1024 ** 2)

    # Get all unique characters
    unique_chars = list(all_chars)

    return total_chars, total_size_mb, unique_chars

# Replace 'your/directory/path' with the path to your directory containing HTML files
directory_path = r"C:\Users\LINES\Desktop\project\stringcreator\new_output"
total_chars, total_size_mb, unique_chars = count_chars_in_directory(directory_path)

print(f"Total number of characters: {total_chars:,}")  # Format with commas
print(f"Total size of directory: {total_size_mb:.2f} MB")  # Format to 2 decimal places
print(f"Unique characters: {unique_chars}")
