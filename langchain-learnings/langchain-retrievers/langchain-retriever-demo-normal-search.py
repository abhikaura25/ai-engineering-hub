from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma


load_dotenv()

documents = [
    Document(page_content="LangChain helps developers build LLM applications easily."),
    Document(page_content="Chroma is a vector database optimized for LLM-based search."),
    Document(page_content="Embeddings convert text into high-dimensional vectors."),
    Document(page_content="OpenAI provides powerful embedding models."),
]

embedding_model = OpenAIEmbeddings()

vector_store = Chroma.from_documents(documents=documents,
                                     embedding=embedding_model,
                                     collection_name="retriever-demo-db")

vector_store_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

query = "What is Langchain"

results=vector_store_retriever.invoke(query)

for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)

results_directly_from_vector_store = vector_store.similarity_search(query, k=2)

for i, doc in enumerate(results_directly_from_vector_store):
    print(f"\n--- Direct from Store Result {i+1} ---")
    print(doc.page_content)