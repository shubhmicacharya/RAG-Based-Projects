from datetime import datetime

def format_whatsapp_message(topic, summaries):
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"📰 DAILY NEWS SUMMARY: {topic.upper()}\n📅 Date: {today}\n\n"

    # Limit total message length to under 1500 characters
    char_limit = 1500
    for i, summary in enumerate(summaries, 1):
        entry = f"{i}️⃣ {summary.strip()}\n\n"
        if len(message) + len(entry) > char_limit:
            break
        message += entry

    #message += "🤖 Powered by Gemini + LangChain.\n💡 Reply with a topic to learn more!"
    return message
