
'''
 Summary of Santiago PDF Summarizer App's Flow:
1. User uploads a PDF using Streamlit.
2. The text is extracted from the PDF.
3. The text is split into chunks.
4. Embeddings are generated using a HuggingFace model.
5. A similarity search is run based on a predefined summary prompt.
6. GPT processes the most relevant parts and generates a summary.
7. The summary is displayed in the Streamlit app.
'''


## -------- Libraries ------------

# Import necessary libraries for the frontend (user interface)
import streamlit as st
import os

# Import backend libraries for processing
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.embeddings import HuggingFaceEmbeddings DESACTUALIZADO
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader


## -------- Set up the web page with Streamlit-----------

st.set_page_config(page_title="Santiago's PDF Summarizer")
st.title("Santiago's PDF Summarizer")
st.write("Summarize your PDF files using the power of LLMs and LangChain")
st.divider()
# Upload the PDF file through the Streamlit interface
pdf = st.file_uploader("Upload your PDF", type="pdf")
submit = st.button("Generate Summary")


###--------- Backend Logic for thee LLM---------------

# Function to split the text into smaller chunks and generate embeddings
def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )

    chunks = text_splitter.split_text(text)
    # Create embeddings using HuggingFace model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create a FAISS vector store from the text chunks
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    return knowledgeBase


# Function to summarize the content of the uploaded PDF
def summarizer(pdf):
    response = ""
    pdf_reader = PdfReader(pdf)
    text = ""

    # Extract all text from all pages in the PDF
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    # Process the text and convert it into a searchable vector space
    knowledgeBase = process_text(text)

    # Define a query that asks the model to summarize the content
    query = (
        "Summarize the content of the uploaded PDF file in approximately 5-8 sentences."
    )

    if query:
        # Search for the most relevant parts of the document for the query
        docs = knowledgeBase.similarity_search(query)

        # Load the LLM (GPT model) to answer the query
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.1)
        chain = load_qa_chain(llm, chain_type="stuff")

        # Run the chain with cost tracking
        with get_openai_callback() as cost:
            response = chain.run(input_documents=docs, question=query)
            print(cost)  # You can see the cost of the API call in the terminal/log

    return response


# OpenAI API key here for now, later will be moved to a .env file for security
os.environ["OPENAI_API_KEY"] = ("PERSONAL PRIVATE API KEY HERE")

# Run the summarizer function only when a PDF is uploaded and the button is clicked
if submit and pdf is not None:
    response = summarizer(pdf)
    st.subheader("PDF Summary")
    st.write(response)


