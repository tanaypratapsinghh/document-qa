import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# Part C: model choice. Default is the cheaper model; the checkbox upgrades it.
BASIC_MODEL = "gpt-4.1-nano"
ADVANCED_MODEL = "gpt-4.1-mini"

SUMMARY_TYPES = {
    "Summarize the document in 100 words":
        "Summarize the document in about 100 words.",
    "Summarize the document in 2 connecting paragraphs":
        "Summarize the document in exactly two connecting paragraphs.",
    "Summarize the document in 5 bullet points":
        "Summarize the document in exactly five bullet points.",
}

LANGUAGES = ["English", "Spanish", "French", "German", "Hindi"]


def read_pdf(uploaded_file) -> str:
    """Read an uploaded PDF file and return its text."""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


st.title("Lab 2: Document Summarizer")
st.write("Upload a PDF and choose how you want it summarized.")

# ---------- Sidebar controls ----------
language = st.sidebar.selectbox("Output language", LANGUAGES)
summary_type = st.sidebar.selectbox("Type of summary", list(SUMMARY_TYPES))
use_advanced = st.sidebar.checkbox("Use advanced model")

model = ADVANCED_MODEL if use_advanced else BASIC_MODEL
st.sidebar.caption(f"Model: {model}")

# Part B: the key comes from Streamlit secrets, not from the user.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload a document (.pdf)", type="pdf")

if uploaded_file:
    document = read_pdf(uploaded_file)
    instruction = SUMMARY_TYPES[summary_type]

    messages = [
        {
            "role": "user",
            "content": (
                f"Here's a document: {document}\n\n---\n\n"
                f"{instruction} Write the summary in {language}."
            ),
        }
    ]

    with st.spinner(f"Summarizing with {model}..."):
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        st.write_stream(stream)