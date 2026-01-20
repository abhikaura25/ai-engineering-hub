from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

script_dir = Path(__file__).parent
loader = PyPDFLoader(script_dir / 'dl-curriculum.pdf')

docs = loader.load()


splitter = CharacterTextSplitter(
    chunk_overlap=0,
    chunk_size=100,
    separator=''   
)

result = splitter.split_documents(docs)

print(result[0])


