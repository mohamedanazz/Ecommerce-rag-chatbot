from embedder import embed_User_query
from vectorstore import search_in_pinecone
from LLM import query_llm_with_context


def process_user_query(query: str):
    # Embed the user's query to create a vector representation
    query_vector = embed_User_query(query)

    # Search the vector DB to find top matching chunks related to the user's question
    matched_chunks = search_in_pinecone(query_vector)

    # Send the user query and search results to the LLM for generating a response
    response = query_llm_with_context(query, matched_chunks)

    return response


if __name__ == "__main__":
    user_query = "My product arrived damaged. Can I get a replacement or refund?"

    response = process_user_query(user_query)

    print("\n===== RAG RESPONSE =====")
    print(response)