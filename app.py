import os
import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# Set your OpenAI API key
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


# Load the Chroma database
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"))
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
