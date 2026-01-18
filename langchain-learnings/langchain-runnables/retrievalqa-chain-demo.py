from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI
from dotenv import load_dotenv
from langchain_classic.chains import RetrievalQA

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

llm = OpenAI(model="gpt-3.5-turbo-instruct")

qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

query = "What are key takeaways from the document?"

answer = qa_chain.invoke({"query": query})

print(answer["result"])
