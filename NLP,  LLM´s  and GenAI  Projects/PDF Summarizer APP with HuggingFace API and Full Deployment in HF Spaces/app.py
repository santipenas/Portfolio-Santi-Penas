# ====== CORE SETUP ======
# Note: These are the foundation for our app
import os
from dotenv import load_dotenv
import streamlit as st  # Our app framework

# ====== PDF HANDLING ======
# Note: pypdf is lightweight and handles most PDFs well
from pypdf import PdfReader  # Better than PyPDF2 for our needs

# ====== LANGCHAIN COMPONENTS ======
# Note: We're using LangChain for text processing pipelines
from langchain.text_splitter import CharacterTextSplitter  # For chunking text
from langchain_community.llms import HuggingFaceHub  # For summary generation
from langchain.vectorstores import FAISS  # Local vector storage
from langchain_community.embeddings import HuggingFaceEmbeddings  # Text embeddings
from langchain.chains.question_answering import load_qa_chain  # Backup QA method

# ====== TRANSFORMERS ======
# Note: Direct HuggingFace imports for more control
from transformers import (
    pipeline,  # For ready-to-use NLP pipelines
    AutoModelForQuestionAnswering,  # Custom QA models
    AutoTokenizer  # Handles model tokenization
)

# ====== ENVIRONMENT SETUP ======
load_dotenv()  # Loads from .env file (keep your API key here)

# Safety check for HuggingFace token
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    st.error("⚠️ Hugging Face API token not found. Please add it as a secret in Hugging Face Spaces.")
    st.stop()  # Graceful exit if missing token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token  # Set for LangChain

# ====== STREAMLIT UI ======
st.set_page_config(page_title="Santiago's PDF Summarizer & Q&A")
st.title("📄 Santiago's PDF Summarizer & Q&A")
st.write("Summarize your PDF or ask questions about its content using free Hugging Face models.")
st.divider()

# PDF upload widget - shows only once
pdf = st.file_uploader("Upload your PDF", type="pdf")

# Show buttons only after PDF upload to prevent errors
if pdf is not None:
    summary_btn = st.button("📚 Generate Summary")
    qa_btn = st.button("❓ Ask a Question")
    user_question = st.text_input("Type your question here (for Q&A only):")

# ====== CORE FUNCTIONS ======
def extract_text_from_pdf(pdf):
    """Extracts raw text from PDF with error handling"""
    try:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Handles None returns
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def summarize_pdf(text):
    """Generates summary using BART model with chunking"""
    try:
        # Chunking prevents model context window overflow
        text_splitter = CharacterTextSplitter(
            separator="\n", 
            chunk_size=1000,  # Optimal for BART-large
            chunk_overlap=100,  # Maintains context between chunks
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # Using BART specifically for summarization
        llm = HuggingFaceHub(
            repo_id="facebook/bart-large-cnn",  # Specialized for summaries
            model_kwargs={
                "temperature": 0.5,  # Balances creativity vs accuracy
                "max_length": 100  # Keeps summaries concise
            }
        )

        # Process each chunk separately then combine
        summaries = []
        for chunk in chunks:
            prompt = f"Summarize this: {chunk}"  # Simple but effective prompt
            summary = llm(prompt)
            summaries.append(summary)

        return "\n\n".join(summaries)  # Combine with spacing
    except Exception as e:
        st.error(f"Summarization error: {str(e)}")
        return None

def answer_question(text, question):
    """Handles Q&A with context-aware responses"""
    try:
        # --- Text Preparation ---
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1200,  # Larger chunks for better context
            chunk_overlap=200,  # Prevents information loss at edges
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # --- Semantic Search Setup ---
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1"  # QA-optimized
        )
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        
        # Retrieve most relevant sections
        docs = knowledge_base.similarity_search(question, k=4)  # Get top 4 matches
        if not docs:
            return "I couldn't find relevant information for this question."

        # --- QA Model Configuration ---
        model_name = "deepset/roberta-base-squad2"  # Reliable PyTorch model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForQuestionAnswering.from_pretrained(model_name)

        # Pipeline with optimized settings
        qa_pipeline = pipeline(
            "question-answering",
            model=model,
            tokenizer=tokenizer,
            max_seq_len=384,  # Standard for RoBERTa
            top_k=2,  # Get two potential answers
            handle_impossible_answer=True  # Better than failing
        )

        # --- Answer Generation ---
        context = "\n\n".join([doc.page_content for doc in docs])
        results = qa_pipeline(question=question, context=context, top_k=2)
        
        if not results or results[0]['answer'].strip() == "":
            return "The document doesn't contain a clear answer to this question."

        # --- Response Enrichment ---
        primary_answer = results[0]['answer'].strip()
        secondary_answer = results[1]['answer'].strip() if len(results) > 1 else None
        
        response = f"{primary_answer}"
        
        # Add secondary answer if different and valuable
        if secondary_answer and secondary_answer.lower() != primary_answer.lower():
            response += f"\n\nAdditional context: {secondary_answer}"
        
        # Include supporting evidence
        response += "\n\n**Supporting Excerpts:**"
        for i, doc in enumerate(docs[:2]):  # Limit to 2 for readability
            response += f"\n\n- Excerpt {i+1}: {doc.page_content[:250]}..."  # Preview

        return response

    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        return "Sorry, I encountered an error. Please try again with a different question."

# ====== MAIN EXECUTION FLOW ======
if pdf is not None:
    with st.spinner("Reading and processing the PDF..."):
        full_text = extract_text_from_pdf(pdf)
        if full_text is None:
            st.stop()  # Don't proceed if text extraction failed

    # Summary generation path
    if summary_btn and full_text:
        with st.spinner("Generating summary..."):
            summary = summarize_pdf(full_text)
        if summary:
            st.subheader("📚 PDF Summary")
            st.write(summary)  # Display with proper formatting

    # Q&A path
    if qa_btn and user_question.strip() != "" and full_text:
        with st.spinner("Finding the answer..."):
            answer = answer_question(full_text, user_question)
        if answer:
            st.subheader("❓ Answer to Your Question")
            st.write(answer)  # Renders markdown formatting