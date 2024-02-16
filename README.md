# MetaHunter Toolkit
MetaHunter is a collection of Python scripts designed to facilitate various reconnaissance tasks, including PDF downloading, metadata extraction, and email harvesting.

### Tools Included
PDF Downloader (pdfdownloader.py):

Downloads PDF files from a list of URLs.
Handles error logging for failed downloads.

    sudo python3 pdfdownloader.py -l <url_list_file> -d <destination_folder> -e <error_log_file>

  
  Options:
  
    -l, --url-list: Path to the file containing the list of URLs.
    
    -d, --destination-folder: Destination folder to save downloaded PDF files.
    
    -e, --error-log-file: Path to the file for error logging.

### MetaExtractor (metaxtractor.py):

Extracts metadata from PDF files.
Supports batch processing of multiple PDFs.

    sudo python3 metaxtractor.py -f <folder_path>

  Options:
  
    -f, --folder-path: Path to the folder containing PDF files for metadata extraction.

### Email Hunter (emailhunter.py):

Extracts email addresses from files within a specified folder.
Handles different file formats, including PDF, DOC, and TXT.

    sudo python3 emailhunter.py -o <output_file>


  Options:
    
    -o, --output-file: Path to the output file for storing extracted email addresses.


## Requirements
Before using MetaHunter, ensure you have the following dependencies installed:

    requests==2.26.0: HTTP library for making requests in Python.

### Installation

Clone the repository and install dependencies with the following one-liner:

```bash
sudo git clone https://github.com/Acorzo1983/Metahunter.git && cd metahunter && chmod +x *.py && pip install -r requirements.txt
```

# MetaHunter Usage Examples

Here are some usage examples demonstrating how to use the MetaHunter toolkit for various reconnaissance tasks.

## Example 1: Download PDF Files and Extract Metadata

1. Download PDF files from a list of URLs and extract metadata:

```bash
python pdfdownloader.py -l urls.txt -d pdfs -e errors.txt
```

```bash
python metaxtractor.py -f pdfs
```

## Example 2: Harvest Email Addresses from Public Documents

  Use Metagoofil to gather metadata from public documents:

```bash
metagoofil -d example.com -t all -l 100 -w -f metago_files.txt -o metago_files -tor
```
  
Extract email addresses from the collected metadata:

```bash
python emailhunter.py -f metago_files -o emails.txt
```

Feel free to explore more usage scenarios and customize the commands according to your needs!


This some example commands demonstrating how to use the MetaHunter toolkit for different reconnaissance tasks. You can add more examples or customize the existing ones based on specific use cases. Let me know if you need any further assistance!
