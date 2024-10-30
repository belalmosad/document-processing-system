class AdditionalMetadataService:
    def __init__(self):
        pass
    
    def get_additional_metadata(self, document_id):
        return {
            "document_id": document_id,
            "additional_data": f"Additional data for document id = {document_id}"
        }