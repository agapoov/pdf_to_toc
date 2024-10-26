import json
import fitz
import os


class Section:
    """Represents a section with a title and subsections."""
    def __init__(self, title):
        """Init a section with title and subsections."""
        self.title = title
        self.subsections = {}

    def add_subsection(self, key, subsection):
        """Add a subsection to the section."""
        self.subsections[key] = subsection

    def render_to_dict(self, level=1):
        """Convert the section to dict with different keys for sections and subsections."""
        result = {
            "title": self.title,
        }

        # Determine the appropriate key based on the level
        key = "sections" if level == 1 else "subsections"
        result[key] = {key: subsection.render_to_dict(level + 1) for key, subsection in self.subsections.items()}

        return result


def pdf_to_toc(pdf_file_path):
    """Extract the contents from the PDF file."""
    document = fitz.open(pdf_file_path)
    toc = document.get_toc()  # (level, title, page_number)
    document.close()

    sections = {}
    stack = []
    index_stack = []

    for level, title, page in toc:
        if "Глава" in title:
            continue

        while stack and stack[-1][1] >= level:
            stack.pop()
            index_stack.pop()

        # Create a new section
        section = Section(title)

        if level == 1:
            index_key = str(len(sections) + 1)
            sections[index_key] = section
        else:
            parent_index = index_stack[-1]
            index_key = f"{parent_index}.{len(stack[-1][0].subsections) + 1}" # generate
            stack[-1][0].add_subsection(index_key, section)

        stack.append((section, level))
        index_stack.append(index_key)

    return {"sections": {key: section.render_to_dict() for key, section in sections.items()}}


def save_to_file(pdf_file_path, output_path):
    """Save in JSON format."""
    result = pdf_to_toc(pdf_file_path)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)
    print(f"[+] TOC structure saved to {output_path}")


if __name__ == "__main__":
    try:
        input_pdf_file_path = input("[+] Enter the PDF file path: ").strip()
        input_output_path = input("[+] Enter the output JSON file path (default: structure.json): ").strip() or 'structure.json'
    except ValueError as err:
        print(f"[-] Error parsing input: {err}")
    else:
        if not input_pdf_file_path or not os.path.exists(input_pdf_file_path):
            print(f'[-] Error: File with path "{input_pdf_file_path}" does not exist. Try removing quotes in the file '
                  f'path')
        elif not input_pdf_file_path.lower().endswith('.pdf'):
            print('[-] Error: The specified file is not a PDF.')
        else:
            try:
                save_to_file(input_pdf_file_path, input_output_path)
            except IOError as io_error:
                print(f"[-] Error saving TOC: {io_error}")
