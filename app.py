import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Load OpenAI API key securely
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load FAISS index
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Setup retriever with more chunks
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# GPT model for answering
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

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

        # 🔍 Retrieve chunks from FAISS
        docs = retriever.get_relevant_documents(query)

        # 🧠 Combine the chunks into one context block
        combined_context = "\n\n".join(doc.page_content for doc in docs)

        # 📝 Create a new prompt for GPT
        prompt = (
            f"You are an HR workshop assistant. The user asked:\n\n"
            f"{query}\n\n"
            "Here are the most relevant document excerpts:\n\n"
            f"{combined_context}\n\n"
            "Based on this content, provide a helpful and focused answer. "
            "If nothing is relevant, say: 'I couldn’t find anything helpful in your materials.'"
        )

        # 💬 Get GPT's response
        response = llm.invoke(prompt)

        # 🤖 Show answer
        st.markdown("### 🤖 Answer")
        st.write(response.content)


        # 📄 Show relevant sources (without duplicates and cleaned up)
if docs:
    st.markdown("#### 📄 Relevant Sources")
    seen = set()
    for doc in docs:
        raw_source = doc.metadata.get("source", "Unknown file")
        source = raw_source.replace("downloaded_docs/", "")
        if source not in seen:
            st.write(f"- {source}")
            seen.add(source)

