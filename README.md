# document-processing-system
Document processing system should securely process and stores documents and provide a user interface for interacting with these documents.

## General system components
The system consists of major five components interacting together:
* **Document processing backend** should securely process and store documents.
* **External API** should be integrated with document processing backend, provides additional functionalities for documents. 
* **Postgres database** should securely store and handle relationships between data of users, documents metadata, and audit trail.  
* **Docker volume** should be the storage file system on which the files are stored and encrypted.
* **Client-side application**: should be an interface for users and admins to interact with the system. 

## System architecture

## Database UML diagram

<img src="./pictures/db_uml.svg">
