# 🧠 HR Workshop Assistant

This is an AI-powered assistant that helps HR teams search through internal HR workshop materials using natural language.

The assistant is built using:
- [Streamlit](https://streamlit.io) for the user interface
- [LangChain](https://www.langchain.com) for document retrieval
- [OpenAI](https://platform.openai.com) for embeddings and GPT-3.5 responses
- [FAISS](https://github.com/facebookresearch/faiss) for document vector storage

---

## 🚀 Features

- Ask natural questions like:  
  _"Suggest a workshop on conflict resolution"_  
  _"Do we have any content about teamwork?"_

- Instantly searches across embedded HR documents  
- Returns answers and suggests relevant files  
- Designed for non-technical HR team members to use easily

---


---

## 🔧 How to Update Documents

> This step is run locally. Do NOT run on Streamlit Cloud.

1. Add new files to the `downloaded_docs/` folder on your computer  
2. Run the following command locally:

```bash
python3 embed_docs.py

