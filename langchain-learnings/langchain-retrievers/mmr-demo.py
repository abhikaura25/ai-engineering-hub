from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

load_dotenv()

docs = [
    Document(page_content="LangChain makes it easy to work with LLMs."),
    Document(page_content="LangChain is used to build LLM based applications."),
    Document(page_content="Chroma is used to store and search document embeddings."),
    Document(page_content="Embeddings are vector representations of text."),
    Document(page_content="MMR helps you get diverse results when doing similarity search."),
    
    Document(page_content="LangChain supports Chroma, FAISS, Pinecone, and more."),
]

vector_store = Chroma.from_documents(documents=docs,
                                     embedding=OpenAIEmbeddings(),
                                     collection_name="mmr-demo")

retriever = vector_store.as_retriever(
    search_type = 'mmr',
    search_kwargs={"k": 3, "lambda_mult": 0.5})

query = "What is langchain ?"

results = retriever.invoke(query)

for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)