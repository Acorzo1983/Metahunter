import os
import re
import argparse
import sys
import time
import csv
from concurrent.futures import ThreadPoolExecutor

# Define allowed domain extensions
allowed_domains = ['.gov', '.net', '.com', '.edu', '.org']

def extract_emails_from_file(file_path, error_output):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        file_content = file.read()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', file_content)
        for email in emails:
            if is_allowed_domain(email):
                try:
                    yield f'{file_path}: {email}\n'
                except UnicodeEncodeError:
                    error_output.write(f'{file_path}: {email}\n')

def is_allowed_domain(email):
    for domain in allowed_domains:
        if domain in email:
            return True
    return False

def count_files(folder_path):
    count = 0
    for root, dirs, files in os.walk(folder_path):
        count += len(files)
    return count

def process_file(file_path, output, error_output):
    emails = extract_emails_from_file(file_path, error_output)
    for email in emails:
        output.write(email)

def process_files(folder_path, output_file):
    total_files = count_files(folder_path)
    processed_files = 0

    with open(output_file, 'w', encoding='utf-8') as output, open("outputfilename_errors.txt", 'w', encoding='utf-8') as error_output:
        with ThreadPoolExecutor() as executor:
            results = []

            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    processed_files += 1

                    # Ignore the output file while processing files
                    if file_path != os.path.abspath(output_file):
                        results.append(executor.submit(process_file, file_path, output, error_output))

            # Simple animation with progress bar
            while True:
                completed = sum(1 for result in results if result.done())
                progress = completed / total_files * 100

                sys.stdout.write('\r')
                sys.stdout.write(f'Processing files: [{"#" * int(progress / 10):<10}] {progress:.2f}% ({completed}/{total_files})')
                sys.stdout.flush()

                if completed == len(results):
                    break

                time.sleep(0.1)

    sys.stdout.write('\n')

if __name__ == "__main__":
    # Add creator credits and version at the beginning
    print("Email Hunter - Version Beta 0.2")
    print("Created by Albert.C\n")

    parser = argparse.ArgumentParser(description='Script to extract email addresses from files in a folder.')
    parser.add_argument('-f', '--folder', metavar='folder_path', type=str, default='.', help='Path of the folder containing the files (default: current folder)')
    parser.add_argument('-o', '--output', metavar='output_file', type=str, default='email_discovered.txt', help='Output file for email addresses (default: email_discovered.txt)')

    args = parser.parse_args()
    folder_path = args.folder
    output_file = args.output

    process_files(folder_path, output_file)

    # Ask if a clean CSV file is desired
    if input("Do you want to generate the clean CSV file? (y/n): ").lower() == "y":
        cleaned_output_file = os.path.splitext(output_file)[0] + "_clean.csv"
        emails_found = {}

        # Read the original file and count the results
        with open(output_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                line_elements = line.split(": ")
                if len(line_elements) >= 2:
                    email = line_elements[1]
                    if email not in emails_found:
                        emails_found[email] = {'found_times': 1, 'file_counts': {}}
                    else:
                        emails_found[email]['found_times'] += 1

                    file_name = line_elements[0]
                    if file_name not in emails_found[email]['file_counts']:
                        emails_found[email]['file_counts'][file_name] = 1
                    else:
                        emails_found[email]['file_counts'][file_name] += 1

        # Write the clean CSV file with the collected information
        with open(cleaned_output_file, 'w', newline='', encoding='utf-8') as cleaned_output:
            writer = csv.writer(cleaned_output)
            writer.writerow(["Email", "Found Total Times", "File Counts"])

            for email, data in emails_found.items():
                file_counts = '; '.join([f"{file_name}: {count}" for file_name, count in data['file_counts'].items()])
                writer.writerow([email, data['found_times'], file_counts])

        print(f"Clean CSV file has been generated: {cleaned_output_file}")

    # Ask if cleaning the results and generating the clean output file is desired
    if input("Do you want to clean the results and generate the clean output file? (y/n): ").lower() == "y":
        cleaned_output_file = os.path.splitext(output_file)[0] + "_clean.txt"
        emails_found = {}

        # Read the original file and count the results
        with open(output_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                line_elements = line.split(": ")
                if len(line_elements) >= 2:
                    email = line_elements[1]
                    if email not in emails_found:
                        emails_found[email] = {'found_times': 1, 'file_counts': {}}
                    else:
                        emails_found[email]['found_times'] += 1

                    file_name = line_elements[0]
                    if file_name not in emails_found[email]['file_counts']:
                        emails_found[email]['file_counts'][file_name] = 1
                    else:
                        emails_found[email]['file_counts'][file_name] += 1

        # Write the clean output file with the collected information
        with open(cleaned_output_file, 'w', encoding='utf-8') as cleaned_output:
            for email, data in emails_found.items():
                cleaned_output.write(f'{email}\n')
                cleaned_output.write(f'Found total times: {data["found_times"]}\n')
                for file_name, count in data['file_counts'].items():
                    cleaned_output.write(f'Times in {file_name}: {count}\n')

        print(f"Clean output file has been generated: {cleaned_output_file}")
