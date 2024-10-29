import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import time
from dotenv import load_dotenv

load_dotenv()

# Load the Groq API key
groq_api_key = os.environ['GROQ_API_KEY']
print(groq_api_key)

if "vector" not in st.session_state:
    
    # 1. Load
    st.session_state.loader = WebBaseLoader("https://fashionweekonline.com/fashion-week-dates")
    st.session_state.docs = st.session_state.loader.load()
    print("Documents loaded.")

    # 2. Text Split
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    print("Documents split into chunks.")

    # 3. Embedding
    st.session_state.embeddings = OllamaEmbeddings()
    print("Embeddings created.")

    # 4. Vector Store: Sending doc and embedding to vector store
    st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
    print("Vector store created.")

st.title("Fashion Finder")
st.subheader("Utilizing natural language chat, Fashion Finder is able to tell users when and where the next fashion show is.")
# 5. Prompt: Use prompt template
prompt = ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}
"""
)
print("Prompt template created.")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
print("ChatGroq model initialized.")

# 6. Document Chain: Stuff docs into model 
document_chain = create_stuff_documents_chain(llm, prompt)
print("Document chain created.")

# 7. Retriever: Converts the vector store into a retriever instance that can find relevant documents based on user input.
retriever = st.session_state.vectors.as_retriever()
print("Retriever created.")

# 8. Retriever Chain: Combines the retriever and document chain, enabling efficient query processing.
retrieval_chain = create_retrieval_chain(retriever, document_chain)
print("Retrieval chain created.")

prompt = st.text_input("Input your prompt here")

if prompt:
    start = time.process_time()
    
    # 9. Invoke: The retrieval chain is invoked to generate a response based on the context.
    response = retrieval_chain.invoke({"input": prompt})
    print("Response time :", time.process_time() - start)
    st.write(response['answer'])

    # With a streamlit expander
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")
