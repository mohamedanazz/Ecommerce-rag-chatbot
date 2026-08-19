import os
from pypdf import PdfReader

def read_pdf(pdf_path: object) -> list[str]:
    """

    :rtype: list[str]
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")

    reader = PdfReader(pdf_path)
    pages = [page.extract_text() for page in reader.pages]
    return pages