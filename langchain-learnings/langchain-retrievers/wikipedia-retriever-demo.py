from dotenv import load_dotenv
from langchain_community.retrievers import WikipediaRetriever

load_dotenv()

wikipedia_retriever = WikipediaRetriever(
    top_k_results=2,
    lang="en"
)

query = "India and pakistan cricket match history in detail."

docs = wikipedia_retriever.invoke(query)

for i, doc in enumerate(docs):
    print(f"\n--- Result {i+1} ---")
    print(f"Content:\n{doc.page_content}...")  # truncate for display