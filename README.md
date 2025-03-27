# 🧠 HR Workshop Assistant

This is an AI-powered assistant that helps HR teams search and interact with internal workshop materials using natural language.

Built with:
- [Streamlit](https://streamlit.io/) for a browser-based interface
- [OpenAI GPT-3.5](https://platform.openai.com) for language understanding
- [FAISS](https://github.com/facebookresearch/faiss) for fast document similarity search
- [LangChain](https://www.langchain.com) for combining everything together

---

## 🎯 What It Does

- ✅ Let users ask **natural questions** like:
  - “Do we have anything on employee engagement?”
  - “What workshop covers conflict resolution?”
  - “Where can I find materials about leadership?”

- ✅ Returns an AI-generated **summary + suggested documents**
- ✅ Works entirely through a **simple browser interface**
- ✅ Can be easily updated with new documents (no tech knowledge needed by users)

---

## 📁 Project Structure

```bash
hr-workshop-assistant/
├── app.py                 # Main Streamlit app
├── embed_docs.py          # Script to convert docs into searchable format
├── requirements.txt       # Python dependencies
├── faiss_index/           # AI-generated search index (auto updated)
│   ├── index.faiss
│   └── index.pkl
└── downloaded_docs/       # Local folder to store HR files before embedding
```

---

## 🧪 How It Works (Behind the Scenes)

1. `embed_docs.py` loads and reads all documents from `downloaded_docs/`
2. It uses OpenAI to:
   - Extract keywords
   - Break the documents into chunks
   - Convert each chunk into a vector (embedding)
3. It stores these vectors in `faiss_index/` using FAISS
4. The Streamlit app (`app.py`) lets users type a question, searches the most similar chunks, and asks GPT to summarize them
5. The answer is displayed — along with a list of relevant documents

---

## 🔧 How to Use

### 🖥 For Users:
- Visit the Streamlit app link (e.g. `https://your-app.streamlit.app`)
- Type a question into the search box
- Read the AI answer and check the listed documents

---

### 🛠 For Developers / Admins:
To update the app with new documents:

1. Add new files to the `downloaded_docs/` folder on your local machine  
2. Run:

```bash
export OPENAI_API_KEY=sk-...
python3 embed_docs.py
```

3. Upload the updated `faiss_index/` (both `index.faiss` and `index.pkl`) to GitHub
4. Streamlit Cloud will automatically reload the app with the new data

✅ That’s it — no need to re-deploy!

---

## 🔐 API Key Management

OpenAI API key is **not hardcoded**.  
It's loaded from **Streamlit Secrets**, like this:

```python
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
```

To set your secret in Streamlit Cloud:

1. Go to your app dashboard  
2. Click **“Edit Secrets”**  
3. Add:

```
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 📌 Features in Progress (Future Ideas)

- [ ] Automatic syncing from Google Drive
- [ ] Upload documents directly via the app
- [ ] PDF preview or download links
- [ ] Admin dashboard / logs

---

## 🤝 Contributions

This project is maintained by [@sajjadsahabi](https://github.com/sajjadsahabi) and is open for contributions!

---

## 📃 License

free to use and modify.
