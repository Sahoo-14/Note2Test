import streamlit as st
from transformers import pipeline
import random
import re
from pypdf import PdfReader
from docx import Document
import io

# Set page config must be the first Streamlit command
st.set_page_config(page_title="NoteGenie", layout="centered")

# Use @st.cache_resource so the model only loads ONCE, not on every button click!
@st.cache_resource
def load_summarizer():
    try:
        # Explicitly specify a fast, lightweight summarization model
        return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    except KeyError:
        # Fallback to text2text-generation if summarization task registration fails
        return pipeline("text2text-generation", model="google/flan-t5-small")

def extract_text_from_file(uploaded_file):
    """Extract plain text from an uploaded PDF, DOCX, or TXT file."""
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    elif file_type == "pdf":
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    elif file_type == "docx":
        doc = Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError(f"Unsupported file type: .{file_type}")
    
def generate_quiz_from_notes(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 5]
    questions = []

    for i, sentence in enumerate(sentences[:3]):
        words = sentence.split()
        if len(words) < 4:
            continue

        answer = words[-1].strip(".").capitalize()
        question = sentence.replace(answer, "_____") + "?"
        
        wrong_options = ["India", "Technology", "Student", "Team"]
        wrong_choices = random.sample([w for w in wrong_options if w.lower() != answer.lower()], 3)
        options = wrong_choices + [answer]
        random.shuffle(options)

        option_text = "\n".join([f"{chr(97+j)}. {opt}" for j, opt in enumerate(options)])
        full_question = f"{i+1}) {question}\n{option_text}\n"
        questions.append(full_question)

    return "\n".join(questions) if questions else "Could not generate questions. Try providing longer, complete sentences."

# UI Layout
st.title("🧠 NoteGenie - Summarize Notes & Create Quizzes")
st.markdown("Paste your notes below:")

uploaded_file = st.file_uploader("📎 Or upload notes (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

extracted_text = ""
if uploaded_file is not None:
    try:
        extracted_text = extract_text_from_file(uploaded_file)
        st.success(f"Loaded {len(extracted_text.split())} words from {uploaded_file.name}")
    except Exception as e:
        st.error(f"Couldn't read {uploaded_file.name}: {str(e)}")

user_input = st.text_area(
    "📝 Your Notes",
    value=extracted_text,
    height=300,
    placeholder="Enter your study notes here, or upload a file above..."
)


col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Summarize", use_container_width=True):
        if user_input.strip():
            with st.spinner("Loading AI model and summarizing... (First run may take a minute)"):
                try:
                    summarizer = load_summarizer()
                    # Handle max_length dynamically based on input length to avoid truncation warnings
                    input_words = len(user_input.split())
                    max_len = min(100, max(30, int(input_words * 0.6)))
                    
                    summary = summarizer(user_input, max_length=max_len, min_length=15, do_sample=False)[0]['summary_text']
                    st.subheader("📄 Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error during summarization: {str(e)}")
        else:
            st.warning("Please enter some notes first!")

with col2:
    if st.button("❓ Generate Quiz", use_container_width=True):
        if user_input.strip():
            quiz = generate_quiz_from_notes(user_input)
            st.subheader("📝 Quiz")
            st.text(quiz)
        else:
            st.warning("Please enter some notes first!")