# 🛒 E-Commerce RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot designed for an e-commerce brand to answer customer questions using the company's internal policies and documents.

The system retrieves relevant information from a vector database and provides context-aware answers using a Large Language Model (LLM).

---

## 🚀 Project Overview

Traditional chatbots often rely only on the knowledge stored inside the language model. This can lead to inaccurate or outdated answers when the user asks about company-specific information.

This project solves that problem using **Retrieval-Augmented Generation (RAG)**.

Instead of asking the LLM to answer directly, the system:

1. Converts the user's question into a vector embedding.
2. Searches a vector database for relevant information.
3. Retrieves the most relevant document chunks.
4. Sends the retrieved context along with the user's question to the LLM.
5. Generates an answer based on the retrieved company information.

### Example

**Customer:**

> My product arrived damaged. Can I get a replacement or refund?

**Chatbot:**

> I'm sorry about the damaged package. Please don't consume the affected product. I can help you with the refund/replacement process. Please provide your Order ID and, if possible, clear photos of the damaged product and packaging. Our team will verify the issue and arrange an appropriate refund or replacement.

The answer is generated using the relevant information retrieved from the e-commerce policy documents.

---

# 🏗️ Architecture

```text
                    User Question
                         │
                         ▼
              ┌─────────────────────┐
              │   Query Embedding   │
              │ Sentence Transformer│
              └──────────┬──────────┘
                         │
                         ▼
                Query Vector (384D)
                         │
                         ▼
              ┌─────────────────────┐
              │      Pinecone       │
              │    Vector Search    │
              └──────────┬──────────┘
                         │
                         ▼
                  Top-K Documents
                    (Top 4 chunks)
                         │
                         ▼
              ┌─────────────────────┐
              │ Context + Question  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   DeepSeek LLM      │
              │    Generation       │
              └──────────┬──────────┘
                         │
                         ▼
                  Final Answer
🔄 RAG Pipeline
1. Document Processing

The project starts with company documents such as:

Return policies
Refund policies
Replacement policies
Shipping policies
Product information
Customer support guidelines

PDF documents are processed and converted into text.

PDF
 ↓
Text Extraction
 ↓
Cleaned Text
2. Text Chunking

Large documents are divided into smaller chunks.

This makes retrieval more efficient because the system can retrieve only the relevant sections instead of sending the entire document to the LLM.

Large Document
      ↓
   Chunking
      ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
3. Embedding Generation

Each document chunk is converted into a numerical vector using:

Sentence Transformers

Model:

sentence-transformers/all-MiniLM-L6-v2

The model produces:

384-dimensional embeddings

The same embedding model is used for both:

Document chunks
User queries

This is important because both need to exist in the same vector space for similarity search.

4. Vector Storage

The generated embeddings are stored in:

Pinecone

Each vector contains:

ID
Vector
Metadata

Example metadata:

{
    "text": "Refund requests must be submitted...",
    "chunk_index": 4
}
5. Query Retrieval

When a user asks a question, the question is converted into an embedding.

The embedding is sent to Pinecone.

The system performs similarity search and retrieves the most relevant chunks.

The current implementation retrieves:

Top K = 4

matching chunks.

6. Context Construction

The retrieved chunks are combined into a context.

Conceptually:

Retrieved Chunk 1
+
Retrieved Chunk 2
+
Retrieved Chunk 3
+
Retrieved Chunk 4

Then the system sends:

Context + User Question

to the LLM.

7. LLM Generation

The project uses:

DeepSeek

The LLM receives the retrieved context and generates the final response.

The system prompt instructs the model to answer using the provided context rather than relying purely on its general knowledge.

🧰 Tech Stack
Technology	Purpose
Python	Core programming language
Sentence Transformers	Text embeddings
all-MiniLM-L6-v2	Embedding model
Pinecone	Vector database
DeepSeek	LLM generation
OpenAI Python SDK	API client for DeepSeek-compatible endpoint
python-dotenv	Environment variable management
PyPDF	PDF document processing
Git	Version control
GitHub	Source code hosting
📁 Project Structure
Ecommerce-rag-chatbot/
│
├── Resources/
│   └── Return&RefundPolicy.pdf
│
├── Chunker.py
├── LLM.py
├── QueryProceesor.py
├── dataprocessor.py
├── embedder.py
├── pdfreader.py
├── vectorstore.py
│
├── .env.example
├── .gitignore
├── Requirement.txt
└── README.md
📄 File Responsibilities
pdfreader.py

Responsible for reading PDF documents and extracting their text.

PDF → Raw Text
Chunker.py

Splits large documents into smaller chunks suitable for embedding and retrieval.

Text → Chunks
embedder.py

Generates embeddings using:

all-MiniLM-L6-v2

It contains functions for:

Embedding document chunks
Embedding user queries
vectorstore.py

Handles Pinecone operations:

Uploading vectors
Storing metadata
Similarity search
Retrieving relevant chunks
dataprocessor.py

Coordinates the document ingestion pipeline.

Documents
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
Pinecone
LLM.py

Handles communication with the DeepSeek LLM and generates responses using the retrieved context.

QueryProceesor.py

Coordinates the complete query pipeline:

User Query
   ↓
Embedding
   ↓
Pinecone Search
   ↓
Context Retrieval
   ↓
DeepSeek
   ↓
Response
🔐 Environment Variables

API credentials are not stored in the repository.

Create a local .env file:

DEEPSEEK_API_KEY=your_deepseek_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name

The repository contains:

.env.example

as a template.

Never commit your actual .env file.

⚙️ Installation
1. Clone the repository
git clone https://github.com/mohamedanazz/Ecommerce-rag-chatbot.git
cd Ecommerce-rag-chatbot
2. Create a virtual environment
Windows
python -m venv .venv

Activate it:

.venv\Scripts\activate
Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r Requirement.txt
4. Configure environment variables

Create:

.env

Add:

DEEPSEEK_API_KEY=your_deepseek_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
🗄️ Pinecone Configuration

The embedding model:

sentence-transformers/all-MiniLM-L6-v2

produces:

384 dimensions

Therefore, the Pinecone index must be configured with:

Dimension: 384

The similarity metric should be compatible with the normalized embeddings used by the project.

▶️ Running the Project
Step 1 — Process the documents

Run the document processing pipeline:

python dataprocessor.py

This processes the documents and stores their embeddings in Pinecone.

Step 2 — Ask a question

Run:

python QueryProceesor.py

Example:

My product arrived damaged. Can I get a replacement or refund?

The system will:

Generate Query Embedding
        ↓
Search Pinecone
        ↓
Retrieve Top 4 Chunks
        ↓
Send Context to DeepSeek
        ↓
Generate Final Response
💬 Example Questions

The chatbot can answer questions such as:

Refund

Can I get a refund for my order?

Damaged Product

My product arrived damaged. Can I get a replacement?

Return Policy

What is your return policy?

Refund Eligibility

How long do I have to request a refund?

Shipping

What should I do if my package arrives damaged?

Customer Support

What information do I need to provide for a damaged product claim?

The chatbot should answer based on the information available in the company's documents.

🎯 Why RAG?

Without RAG:

User Question
     ↓
LLM
     ↓
Potentially generic answer

With RAG:

User Question
     ↓
Retrieve company-specific information
     ↓
Relevant context
     ↓
LLM
     ↓
Grounded answer

RAG helps reduce hallucinations and allows the chatbot to work with private or frequently changing company information without retraining the LLM.

🔎 Retrieval Example

For the question:

My product arrived damaged. Can I get a replacement or refund?

The system converts the question into an embedding and searches Pinecone.

Example:

Found 4 matches for the query.

The retrieved chunks may contain information about:

Damaged products
Refund eligibility
Replacement process
Required order information
Required product photographs

These chunks are then provided to DeepSeek as context.

🔒 Security

Sensitive credentials are excluded from Git using:

.gitignore

The following file is never committed:

.env

Instead, the repository provides:

.env.example

with placeholder values.

📈 Future Improvements

Potential improvements for future versions include:

 FastAPI backend
 REST API for chatbot queries
 Streaming LLM responses
 Conversation history
 Chat session management
 Authentication and authorization
 RAG evaluation metrics
 Retrieval score filtering
 Hybrid search
 Reranking retrieved documents
 Metadata filtering
 Better chunking strategies
 Query rewriting
 Citation/source references
 PostgreSQL integration
 Redis caching
 Docker deployment
 Cloud deployment
 Monitoring and logging
 Production-grade error handling
🧠 Key Concepts Demonstrated

This project demonstrates practical experience with:

Retrieval-Augmented Generation (RAG)
Embeddings
Semantic Search
Vector Databases
Document Processing
Text Chunking
Similarity Search
Prompt Engineering
LLM Integration
API Integration
Environment Variable Management
Python Project Structure
Git & GitHub
👨‍💻 Author

Mohamed Anas

GitHub:

https://github.com/mohamedanazz
