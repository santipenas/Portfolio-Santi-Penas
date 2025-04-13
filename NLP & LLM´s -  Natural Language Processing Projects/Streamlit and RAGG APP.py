import streamlit as st
import chromadb
from openai import OpenAI
import os

# Step 1: Set up the OpenAI client using an API key from the environment (safer than hardcoding)
# Make sure to set your OPENAI_API_KEY in your .streamlit/secrets.toml file or as an environment variable

openai_api_key = os.getenv("OPENAI_API_KEY")  # Get the OpenAI API key from the environment
if not openai_api_key:
    st.error("Please set your OpenAI API key as an environment variable or in the .streamlit/secrets.toml file.")
    st.stop()

client_openai = OpenAI(api_key=openai_api_key)

# Function to get a response from the model
def get_completion(prompt):
    response = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Using the GPT-3.5 Turbo model
        messages=[
            {
                "role": "system", 
                "content": "You're a helpful assistant who looks answers up for a user in a textbook and returns the answer to the user's question. If the answer is not in the textbook, you say 'I'm sorry, I don't have access to that information.'"
            },
            {
                "role": "user", 
                "content": prompt  # User's question
            },
        ]
    )
    # Return the model's response
    return response.choices[0].message.content

# Step 2: Setup ChromaDB for similarity search
# Chroma is a vector database. We are setting it to use in-memory storage, which is useful for quick prototyping.

client_chroma = chromadb.PersistentClient("./mycollection")  # This stores your database locally in 'mycollection'
collection = client_chroma.get_or_create_collection(name="RAG_Assistant", metadata={"hnsw:space": "cosine"})

# Streamlit UI elements
st.title("Similarity Search App")  # Title of the web app
st.markdown("This app uses Chroma to perform similarity searches on a collection of documents and OpenAI to answer questions based on the search results.")

st.sidebar.title("Configuration")  # Sidebar title
st.sidebar.markdown("Adjust the settings for your query.")  # Sidebar description

# User input in the sidebar
n_results = st.sidebar.number_input("Number of results", min_value=1, max_value=10, value=1)  # Number of search results
user_question = st.text_area("Ask a question", key="user_question")  # User's question input area

# When the user clicks "Get Answers", this will execute
if st.button("Get Answers"):
    st.write(f"Question: {user_question}")
    st.write(f"Number of Results: {n_results}")

    # Perform similarity search with ChromaDB
    results = collection.query(query_texts=[user_question], n_results=n_results, include=["documents", "metadatas"])
    
    search_results = []  # Store formatted search results

    # Loop through the search results and format them with metadata
    for res in results["documents"]:
        for doc, meta in zip(res, results["metadatas"][0]):
            # Format the document text and its metadata
            metadata_str = ", ".join(f"{key}: {value}" for key, value in meta.items())
            search_results.append(f"{doc}\nMetadata: {metadata_str}")
    
    # Join search results into a single text block
    search_text = "\n\n".join(search_results)

    # Step 3: Format the prompt using the RAG (Retrieve and Generate) Instructions
    prompt = f"""Your task is to answer the following user question using the supplied search results.
    User Question: {user_question}
    Search Results: {search_text}
    """
    
    # Get the response from OpenAI
    response = get_completion(prompt)
    st.write(response)  # Display OpenAI's answer

    # Step 4: Optional improvement, where we ask the assistant to cite passages from the search results.
    metadata_prompt = f"""
    Your task is to answer the following user question using the supplied search results. 
    At the end of each search result, include Metadata: Cite the passages, their chunk index, and their URL in your answer.
    User Question: {user_question}
    Search Results: {search_text}
    """
    
    # Get and display the response with metadata citation
    metadata_response = get_completion(metadata_prompt)
    st.write("With citations: ", metadata_response)
