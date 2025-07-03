import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader
from langchain_community.document_loaders import TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_function import get_embedding_function
from langchain_chroma import Chroma

DATA_PATH = "data"
CHROMA_PATH = "chroma"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    args = parser.parse_args()
    
    if args.reset:
        print("Clearing database")
        clear_database()
    
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)
    print("Ingestion complete.")

def load_documents():
    """Load documents from PDF, DOCX, and TXT files"""
    documents = []
    
    # Load PDF files
    pdf_loader = PyPDFDirectoryLoader(DATA_PATH)
    pdf_documents = pdf_loader.load()
    documents.extend(pdf_documents)
    print(f"Loaded {len(pdf_documents)} PDF documents")
    
    # Load DOCX files
    docx_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.docx",
        loader_cls=Docx2txtLoader,
        show_progress=True
    )
    docx_documents = docx_loader.load()
    documents.extend(docx_documents)
    print(f"Loaded {len(docx_documents)} DOCX documents")
    
    # Load TXT files
    txt_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True
    )
    txt_documents = txt_loader.load()
    documents.extend(txt_documents)
    print(f"Loaded {len(txt_documents)} TXT documents")
    
    print(f"Total documents loaded: {len(documents)}")
    return documents

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    
    chunks_with_ids = calculate_chunk_ids(chunks)
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add.")

def calculate_chunk_ids(chunks):
    """Calculate unique IDs for chunks, handling different file types"""
    last_page_id = None
    current_chunk_index = 0
    
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        
        # For TXT and DOCX files, page might be None
        if page is None:
            page = 0
        
        current_page_id = f"{source}:{page}"
        
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        chunk.metadata["id"] = chunk_id
    
    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
