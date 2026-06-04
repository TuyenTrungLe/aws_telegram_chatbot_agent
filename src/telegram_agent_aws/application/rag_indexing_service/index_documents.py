from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from telegram_agent_aws.config import settings
from telegram_agent_aws.infrastructure.clients.qdrant import get_qdrant_client


def generate_split_documents():
    loader = PyPDFLoader("./data/Tu_full_biography.pdf")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    docs = loader.load()
    all_splits = text_splitter.split_documents(docs)

    return all_splits


def index_documents():
    all_splits = generate_split_documents()
    embeddings = OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        tiktoken_enabled=False,
        check_embedding_ctx_length=False,
    )

    QdrantVectorStore.from_documents(
        documents=all_splits,
        embedding=embeddings,
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        collection_name="telegram_agent_aws_collection",
        timeout=120,
        batch_size=4,
    )

    logger.info("Documents indexed successfully.")
