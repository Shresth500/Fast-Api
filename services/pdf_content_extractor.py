import os
import shutil

from fastapi import UploadFile
from pathlib import Path
from services.extractor_class import ContentExtractor
from langchain_community.document_loaders import PyPDFLoader


BASE_DIR = Path(__file__).parent.parent

class PdfContentExtractor(ContentExtractor):
    def __init__(self):
        pass
    
    
    def extract_content_from_pdf(self,
                                 file_path:str):
        # file_path = f"{BASE_DIR}/pdf/{str(user_id)}/{str(chat_window_id)}/{file.filename}"
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        content = "\n".join(
            document.page_content
            for document in documents
        )

        return content
        

    def save_content_from_pdf(self,user_id:int,
                                 chat_window_id:int,
                                 file: UploadFile):
        path = f"{BASE_DIR}/pdf/{str(user_id)}/{str(chat_window_id)}"
        print(path)
        os.makedirs(path, exist_ok=True)

        file_path = os.path.join(path, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path