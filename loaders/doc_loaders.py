from langchain_community.document_loaders import UnstructuredPDFLoader
from PIL import Image

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

async def load_pdf(path: str):
    loader = UnstructuredPDFLoader(path)
    return loader.load()  # list of Document(page_content=...)

async def load_image(path: str):
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    from langchain.schema import Document
    return [Document(page_content=text)]

async def load_documents(uris:list[str]):
    docs = []
    for uri in uris:
        if uri.endswith(".pdf"):
            docs.extend(await load_pdf(uri))
        elif uri.endswith(tuple([".jpg", ".jpeg", ".png"])):
            docs.extend(await load_image(uri))
    return docs
