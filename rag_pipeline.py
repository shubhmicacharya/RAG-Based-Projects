import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage
from summarize_news import summarize
from fetch_news import get_news
from langchain.chains import RetrievalQA

load_dotenv()

FetchNewsRunnable = RunnableLambda(lambda topic: get_news(topic, num_articles=5))

SummarizeRunnable = RunnableLambda(lambda articles: [
    summarize(
        (a.get("title") or "") + ". " + (a.get("description") or "") + " " + (a.get("content") or "")
    ) for a in articles
])

NewsPipeline = RunnableSequence(FetchNewsRunnable | SummarizeRunnable)

embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

def store_summaries(summaries, topic):
    docs = [f"{summary}\nTopic: {topic}" for summary in summaries]
    metadatas = [{"topic": topic} for _ in summaries]
    vectorstore.add_texts(docs, metadatas=metadatas)
    print(f"✅ Stored {len(summaries)} summaries in vector store.")

def get_qa_chain():
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True  # Optional: lets you inspect source docs
    )
