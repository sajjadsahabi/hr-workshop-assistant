import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load your OpenAI key securely test
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load the FAISS index
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)


retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

from langchain_core.messages import SystemMessage
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# Add system context manually using chain config
system_message = SystemMessage(
    content="You are an HR workshop assistant. Answer only based on the user's uploaded workshop documents. Be focused, clear, and suggest specific documents when possible."
)

from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
prompt = ChatPromptTemplate.from_messages([
    system_message,
    ("human", "{question}")
])
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    condense_question_prompt=prompt
)


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
