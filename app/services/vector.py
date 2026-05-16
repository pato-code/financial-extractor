from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter 


class VectorService:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.vector_store = Chroma(collection_name=collection_name)
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    def add_documents(self, documents: list[Document], chunk_size: int = 2500, overlap: int = 300):
        processed_documents: list[Document] = []
        for doc in documents:
            
            chunks = self.splitter.split_text(doc.page_content)

            for chunk_index, chunk in enumerate(chunks):
                metadata = dict(doc.metadata or {})
                metadata["chunk_index"] = chunk_index
                processed_documents.append(Document(page_content=chunk, metadata=metadata))

        self.vector_store.add_documents(processed_documents)

    def _chunk_text(self, text: str, chunk_size: int = 2500, overlap: int = 300) -> list[str]:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        chunks: list[str] = []
        start = 0
        text_length = len(text)
        while start < text_length:
            end = start + chunk_size
            chunks.append(text[start:end])
            if end >= text_length:
                break
            start += chunk_size - overlap

        return chunks

    def query(self, query: str, top_k: int = 15) -> list[Document]:
        return self.vector_store.similarity_search(query, k=top_k)