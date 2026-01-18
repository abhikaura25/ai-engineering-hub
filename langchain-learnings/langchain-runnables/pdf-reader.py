from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

### load the doc ####
script_dir = Path(__file__).parent
loader = TextLoader(script_dir / "docs.txt")
documents = loader.load()

### Split the text into smaller chunks ####
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

docs = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())

retriever = vectorstore.as_retriever()

query = "What are key takeaways from this document?"

retrieved_docs = retriever.invoke(query)

retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

llm = OpenAI(model="gpt-3.5-turbo-instruct")

prompt = f"Based on the following text, answer the question: {query} \n\n {retrieved_text}"
answer = llm.invoke(prompt)

print('Answer:', answer)
