import os
import csv

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
    file_data = []  # List to store data for each file

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
                    unique_characters.update(set(content))
                    file_size_bytes = os.path.getsize(filepath)
                    total_size_bytes += file_size_bytes
                    formatted_size = format_size(file_size_bytes)

                    # Add the file data to the list
                    file_data.append([filename, format_number(num_characters), formatted_size])
                    
            except FileNotFoundError:
                print(f"Error: File not found at {filepath}")
            except Exception as e:
                print(f"Error: {e}")

    formatted_total_size = format_size(total_size_bytes)
    print(f"\nTotal number of characters in all text files: {format_number(total_characters)}")
    print(f"Total size of the directory: {formatted_total_size}")
    print(f"\nUnique characters in the text files: {', '.join(sorted(unique_characters))}")

    return file_data  # Return the collected data

def write_to_csv(data, csv_file_path):
    # Write data to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Number of Characters', 'File Size'])
        writer.writerows(data)

if __name__ == "__main__":
    text_files_directory = r"C:\Users\R. García\Desktop\Projects\MrKlean\stringcreator\new_output"
    csv_file_path = r"C:\Users\R. García\Desktop\Projects\MrKlean\stringcreator\file_data.csv"  # Path to save the CSV file

    file_data = count_characters_in_directory(text_files_directory)
    write_to_csv(file_data, csv_file_path)
    print(f"Data saved to {csv_file_path}")
