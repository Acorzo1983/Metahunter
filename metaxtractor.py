import os
import subprocess

def get_pdf_metadata(pdf_file):
    try:
        result = subprocess.run(['pdfinfo', pdf_file], capture_output=True, text=True)
        metadata = result.stdout
        return metadata
    except:
        return None

def extract_folder_metadata(source_folder):
    output_file = os.path.join(source_folder, 'metaxtractor_result.txt')

    num_files = 0
    num_pdf_files = 0

    with open(output_file, 'w') as file:
        for root, _, files in os.walk(source_folder):
            for pdf_file in files:
                pdf_path = os.path.join(root, pdf_file)
                file_name = os.path.basename(pdf_path)

                # Check if the file is a PDF
                if os.path.isfile(pdf_path) and (pdf_file.lower().endswith('.pdf') or subprocess.call(['file', pdf_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)):
                    metadata = get_pdf_metadata(pdf_path)

                    if metadata is not None:
                        file.write(f"{file_name}:\n{metadata}\n")
                    else:
                        file.write(f"{file_name}: Metadata extraction failed\n")

                    num_pdf_files += 1
                else:
                    file.write(f"{file_name}: Not a PDF file\n")

                num_files += 1

    final_result = f"""
    ----- Result -----

    Files found: {num_files}
    PDF files scanned: {num_pdf_files}
    Result file: {output_file}
    """

    print(final_result)

if __name__ == "__main__":
    import argparse

    # Command line arguments configuration
    parser = argparse.ArgumentParser(description="Script to extract metadata from PDF files in a folder")

    parser.add_argument("-f", "--folder", type=str, required=True, help="Path of the folder to scan")

    args = parser.parse_args()

    # Call the main function with the provided argument
    extract_folder_metadata(args.folder)
