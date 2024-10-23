# PDF TOC Extractor

A simple Python script to extract the table of contents (TOC) from PDF files and save it in JSON format.

## Requirements

- Python 3.8 or higher
- PyMuPDF library

## Installation

1. Clone or download this repository.
   ```bash
   git clone https://github.com/agapoov/pdf_to_toc.git
   ```
2. Navigate to the project directory.
3. Install the required library:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your PDF file in the same directory as the script or provide the full path to the PDF file.
2. Open your terminal or command prompt.
3. Navigate to the project directory:

   ```bash
   cd /path/to/your/project
   ```

4. Create virtual env:
   ```bash
   python -m venv venv
   ```
5. Run project:
   ```bash
    python pdf_to_toc_extractor.py
   ```
6. Follow the prompts to enter the PDF file path and the output JSON file path (default: `structure.json`).

## Example

```
[+] Enter the PDF file path: sample.pdf
[+] Enter the output JSON file path: my_toc.json
[+] TOC structure saved to my_toc.json
```

## License

None
