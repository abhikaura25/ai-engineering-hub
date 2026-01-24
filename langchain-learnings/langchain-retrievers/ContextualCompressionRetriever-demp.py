from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

model = ChatOpenAI()
embedding_model = OpenAIEmbeddings()


docs = [
    Document(page_content=(
        """The Grand Canyon is one of the most visited natural wonders in the world.
        Photosynthesis is the process by which green plants convert sunlight into energy.
        Millions of tourists travel to see it every year. The rocks date back millions of years."""
    ), metadata={"source": "Doc1"}),

    Document(page_content=(
        """In medieval Europe, castles were built primarily for defense.
        The chlorophyll in plant cells captures sunlight during photosynthesis.
        Knights wore armor made of metal. Siege weapons were often used to breach castle walls."""
    ), metadata={"source": "Doc2"}),

    Document(page_content=(
        """Basketball was invented by Dr. James Naismith in the late 19th century.
        It was originally played with a soccer ball and peach baskets. NBA is now a global league."""
    ), metadata={"source": "Doc3"}),

    Document(page_content=(
        """The history of cinema began in the late 1800s. Silent films were the earliest form.
        Thomas Edison was among the pioneers. Photosynthesis does not occur in animal cells.
        Modern filmmaking involves complex CGI and sound design."""
    ), metadata={"source": "Doc4"})
]

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name="context-compression-collection"
)

base_retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}
)

# Compression prompt - extracts only relevant parts from documents
compression_prompt = ChatPromptTemplate.from_template(
    """Given the following question and document, extract only the parts of the document that are relevant to answering the question.
If no parts are relevant, respond with "NOT_RELEVANT".

Question: {question}

Document:
{document}

Relevant extracted content:"""
)

# Chain for compressing a single document
compressor_chain = compression_prompt | model | StrOutputParser()


def compress_documents(question: str, documents: list[Document]) -> list[Document]:
    """Compress documents by extracting only relevant content."""
    compressed_docs = []

    for doc in documents:
        compressed_content = compressor_chain.invoke({
            "question": question,
            "document": doc.page_content
        })

        # Skip if not relevant
        if compressed_content.strip().upper() != "NOT_RELEVANT":
            compressed_docs.append(
                Document(
                    page_content=compressed_content.strip(),
                    metadata=doc.metadata
                )
            )

    return compressed_docs


def contextual_compression_retrieve(question: str) -> list[Document]:
    """Retrieve and compress documents based on the question."""
    # First, retrieve documents
    retrieved_docs = base_retriever.invoke(question)
    print(f"Retrieved {len(retrieved_docs)} documents")

    # Then, compress them
    compressed_docs = compress_documents(question, retrieved_docs)
    print(f"After compression: {len(compressed_docs)} relevant documents\n")

    return compressed_docs


# Example usage
query = "What is photosynthesis?"

print(f"Query: {query}\n")
print("=" * 50)

results = contextual_compression_retrieve(query)

for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} (Source: {doc.metadata.get('source', 'N/A')}) ---")
    print(doc.page_content)

