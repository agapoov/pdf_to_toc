import json
import fitz


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


pdf_file_path = input("[+] Enter the path to the PDF file: ").strip()

result = pdf_to_toc(pdf_file_path)

output_file = "structure.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)  # Save to 'structure.json'

print(f"[+] Successfully saved to {output_file}")
