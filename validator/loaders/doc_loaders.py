from langchain.document_loaders import UnstructuredPDFLoader
from PIL import Image
import pytesseract

async def load_pdf(path: str):
    loader = UnstructuredPDFLoader(path)
    docs = loader.load()
    return docs  # list of Document(page_content=...)

async def load_image(path: str):
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    from langchain.schema import Document
    return [Document(page_content=text)]
