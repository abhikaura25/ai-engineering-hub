from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

video_id = "2fq9wYslV0A"

ytt_api = YouTubeTranscriptApi()

transcript_list = ytt_api.fetch(video_id=video_id, languages=["en"])

# Extract text from transcript snippets
transcript = " ".join(snippet.text for snippet in transcript_list)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.create_documents([transcript])

vector_store = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    collection_name="youtube-demo-collection"
)

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

#result = retriever.invoke('What is computer vision')



chat_model = ChatOpenAI()

prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables = ['context', 'question']
)


question = "is the topic of computer vision discussed in this video? if yes then what was discussed"

retrieved_docs = retriever.invoke(question)

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

chain = prompt | chat_model | StrOutputParser()

result = chain.invoke({"context": context_text, "question": question})

print(result)
