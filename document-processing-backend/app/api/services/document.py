from collections import defaultdict
from io import BytesIO
from pathlib import Path
import re
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from api.schemas.document import DocumentMetadataResponse
from db.models.document_metadata import DocumentMetadata
from db.models.document_user_permissions import DocumentUserPermission
from abc import ABC, abstractmethod
import PyPDF2
from core.config import Config

class DocumentProcessor(ABC):
    @abstractmethod
    def process(self, document_data: UploadFile) -> defaultdict[str, int]:
        pass
    
    def _extract_keywords(self, content: str):
        stop_words = Config.STOP_WORDS
        result: defaultdict[str, int] = defaultdict(int)
        words = re.findall(r'\b\w+\b', content.lower())
        for word in words:
            if word not in stop_words:
                result[word] += 1
        return result
    
class PDFProcessor(DocumentProcessor):
    async def process(self, document_data: UploadFile) -> defaultdict[str, int]:
       content = await self._extract_content(document_data)
       key_words = self._extract_keywords(content)
       return key_words
    
    async def _extract_content(self, document_data: UploadFile):
        pdf_bytes = await document_data.read()
        pdf_stream = BytesIO(pdf_bytes)
        content_list = [] # To be same as StringBuilder in java for better performance instead of reassign string
        reader = PyPDF2.PdfReader(pdf_stream)
        for page in reader.pages:
           content_list.append(page.extract_text().replace("\n", ""))
        content = "".join(content_list)
        return content
        
class TXTProcessor(DocumentProcessor):
    async def process(self, document_data: UploadFile):
        content = await self._extract_content(document_data)
        key_words = self._extract_keywords(content)
        return key_words
    
    async def _extract_content(self, document_data: UploadFile):
        txt_bytes = await document_data.read()
        txt_content = txt_bytes.decode("utf-8")
        content_list = [] # To be same as StringBuilder in java for better performance instead of reassign string
        for line in txt_content:
            content_list.append(line.strip())
        return "".join(content_list)
        
class DocumentFactory:
    
    document_processors = {
        "pdf": PDFProcessor,
        "txt": TXTProcessor
    }
    
    @staticmethod
    def get_document_processor(document_type: str) -> DocumentProcessor:
        processor_class = DocumentFactory.document_processors.get(document_type)
        if not processor_class:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported document type"
            )
        return processor_class()
    


class DocumentService:
    def __init__(self, db: Session, document_factory: DocumentFactory):
        self.db = db
        self.document_factory = document_factory
    
    async def process_document(self, document_data: UploadFile) -> DocumentMetadataResponse:
        document_type = self._map_MIME_type(document_data.content_type)
        document_prcessor = self.document_factory.get_document_processor(document_type)
        processed_document = await document_prcessor.process(document_data)
        db_document_metadata = DocumentMetadata(
            document_type=document_type,
            size=document_data.size,
            mime_type=document_data.content_type,
            keywords=processed_document,
            filename=document_data.filename,
            author_id=28,
            processing_status="Completed"
        )
        self.db.add(db_document_metadata)
        self.db.commit()
        self.db.refresh(db_document_metadata)
        await self._save_document_in_volume(document_data)
        return db_document_metadata
    
    def get_document_metadata_by_document_id(self, document_id: int):
        result: DocumentMetadata = self.db.query(DocumentMetadata).filter(DocumentMetadata.id == document_id).first()
        if(not result):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        return result
    
    def get_document_by_author_id(self, author_id: int):
        return self.db.query(DocumentMetadata).filter(DocumentMetadata.author_id == author_id).all()
    
    def stream_document(self, document_id: int):
        document_metadata = self.get_document_metadata_by_document_id(document_id)
        volume_path = Path(Config.VOLUME_PATH)
        document_name = document_metadata.filename
        document_path = Path(volume_path / document_name)
        document_output = BytesIO()
        with open(document_path, "rb") as document_to_read:
            document_output.write(document_to_read.read())
        document_output.seek(0)
        return StreamingResponse(document_output, media_type=f"{document_metadata.mime_type}", headers={
        "Content-Disposition": f'attachment; filename="{document_metadata.filename}"'})
    
    def search_by_keywords(self, keywords: list[str]):
        query = (
        self.db.query(DocumentMetadata)
        .filter(or_(
            *[
                DocumentMetadata.keywords.has_key(keyword)
                for keyword in keywords
            ]
        )))

        results = query.all()
        return results
            
    # Private helper functions
    def _map_MIME_type(self, type: str) -> str:
        MIME_types = {
            "text/plain": "txt",
            "application/pdf": "pdf"
        }
        return MIME_types.get(type, "unknown")
        
    async def _save_document_in_volume(self, document_data: UploadFile):
        await document_data.seek(0) # to ensure the pointer is reset        
        volume_path = Path(Config.VOLUME_PATH)
        file_path = volume_path / document_data.filename
        file_content = await document_data.read()
        with open(file_path, "wb") as document_to_write:
            document_to_write.write(file_content)
        return {"filename": document_data.filename, "path": str(file_path)}
        
        
    
    