import os
import requests
import argparse

def download_pdf(url, file_name):
    try:
        response = requests.get(url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return True, ""
    except requests.exceptions.RequestException as e:
        return False, str(e)

def save_error(url, error, error_file_name):
    with open(error_file_name, 'a') as file:
        file.write(f"URL: {url}\n")
        file.write(f"Error: {error}\n\n")

def main(url_file, dest_folder, error_file_name):
    # Create destination folder if not exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Create error file if not exists
    if not os.path.isfile(error_file_name):
        with open(error_file_name, 'w'): pass

    # Read URLs from file
    with open(url_file, 'r') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls]

    for url in urls:
        file_name = url.split("/")[-1]
        file_name = f"{dest_folder}/{file_name}"
        success, error = download_pdf(url, file_name)

        if not success:
            save_error(url, error, error_file_name)
            continue

        print(f"Downloaded: {file_name}")

if __name__ == "__main__":
    # Command line arguments configuration
    parser = argparse.ArgumentParser(description="Script to download PDF files from URLs in a file")

    parser.add_argument("-l", "--url_file", type=str, required=True, help="Path to the file containing the URLs")
    parser.add_argument("-d", "--dest_folder", type=str, default="pdfs", help="Destination folder to save downloaded files")
    parser.add_argument("-e", "--error_file_name", type=str, default="errors.txt", help="Output file name for errors")

    args = parser.parse_args()

    # Call the main function with provided arguments
    main(args.url_file, args.dest_folder, args.error_file_name)
