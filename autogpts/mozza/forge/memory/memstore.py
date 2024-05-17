import abc

class MemStore(abc.ABC):
    @abc.abstractmethod
    def __init__(self, store_path: str):
        pass

    @abc.abstractmethod
    def add_task_memory(self, task_id: str, document: str, metadatas: dict) -> None:
        self.add(collection_name=task_id, document=document, metadatas=metadatas)

    @abc.abstractmethod
    def query_task_memory(self, task_id: str, query: str, filters: dict = None, document_search: dict = None) -> dict:
        return self.query(collection_name=task_id, query=query, filters=filters, document_search=document_search)

    @abc.abstractmethod
    def get_task_memory(self, task_id: str, doc_ids: list = None, filters: dict = None) -> dict:
        return self.get(collection_name=task_id, doc_ids=doc_ids, filters=filters)

    @abc.abstractmethod
    def update_task_memory(self, task_id: str, doc_ids: list, documents: list, metadatas: list):
        self.update(collection_name=task_id, doc_ids=doc_ids, documents=documents, metadatas=metadatas)

    @abc.abstractmethod
    def delete_task_memory(self, task_id: str, doc_id: str):
        self.delete(collection_name=task_id, doc_id=doc_id)

    @abc.abstractmethod
    def add(self, collection_name: str, document: str, metadatas: dict) -> None:
        pass

    @abc.abstractmethod
    def query(self, collection_name: str, query: str, filters: dict = None, document_search: dict = None) -> dict:
        pass

    @abc.abstractmethod
    def get(self, collection_name: str, doc_ids: list = None, filters: dict = None) -> dict:
        pass

    @abc.abstractmethod
    def update(self, collection_name: str, doc_ids: list, documents: list, metadatas: list):
        pass

    @abc.abstractmethod
    def delete(self, collection_name: str, doc_id: str):
        pass
