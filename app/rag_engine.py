# app/rag_engine.py
from langchain_classic.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.language_models.llms import LLM

from app.llama_api import llama_generate
from app.utils.config import VECTOR_STORE_PATH, EMBEDDING_MODEL


class LlamaAPIWrapper(LLM):
    """Custom LLaMA API wrapper for LangChain."""

    def _call(self, prompt: str, stop=None) -> str:
        try:
            response = llama_generate(prompt)
            return response.strip()
        except Exception as e:
            return f"[Error calling LLaMA API: {e}]"

    @property
    def _identifying_params(self):
        return {"name_of_model": "LLaMA via API"}

    @property
    def _llm_type(self):
        return "llama_api"


def get_response(query: str) -> str:
    """Retrieve relevant context and generate answer using RAG + LLaMA."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embeddings
    )

    retriever = db.as_retriever(search_kwargs={"k": 3})
    llm = LlamaAPIWrapper()

    # RetrievalQA chain expects 'query' input
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    result = qa_chain.invoke({"query": query})
    # Sometimes the key is 'result', sometimes the chain returns raw text
    if isinstance(result, dict) and "result" in result:
        return result["result"]
    return str(result)
