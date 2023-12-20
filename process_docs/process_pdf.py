from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer


def process_pdf(path_file):
    text_pages = {}
    for i, page_layout in enumerate(extract_pages(path_file)):
        text_pages[i + 1] = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_pages[i + 1] += element.get_text()
    return text_pages
