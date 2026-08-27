import streamlit as st
from openai import OpenAI, AuthenticationError, OpenAIError

# ---------- Config ----------
# Lab 01, step 6b: change the model. Options: gpt-4.1, gpt-5-chat-latest, gpt-5-nano
MODEL = "gpt-4.1"

st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need an OpenAI API key, which you can get "
    "[here](https://platform.openai.com/account/api-keys)."
)


# ---------- Step 6a: validate the API key as soon as it is entered ----------
def validate_api_key(key: str) -> bool:
    """Make a cheap call to OpenAI to confirm the key works."""
    try:
        OpenAI(api_key=key).models.list()
        return True
    except AuthenticationError:
        return False
    except OpenAIError:
        return False


openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
elif not validate_api_key(openai_api_key):
    st.error("Invalid OpenAI API key. Please check it and try again.", icon="🚨")
else:
    st.success("API key is valid.", icon="✅")
    client = OpenAI(api_key=openai_api_key)

    # ---------- Only shown once the key is valid ----------
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

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