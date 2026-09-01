import streamlit as st
from openai import OpenAI

MODEL = "gpt-4.1"

st.title("Lab 1: Document question answering")
st.write(
    "Upload a document below and ask a question about it and GPT will answer!"
)

# Part B: the key now comes from Streamlit secrets, not from the user.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    document = uploaded_file.read().decode()
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )
    st.write_stream(stream)