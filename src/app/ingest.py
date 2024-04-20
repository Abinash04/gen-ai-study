from __future__ import annotations

from pathlib import Path

from chromadb import IDs
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
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
    # loader = PDFReader()
    # documents = loader.load_data(file=Path("./books/frankenstein.pdf"))
    # for document in documents:
    #     print(f"Document ID: {document.id_}")
    #     for attr, value in document.__dict__.items():
    #         if attr != 'id_':  # Exclude the 'id_' attribute from printing
    #             print(f"{attr}: {value}")
    #     print()


    client = get_chroma_client()
   

    # import sys
    # sys.exit(0)

    collection = client.get_or_create_collection(Collections.Books.value)

    store = ChromaVectorStore(chroma_collection=collection)

    # TASK: Vectorize ./books/frankenstein.pdf into the chromadb collection

    # load documents
    # documents = SimpleDirectoryReader("./books/").load_data()

    loader = PDFReader()
    documents = loader.load_data(file=Path("./books/frankenstein.pdf"))

    books_dict = {"book_id":1818}

    # print("documents---->", documents)

    # parse into nodes
    node_parser = SentenceSplitter(chunk_size=256)
    nodes = node_parser.get_nodes_from_documents(documents)


    index = VectorStoreIndex.from_vector_store(vector_store=store, embed_model=get_embed_model, book_id=1818)
    # index1 = VectorStoreIndex.from_documents(documents, book_id=1818)
    logger.info(f"index:{index}")


    # - create a vector store index from the "store", use get_embed_model() for the embed model
    # - The frankenstein book should be identified by a "book_id" of 1818
    # - Utilize a chunking strategy appropriate for a book
    # - Do not ingest the same book more than once if re-run

    # db = Chroma.from_documents(docs0, embeddings, ids=ids, persist_directory='db')


    logger.info("Complete.")
