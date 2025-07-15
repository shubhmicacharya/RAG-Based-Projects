import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.messages import HumanMessage

load_dotenv()

MAX_WORDS = 1000
MIN_WORDS = 50

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def get_structured_prompt(text):
    return f"""
Role:
You are a professional news summarization agent capable of extracting key information from articles and rewriting it in a concise and reader-friendly way.

Input:
A news article in plain text format.

Output:
A concise summary of 3 to 4 sentences that highlights the key points of the article. The summary must be clear, accurate, and easy to read.

Constraints:
- Do not copy long verbatim excerpts.
- Do not include personal opinions.
- Avoid redundant sentences.
- Limit summary to ~100 words.

Task:
Read the input news article and generate a short summary using your understanding of the main points and facts.

Capabilities:
You understand news language, can differentiate between key points and filler content, and can rewrite complex ideas in simple language.

Reminders:
- Do not add any extra commentary or suggestions.
- Stick to the original article’s factual tone.
- Avoid mentioning "the article says" or similar phrases.
- Donot include anything related to ICE.

Article:
{text}
"""

def summarize(text):
    if len(text.split()) < MIN_WORDS:
        print("ℹ️ Skipping summarization: article too short.")
        return text

    try:
        trimmed_text = ' '.join(text.split()[:MAX_WORDS])
        print("✅ Sending article to Gemini for summarization...")
        prompt = get_structured_prompt(trimmed_text)
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        print("⚠️ LangChain summarization error:", e)
        return text
