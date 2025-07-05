# rag.py

from unittest import result
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import chromadb

from dotenv import load_dotenv
import os


import tempfile
from sentiment_tracker import log_sentiment
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client_chroma = chromadb.PersistentClient(path="chroma_store")
collection = client_chroma.get_or_create_collection(name="mental_health_kb_v2")

from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

def sentiment_analysis(text):
    truncated_text = text[:400]
    results = sentiment_pipeline(truncated_text)

    if isinstance(results, list) and len(results) > 0:
     
        top_result = sorted(results, key=lambda x: x['score'], reverse=True)[0]
        label = top_result['label']

        if label == 'POS':
            return '🟢 Positive'
        elif label == 'NEG':
            return '🔴 Negative'
        else:
            return '⚪️ Neutral'
    else:
        return '⚪️ Neutral'  


def sentiment_analysis_with_logging(text):

    sentiment = sentiment_analysis(text)
    log_sentiment(text, sentiment)
    return sentiment





def rag_with_history(user_input, history=[]):
    
    messages = []
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": user_input})

    if user_input.strip().lower() in ["show my progress", "statistics", "summary", "sentiment history", "sentiment summary","sentiment statistics","sentiment progress","journey","emotional journey", "emotional progress", "emotional summary", "emotional statistics", "emotional history","summarize my emotional journey"]:
        from sentiment_tracker import get_sentiment_text_for_llm
        context = get_sentiment_text_for_llm(limit=30)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You're a kind assistant who provides a summary of the user's emotional journey based on their recent entries and also suggest them proper measures that they should take based on the knowledge base."},
                {"role": "user", "content": f"Here are my recent emotional entries:\n{context}\n\nHow have I been doing emotionally?"}
            ],
            temperature=0.6,
            max_tokens=400
        )
        reply = response.choices[0].message.content
        sentiment = sentiment_analysis_with_logging(user_input)
        reply += f"\n\n🧠 *Sentiment*: **{sentiment}**"
        return {"role": "assistant", "content": reply}
    else:
        query_embedding = embed_model.encode(user_input).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        context = "\n".join(results["documents"][0])

        
        system_message = {
            "role": "system",
            "content": (
                "You are MindMate, an empathetic mental health assistant. "
                "If you aren't aware of the topic being discussed or is outside the scope of the context, politely refuse to answer. "
                "Use the following context to help answer the user's question:\n\n"
                f"{context}"
            )
        }
        
        sanitized_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages
            if isinstance(m, dict) and "role" in m and "content" in m
        ]

        all_messages = [system_message] + sanitized_messages



        # Step 5: Call GPT-4o-mini
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=all_messages,
            temperature=0.7,
            max_tokens=300
        )

        reply = response.choices[0].message.content
        sentiment = sentiment_analysis_with_logging(user_input)
        reply += f"\n\n🧠 *Sentiment*: **{sentiment}**"

       
        return {"role": "assistant", "content": reply}

def messages_to_pairs(messages):
    pairs = []
    for i in range(0, len(messages), 2):
        if i + 1 < len(messages):
            pairs.append([messages[i]['content'], messages[i + 1]['content']])
    return pairs
    
