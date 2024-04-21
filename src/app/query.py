from __future__ import annotations

from typing import TYPE_CHECKING

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

from app.chroma import get_chroma_client
from app.common import Collections, get_embed_model
from app.log import get_logger

if TYPE_CHECKING:
    from llama_index.core.base.response.schema import RESPONSE_TYPE
    from llama_index.core.schema import QueryType

__all__ = ["query"]

logger = get_logger("query")


def query(question: QueryType) -> RESPONSE_TYPE | None:
    logger.info("Starting..")

    client = get_chroma_client()
    collection = client.get_or_create_collection(Collections.Books.value)

    llama = Ollama(
        base_url="http://localhost:11434",
        model="llama2",
        request_timeout=300,
    )

    store = ChromaVectorStore(chroma_collection=collection)
    
    # build index
    index = VectorStoreIndex.from_vector_store(vector_store=store, embed_model=get_embed_model())

    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=2,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer(llm=llama)

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.9)],
    )

    # TASK: Query the vector database and use llama2 LLM to get an answer to the passed in question.
    # Return: The Response object from the query engine.
    query_engine = index.as_query_engine(llm=llama)
    response = query_engine.query(question)

    if response:
        return response

    return None
