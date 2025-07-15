from rag_pipeline import NewsPipeline, store_summaries, get_qa_chain
from send_to_WP import send_whatsapp_message
from format_msg import format_whatsapp_message

if __name__ == "__main__":
    topic = input("Enter a news topic to know about: ")
    print(f"Fetching news articles about: {topic}")

    summaries = NewsPipeline.invoke(topic)

    if summaries:
        store_summaries(summaries, topic)
        qa = get_qa_chain()
        question = f"What are the latest developments in {topic}?"
        answer = qa.invoke(question)

        print(f"\n🧠 Query: {answer.get('query', question)}")
        print(f"📌 Answer: {answer.get('result', 'No result found.')}")
        
        # Optional: show source docs
        if "source_documents" in answer:
            print("\n📚 Retrieved Documents:")
            for doc in answer["source_documents"]:
                print("—", doc.page_content[:200], "...\n")
                
        whatsapp_msg = format_whatsapp_message(topic, summaries)
        send_whatsapp_message(whatsapp_msg)

    else:
        print("No summaries available for the given topic.")
