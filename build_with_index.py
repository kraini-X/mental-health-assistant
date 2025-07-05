# build_index.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import PyPDF2 as pdf
from tqdm import tqdm

# 1. Read PDF
def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = pdf.PdfReader(f)
        for i in reader.pages:
            text += i.extract_text() or ""
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    start = 0
    chunks = []
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

text = read_pdf("Psychiatric Mental Health Nursing Concepts of Care in Evidence-Based Practice by Mary C. Townsend DSN  PMHCNS-BC (z-lib.org).pdf")
chunks = chunk_text(text)

# 2. Embedding
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embed_model.encode(chunks).tolist()

# 3. Store in Chroma
client = chromadb.PersistentClient(path="chroma_store")
collection_name = "mental_health_kb_v2"
try:
    client.delete_collection(name=collection_name)
except:
    pass

collection = client.get_or_create_collection(name=collection_name)

ids = [f"doc_{i}" for i in range(len(chunks))]

batch_size = 500
for i in tqdm(range(0, len(chunks), batch_size)):
    collection.add(
        documents=chunks[i:i+batch_size],
        embeddings=embeddings[i:i+batch_size],
        ids=ids[i:i+batch_size]
    )

print("✅ Index built successfully.")
