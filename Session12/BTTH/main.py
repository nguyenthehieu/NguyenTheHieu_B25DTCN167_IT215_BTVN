from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, DocumentModel

app = FastAPI()

class DocumentCreate(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str

def get_documents_service(db: Session):
    return db.query(DocumentModel).all()

def create_document_service(db: Session, document: DocumentCreate):
    new_document = DocumentModel(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

def delete_document_service(db: Session, document_id: int):
    document = db.query(DocumentModel).filter( DocumentModel.id == document_id).first()

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài liệu."
        )

    result = {
        "id": document.id,
        "title": document.title,
        "subject": document.subject,
        "document_type": document.document_type,
        "file_url": document.file_url
    }

    db.delete(document)
    db.commit()
    return result

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    documents = get_documents_service(db)
    return documents

@app.post("/documents")
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_document = create_document_service(db, document)
    return {
        "message": "Thêm tài liệu thành công.",
        "data": new_document
    }

@app.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = delete_document_service(db, document_id)
    return {
        "message": "Xóa tài liệu thành công.",
        "data": document
    }