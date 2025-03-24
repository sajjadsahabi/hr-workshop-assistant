import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load your OpenAI key securely
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load the FAISS index
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local("faiss_index", embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Streamlit UI
st.set_page_config(page_title="HR Workshop Assistant")
st.title("🧠 HR Workshop Assistant")
st.markdown("Ask about HR workshop content and get suggestions from your documents.")

query = st.text_input("Type your question:")

if query:
    with st.spinner("Thinking..."):
        response = qa.invoke({"query": query})
        st.markdown("### 🤖 Answer")
        st.write(response)
