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
# Sidebar
with st.sidebar:
    st.header("🧠 About NoteGenie")
    st.markdown(
        "NoteGenie helps you turn raw notes into a **quick summary** "
        "and a **self-test quiz** — great for last-minute revision."
    )

    st.subheader("How to use")
    st.markdown(
        "1. Paste your notes, or upload a PDF/DOCX/TXT file\n"
        "2. Click **Summarize** for a condensed version\n"
        "3. Click **Generate Quiz** to test yourself"
    )

    st.subheader("Tips")
    st.markdown(
        "- Longer, well-formed sentences give better quiz questions\n"
        "- Aim for 20+ words for a useful summary"
    )

    st.divider()
    st.caption("Built with Streamlit + Hugging Face Transformers")

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

MIN_WORDS_FOR_SUMMARY = 20
MAX_WORDS_SUPPORTED = 3000

with col1:
    if st.button("🔍 Summarize", use_container_width=True):
        stripped_input = user_input.strip()
        input_word_count = len(stripped_input.split())

        if not stripped_input:
            st.warning("Please enter some notes first!")
        elif input_word_count < MIN_WORDS_FOR_SUMMARY:
            st.warning(
                f"Your notes are quite short ({input_word_count} words). "
                f"Add at least {MIN_WORDS_FOR_SUMMARY} words for a meaningful summary."
            )
        elif input_word_count > MAX_WORDS_SUPPORTED:
            st.warning(
                f"Your notes are very long ({input_word_count} words). "
                f"Please shorten to under {MAX_WORDS_SUPPORTED} words to avoid timeouts."
            )
        else:
            with st.spinner("Loading AI model and summarizing... (First run may take a minute)"):
                try:
                    summarizer = load_summarizer()
                    # Handle max_length dynamically based on input length to avoid truncation warnings
                    max_len = min(100, max(30, int(input_word_count * 0.6)))

                    summary = summarizer(stripped_input, max_length=max_len, min_length=15, do_sample=False)[0]['summary_text']
                    st.subheader("📄 Summary")
                    st.write(summary)
                except ConnectionError:
                    st.error("⚠️ Couldn't download the AI model. Check your internet connection and try again.")
                except Exception as e:
                    st.error(f"⚠️ Something went wrong during summarization: {str(e)}")

MIN_WORDS_FOR_QUIZ = 10

with col2:
    if st.button("❓ Generate Quiz", use_container_width=True):
        stripped_input = user_input.strip()
        input_word_count = len(stripped_input.split())

        if not stripped_input:
            st.warning("Please enter some notes first!")
        elif input_word_count < MIN_WORDS_FOR_QUIZ:
            st.warning(
                f"Your notes are too short to build a quiz ({input_word_count} words). "
                f"Add at least {MIN_WORDS_FOR_QUIZ} words."
            )
        else:
            try:
                quiz = generate_quiz_from_notes(stripped_input)
                st.subheader("📝 Quiz")
                st.text(quiz)
            except Exception as e:
                st.error(f"⚠️ Something went wrong generating the quiz: {str(e)}")