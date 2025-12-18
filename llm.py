import os
from groq import Groq
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY =os.environ["GROQ_API_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
INDEX_NAME = "chatbot-demo"   # index
TOP_K = 8

client = Groq(api_key=GROQ_API_KEY)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

#enbedding
def embed_query(text: str):
    return embedding_model.encode(text).tolist()


#  RETRIEVAL 
def retrieve_context(user_query, top_k=TOP_K):
    query_vec = embed_query(user_query)

    results = index.query(vector=query_vec, top_k=top_k, include_metadata=True)

    contexts = []
    for match in results.matches:
        contexts.append({
            "source": match.metadata.get("source", ""),
            "text": match.metadata.get("text", "")
        })

    return contexts

    
#  FORMAT CONTEXT 
def format_context(chunks):
    formatted = ""
    for i, c in enumerate(chunks, 1):
        formatted += f"Context {i} (source: {c['source']}): {c['text']}"
    return formatted.strip()


#  FORMAT CONTEXT 
def format_context(chunks):
    formatted = ""
    for i, c in enumerate(chunks, 1):
        formatted += f"Context {i} (source: {c['source']}): {c['text']}"
    return formatted.strip()


#  LLM ANSWER 
def answer_query(user_query):
    chunks = retrieve_context(user_query)
    context_text = format_context(chunks)
    
    print(context_text)
    system_prompt = f"""
    You are an official AI assistant for the Partneroptimizer website.

    Your role is to Answer the visitor’s question using ONLY the provided Website Information.
    Do NOT make assumptions.
    Do NOT cite or mention sources.

    Visitor Question:
    {user_query}

    Website Information:
    {context_text}

    Provide a clear, helpful answer that follows all rules above.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
        ],
        temperature=0.5,
        max_tokens=200
    )

    return response.choices[0].message.content
  
# main function
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() == "exit":
            break
        print("\nAnswer:\n")
        print(answer_query(q))
