# 🧠 MindMate: Mental Health Assistant

MindMate is an empathetic, RAG-based (Retrieval-Augmented Generation) mental health chatbot designed to provide supportive, informative, and sentiment-aware interactions. It uses a knowledge base built from a psychiatric nursing textbook and tracks emotional progress over time.

---

## 🌟 Features

- 🔍 **RAG-based Answers**: Combines user queries with relevant context from a medical knowledge base using ChromaDB and responds empathetically.Advices the user to seek professional help if the mental state is too critical
- 💬 **Chat History**: Retains past messages to support contextual conversation.
- 🧠 **Sentiment Analysis**: Analyzes the emotional tone of user input using a BERTweet model.The model studies from the emotion of the user and tailors the next response
- 📈 **Emotional Tracking**: Logs sentiment history and provides summaries of emotional well-being whenever prompted.
- 🎨 **Custom Gradio UI**: Clean and user-friendly chat interface with mood icons and summaries.


---

## 📚 Knowledge Base

The context used in responses is sourced from:
> **Psychiatric Mental Health Nursing: Concepts of Care in Evidence-Based Practice by Mary C. Townsend**

---

## 🚀 Tech Stack

- Python 3.10+
- Gradio (UI)
- Groq (LLM backend)
- Hugging Face Transformers (for sentiment and embedding)
- ChromaDB (vector store)
- Sentence Transformers
- PyPDF2 (PDF parsing)
- dotenv (environment handling)

---



