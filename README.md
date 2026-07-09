# Note2Test 🧠
> **Note2Test: Instantly turn your notes into smart study quizzes.**
> *Turns your documentation into a personalized test engine, making studying both smarter and faster.*

---

## 📄 Description

**Note2Test** is an AI-powered study assistant designed to transform static notes into active learning resources. By leveraging advanced natural language processing, the application allows users to instantly condense lengthy study materials into concise summaries while simultaneously generating interactive, fill-in-the-blank quizzes.

Perfect for students and professionals alike, Note2Test bridges the gap between passive reading and active recall, ensuring that key information is captured and reinforced efficiently. Whether you are prepping for an exam or mastering a new topic, Note2Test turns your documentation into a personalized test engine, making studying both smarter and faster.

---

## ✨ Features

* **AI-Powered Summarization:** Uses a lightweight, fast Transformers pipeline (`distilbart-cnn-12-6`) to dynamically condense text based on input length.
* **Active Recall Quizzing:** Automatically extracts sentences from your notes to generate fill-in-the-blank review questions.
* **Multi-Format File Upload:** Skip the copy-paste — upload notes directly as **PDF**, **DOCX**, or **TXT** and Note2Test extracts the text for you.
* **Smart Input Validation:** Flags notes that are too short or too long before processing, and surfaces clear, human-readable errors if a model or file fails to load.
* **Smart Fallbacks:** Implements automatic backup model loading (`flan-t5-small`) to ensure high availability and application uptime.
* **Performant Caching:** Leverages Streamlit's structural resource caching so the model loads into memory exactly once — not on every button click.
* **Guided Sidebar:** Built-in "how to use" instructions and tips panel so new users know exactly what to do.

---

## 🚀 Setup

```bash
git clone https://github.com/<your-username>/note2test.git
cd note2test
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The first run downloads the summarization model, so it may take a minute.

---

## 🧭 Usage

1. Paste your notes into the text box, **or** upload a PDF/DOCX/TXT file.
2. Click **🔍 Summarize** for a condensed version of your notes.
3. Click **❓ Generate Quiz** to create a self-test quiz from the same notes.

**Tips for best results:**
- Aim for at least 20 words when summarizing, and 10+ words for quiz generation.
- Longer, well-formed sentences produce better quiz questions.
- Very long notes (3000+ words) should be trimmed to avoid timeouts.

---

## 📂 Repository Structure

```text
Note2Test/
│
├── .gitignore               # Excludes unnecessary files like cache and virtual environments
├── README.md                # Project documentation and guide
├── requirements.txt         # Package dependencies
└── app.py                   # Main Streamlit application codebase
```

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Hugging Face Transformers](https://huggingface.co/docs/transformers) — summarization pipeline
- [pypdf](https://pypi.org/project/pypdf/) — PDF text extraction
- [python-docx](https://python-docx.readthedocs.io/) — DOCX text extraction

---

## 🌱 Branching

- `main` — stable, deployable version
- `dev` — active development

---

## 🗺️ Roadmap / Ideas

- Export summary/quiz as downloadable PDF or TXT
- Difficulty levels for quiz questions
- Session history of past summaries/quizzes
