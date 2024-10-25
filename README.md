# 💊 Medical Information Chatbot

A **Streamlit-based Medical Chatbot** that provides general information about medications and symptoms. Using fuzzy matching, the chatbot identifies keywords and provides information about treatments and remedies for health-related queries. Please note that this is not a substitute for professional medical advice.

## 📋 Project Description

This chatbot uses natural language processing techniques to:
- Recognize keywords related to **medicines** and **symptoms**.
- Retrieve relevant information from a pre-defined medical database.
- Provide suggestions for remedies and general information on medications.

The chatbot is designed for ease of use with a **simple and intuitive interface** where users can type their questions and receive responses based on fuzzy keyword matching.

## 💻 Features

- **Fuzzy Matching:** The chatbot can identify approximate matches for medical terms using the `fuzzywuzzy` library, handling cases with typos or alternate spellings.
- **Keyword Recognition:** Built-in sets of keywords related to **medicines** and **symptoms** help the bot classify user queries accurately.
- **Tokenized Preprocessing:** Uses `nltk` for tokenization, lemmatization, and removal of stopwords, enabling the bot to focus on the main content of user queries.
- **Compound Phrase Normalization:** Recognizes compound phrases (e.g., "back pain" or "head ache") to improve accuracy.

## 🛠️ Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- Streamlit
- FuzzyWuzzy
- NLTK
