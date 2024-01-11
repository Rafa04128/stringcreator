import os

def format_size(size_bytes):
    # Convert size to megabytes
    size_mb = size_bytes / (1024 ** 2)
    return f"{size_mb:.2f} MB"

def format_number(number):
    # Add commas for better readability
    return "{:,}".format(number)

def count_characters_in_directory(directory_path):
    total_characters = 0
    total_size_bytes = 0
    unique_characters = set()

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)

        # Check if the file is a text file
        if filename.endswith(".txt") and os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    num_characters = len(content)
                    total_characters += num_characters

                    # Collect unique characters from the file
                    unique_characters.update(set(content))

                    # Get the file size in bytes
                    file_size_bytes = os.path.getsize(filepath)
                    total_size_bytes += file_size_bytes

                    # Format file size for better readability
                    formatted_size = format_size(file_size_bytes)

                    print(f"File: {filename}, Characters: {format_number(num_characters)}, Size: {formatted_size}")
            except FileNotFoundError:
                print(f"Error: File not found at {filepath}")
            except Exception as e:
                print(f"Error: {e}")

    # Format total size for better readability
    formatted_total_size = format_size(total_size_bytes)

    print(f"\nTotal number of characters in all text files: {format_number(total_characters)}")
    print(f"Total size of the directory: {formatted_total_size}")

    # Output the set of all unique characters
    print(f"\nUnique characters in the text files: {', '.join(sorted(unique_characters))}")

if __name__ == "__main__":
    # Provide the path to the directory containing the text files
    text_files_directory = r"C:\Users\LINES\Desktop\project\stringcreator\output"

    # Count and print the number of characters, individual file size, and total size
    count_characters_in_directory(text_files_directory)