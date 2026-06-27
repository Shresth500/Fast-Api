from abc import ABC, abstractmethod
from fastapi import UploadFile


class ContentExtractor(ABC):

    @abstractmethod
    def extract_content_from_pdf(
        self,
        file_path:str
    ) -> str:
        
        pass

    def save_content_from_pdf(self,user_id:int,
                                 chat_window_id:int,
                                 file: UploadFile):
        pass