import hashlib
import chromadb
from chromadb.config import Settings
from .memstore import MemStore

class ChromaMemStore(MemStore):
    def __init__(self, store_path: str):
        self.client = chromadb.PersistentClient(
            path=store_path, settings=Settings(anonymized_telemetry=False)
        )

    def add(self, collection_name: str, document: str, metadatas: dict) -> None:
        doc_id = hashlib.sha256(document.encode()).hexdigest()[:20]
        collection = self.client.get_or_create_collection(collection_name)
        collection.add(documents=[document], metadatas=[metadatas], ids=[doc_id])

    def query(self, collection_name: str, query: str, filters: dict = None, document_search: dict = None) -> dict:
        collection = self.client.get_or_create_collection(collection_name)
        kwargs = {"query_texts": [query], "n_results": 10}
        if filters:
            kwargs["where"] = filters
        if document_search:
            kwargs["where_document"] = document_search
        return collection.query(**kwargs)

    def get(self, collection_name: str, doc_ids: list = None, filters: dict = None) -> dict:
        collection = self.client.get_or_create_collection(collection_name)
        kwargs = {}
        if doc_ids:
            kwargs["ids"] = doc_ids
        if filters:
            kwargs["where"] = filters
        return collection.get(**kwargs)

    def update(self, collection_name: str, doc_ids: list, documents: list, metadatas: list):
        collection = self.client.get_or_create_collection(collection_name)
        collection.update(ids=doc_ids, documents=documents, metadatas=metadatas)

    def delete(self, collection_name: str, doc_id: str):
        collection = self.client.get_or_create_collection(collection_name)
        collection.delete(ids=[doc_id])
