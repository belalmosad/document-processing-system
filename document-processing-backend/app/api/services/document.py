from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class DocumentProcessor(ABC):
    @abstractmethod
    def process(self):
        pass
    
class PDFProcessor(DocumentProcessor):
    def process(self):
       return "Processing pdf"
        
class TXTProcessor(DocumentProcessor):
    def process(self):
        return "Processing TXT"
        
class DocumentFactory:
    
    document_processors = {
        "pdf": PDFProcessor,
        "txt": TXTProcessor
    }
    
    @staticmethod
    def get_document_processor(document_type: str) -> DocumentProcessor:
        processor_class = DocumentFactory.document_processors.get(document_type)
        if not processor_class:
            raise ValueError("Unsupported document type")
        return processor_class()
    


class DocumentService:
    def __init__(self, db: Session, document_factory: DocumentFactory):
        self.db = db
        self.document_factory = document_factory
    
    def process_document(self, document_type: str, document_data):
        document_prcessor = self.document_factory.get_document_processor(document_type)
        return document_prcessor.process()
    
    