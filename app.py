import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain

# Load your OpenAI key securely
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load the FAISS index
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Try more k for better context

# Define the system prompt
system_message = SystemMessage(
    content=(
        "You are an HR workshop assistant. Answer only based on the user's uploaded workshop documents. "
        "Be focused, clear, and suggest specific documents when possible. "
        "If you do not find a match in the documents, say 'I could not find anything in your materials.' "
        "Do not make up answers."
    )
)

# Setup prompt and chain
prompt = ChatPromptTemplate.from_messages([
    system_message,
    ("human", "{question}")
])

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    condense_question_prompt=prompt
)

# Streamlit UI
st.set_page_config(page_title="Workshop Assistant")
st.title("🧠 Workshop Assistant")
st.markdown("Ask about workshop content and get suggestions from your documents.")

st.markdown("""
💡 **Examples you can try:**
- _"Suggest a workshop on conflict resolution."_
- _"Do I have any material on employee engagement?"_
- _"What file contains teamwork training?"_
""")

query = st.text_input("Type your question:")

if query:
    with st.spinner("Thinking..."):
        # 🔍 Show which chunks are being retrieved
        docs = retriever.get_relevant_documents(query)
        st.markdown("### 🔍 Retrieved Chunks (for debugging)")
        for i, doc in enumerate(docs, 1):
            st.markdown(f"**Chunk {i}:**")
            st.write(doc.page_content[:500])  # show first 500 characters
            st.caption(f"📄 Source: {doc.metadata.get('source', 'Unknown file')}")

        # 💬 Then pass to GPT
        response = qa.invoke({
            "question": query,
            "chat_history": []
        })

        st.markdown("### 🤖 Answer")
        st.write(response.get("answer", "Sorry, I couldn't find an answer."))


        if "source_documents" in response:
            st.markdown("#### 📄 Sources")
            for doc in response["source_documents"]:
                st.write(f"- {doc.metadata.get('source', 'Unknown file')}")
