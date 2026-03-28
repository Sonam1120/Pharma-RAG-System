from sqlalchemy import Column, String, Integer, Date, Text
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    title = Column(String)
    module = Column(String)
    submodule = Column(String)
    version = Column(Integer)
    status = Column(String)  
    effective_date = Column(Date)
    content = Column(Text)


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(String, primary_key=True)
    document_id = Column(String)
    text = Column(Text)


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text)
    retrieved_docs = Column(Text)