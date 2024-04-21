from __future__ import annotations

import os
from pathlib import Path

from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import PDFReader
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.chroma import get_chroma_client
from app.common import Collections, get_embed_model
from app.log import get_logger

__all__ = ["ingest"]
logger = get_logger("ingest")


def ingest() -> None:
    logger.info("Starting..")

    client = get_chroma_client()

    collection = client.get_or_create_collection(Collections.Books.value)

    store = ChromaVectorStore(chroma_collection=collection)

    # considering we have only 1 book we are counting the no. of records
    # in case of more than 1 book, check for book_id here to skip ingestion
    # existing_metadata = collection.peek(limit=1) # will give a peek on the
    # data content with book_id=1818
    # - Do not ingest the same book more than once if re-run
    if collection.count() > 0:
        logger.info("Metadata with book_id 1818 already exists. Skipping ingestion.")
        return

    # load document
    loader = PDFReader()
    documents = loader.load_data(file=Path("./books/frankenstein.pdf"))

    # embeddings
    embedding_function = get_embed_model()

    # - create a vector store index from the "store", use get_embed_model() for the embed model
    index = VectorStoreIndex.from_vector_store(vector_store=store, embed_model=get_embed_model)
    index.storage_context.persist('./data')

    # text chunking strategy
    # - Utilize a chunking strategy appropriate for a book
    node_parser = SentenceSplitter(chunk_size=300, chunk_overlap=10)
    nodes = node_parser.get_nodes_from_documents(documents, show_progress=True)

    # book details
    # - The frankenstein book should be identified by a "book_id" of 1818
    book_id = 0
    book_details = {"frankenstein.pdf": 1818,}

    # Convert chunks to vector representations and store in Chroma DB
    documents_list = []
    embeddings_list = []
    ids_list = []
    metadata_list = []

    # TASK: Vectorize ./books/frankenstein.pdf into the chromadb collection
    for file_name in os.listdir('./books'):
        if file_name.endswith('.pdf'):            
            book_id = str(book_details.get(file_name))
            
            for i, chunk in enumerate(nodes):
                vector = embedding_function.get_query_embedding(chunk.get_content())   
                embeddings_list.append(vector)
                documents_list.append(chunk.get_content())
                ids_list.append(f"{file_name}_{i}")
                metadata_list.append({"book_id":book_id})

            collection.add(
                    embeddings=embeddings_list,
                    documents=documents_list,
                    ids=ids_list,
                    metadatas=metadata_list
            )
   
    logger.info("Complete.")
    
