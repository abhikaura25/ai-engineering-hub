from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
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

def get_context(retrieved_docs):
    return "\n\n".join(doc.page_content for doc in retrieved_docs)

parallel_chain = RunnableParallel({
    'context': retriever | RunnableLambda(get_context),
    'question': RunnablePassthrough()
})

parser = StrOutputParser()

main_chain = parallel_chain | prompt | chat_model | parser

result = main_chain.invoke('Can you summarize the video')

print(result)

