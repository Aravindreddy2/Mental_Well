# app/utils/config.py
# app/utils/config.py
import streamlit as st

LLAMA_API_KEY = st.secrets["LLAMA_API_KEY"]
LLAMA_API_URL = st.secrets["LLAMA_API_URL"]


  
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "./data/embeddings"
# app/utils/config.py
ALERT_EMAIL = "aravindreddyashireddy@gmail.com"
ALERT_EMAIL_PASSWORD = "wtrs llcd exjw mpio" 

