import os

def count_total_characters_in_directory(directory_path):
    total_characters_across_all_files = 0

    try:
        # Iterate over all files in the directory
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)

            # Check if the file is a text file
            if filename.endswith(".txt") and os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()

                    # Count total characters for each file
                    total_characters = len(content)
                    total_characters_across_all_files += total_characters

                    # Format total characters for better readability
                    formatted_total_characters = "{:,}".format(total_characters)

                    # Print the total number of characters for each file
                    print(f"File: {filename}, Total characters: {formatted_total_characters}")

        # Format total characters across all files for better readability
        formatted_total_across_all_files = "{:,}".format(total_characters_across_all_files)
        print(f"\nTotal characters across all files: {formatted_total_across_all_files}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Provide the path to the directory containing the text files
    text_files_directory = r"C:\Users\LINES\Desktop\project\stringcreator\output"

    # Count and print the total number of characters for all files in the directory
    count_total_characters_in_directory(text_files_directory)
