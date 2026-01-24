from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

model = ChatOpenAI()
embedding_model = OpenAIEmbeddings()

all_docs = [
    Document(page_content="Regular walking boosts heart health and can reduce symptoms of depression.", metadata={"source": "H1"}),
    Document(page_content="Consuming leafy greens and fruits helps detox the body and improve longevity.", metadata={"source": "H2"}),
    Document(page_content="Deep sleep is crucial for cellular repair and emotional regulation.", metadata={"source": "H3"}),
    Document(page_content="Mindfulness and controlled breathing lower cortisol and improve mental clarity.", metadata={"source": "H4"}),
    Document(page_content="Drinking sufficient water throughout the day helps maintain metabolism and energy.", metadata={"source": "H5"}),
    Document(page_content="The solar energy system in modern homes helps balance electricity demand.", metadata={"source": "I1"}),
    Document(page_content="Python balances readability with power, making it a popular system design language.", metadata={"source": "I2"}),
    Document(page_content="Photosynthesis enables plants to produce energy by converting sunlight.", metadata={"source": "I3"}),
    Document(page_content="The 2022 FIFA World Cup was held in Qatar and drew global energy and excitement.", metadata={"source": "I4"}),
    Document(page_content="Black holes bend spacetime and store immense gravitational energy.", metadata={"source": "I5"}),
]

vector_store = Chroma.from_documents(
    documents=all_docs,
    embedding=embedding_model,
    collection_name='multi-query-store'
)

base_retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# Multi-query prompt to generate alternative questions
multi_query_prompt = ChatPromptTemplate.from_template(
    """You are an AI assistant that generates multiple search queries based on a single input query.

Generate 3 different versions of the given question to retrieve relevant documents from a vector database.
Provide these alternative questions separated by newlines.

Original question: {question}

Alternative questions:"""
)

# Chain to generate multiple queries
query_generator = multi_query_prompt | model | StrOutputParser()


def multi_query_retrieve(question: str) -> list[Document]:
    """Generate multiple queries and retrieve unique documents."""
    # Generate alternative queries
    response = query_generator.invoke({"question": question})
    queries = [question] + [q.strip() for q in response.strip().split("\n") if q.strip()]

    # Retrieve documents for each query
    all_docs = []
    seen_contents = set()

    for query in queries:
        docs = base_retriever.invoke(query)
        for doc in docs:
            if doc.page_content not in seen_contents:
                seen_contents.add(doc.page_content)
                all_docs.append(doc)

    return all_docs


query = "How can I improve my health?"

print(f"Original query: {query}\n")
print("Generating alternative queries and retrieving documents...\n")

results = multi_query_retrieve(query)

for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)

