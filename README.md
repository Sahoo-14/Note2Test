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
* **Smart Fallbacks:** Implements automatic backup model loading (`flan-t5-small`) to ensure high availability and application uptime.
* **Performant Caching:** Leverages Streamlit's structural resource caching so the model loads into memory exactly once—not on every button click.

---

## 📂 Repository Structure

```text
Note2Test/
│
├── .gitignore               # Excludes unnecessary files like cache and virtual environments
├── README.md                # Project documentation and guide
├── requirements.txt         # Package dependencies
└── app.py                   # Main Streamlit application codebase
