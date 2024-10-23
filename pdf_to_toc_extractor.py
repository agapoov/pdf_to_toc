import json
import fitz
import os

class Section:
    """Represents a section with a title, page, and subdivisions."""
    def __init__(self, title, page):
        """init a section with title, page and subdivisions"""
        self.title = title
        self.page = page
        self.subdivisions = []

    def add_subdivision(self, subdivision):
        """Add subdivision to section"""
        self.subdivisions.append(subdivision)

    def render_to_dict(self):
        """Convert the section to dict"""
        return {
            "title": self.title,
            "page": self.page,
            "subdivisions": [sub.render_to_dict() for sub in self.subdivisions],
        }


def pdf_to_toc(pdf_file_path):
    """Extract the contents from pdf file"""
    document = fitz.open(pdf_file_path)
    toc = document.get_toc()  # (level, title, page_number)
    document.close()

    main_section = Section("Main_Section", 0)  # Creating the root of the structure

    stack = [
        (main_section, 0)
    ]  # the stack will be replenished with elements as the document is processed

    for level, title, page in toc:
        while stack[-1][1] >= level:
            stack.pop()

        section = Section(title, page)
        stack[-1][0].add_subdivision(section)
        stack.append((section, level))

    return main_section.render_to_dict()



def save_to_file(pdf_file_path, output_path):
    """Save in json format"""
    result = pdf_to_toc(pdf_file_path)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    print(f"[+] TOC structure saved to {output_path}")

if __name__ == "__main__":
    pdf_file_path = input("[+] Enter the PDF file path: ").strip()
    output_path = input("[+] Enter the output JSON file path(default: structure.json): ").strip()
    if not output_path:
        output_path = 'structure.json'
    
    if not os.path.isfile(pdf_file_path):
        print(f'[-] Error: File with path "{pdf_file_path}" does not exist. Try removing quotes in the file path')
    else:
        save_to_file(pdf_file_path, output_path)
