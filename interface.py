import streamlit as st
from chat_backend import load_model_and_db, query_rag

st.set_page_config(page_title="DocBot",layout="centered")
st.title("💬 DocBot")
st.write("Ask me anything from the documentation.")

@st.cache_resource
def setup():
    return load_model_and_db()

db, model = setup()

query = st.chat_input("Go ahead ask me anything....")

if query:
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Give me a moment...."):
            response = query_rag(query,db,model)
            st.write(response)