from torch.fx.experimental.unification.dispatch import namespace

from pdfreader import read_pdf
from Chunker import chunk_pages
from embedder import embed_chunks
from vectorstore import store_in_pinecone
from typing import List

pdf_path = r"C:\Users\DELL\PycharmProjects\PythonProject\RAG_Chatbot\Resources\Return&RefundPolicy.pdf"

def run():
    # Read HR Policy PDF and extract text
    pages = read_pdf(pdf_path)


    # Chunk the data into smaller pieces
    chunks = chunk_pages(pages)
    print(f"Total chunks Created: {len(chunks)}")
    print("first Chunks:")
    print(chunks[0])

    # Embed the chunks using OpenAI's embedding model to create vector representations
    embeddings = embed_chunks(chunks)
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding size: {len(embeddings[0])}")

    print("\nFirst embedding:")
    print(embeddings[0][:10])

    # Store the chunks and their embeddings in Pinecone vector database
    store_in_pinecone(chunks, embeddings,namespace="")

if __name__ == '__main__':
    run()