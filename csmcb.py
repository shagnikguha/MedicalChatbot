import streamlit as st
import json
import nltk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

medicine_keywords = {'medicine', 'medication', 'drug', 'treatment', 'prescription', 'pill', 'tablet', 'capsule', 'syrup', 'ointment', 'inhaler', 'injection', 'dose', 'dosage', 'pharmaceutical', 'therapy', 'antibiotic', 'painkiller', 'vaccine'}
symptom_keywords = {'symptom', 'pain', 'condition', 'illness', 'discomfort', 'ache', 'ailment', 'disorder', 'syndrome', 'disease', 'infection', 'inflammation', 'fever', 'cough', 'headache', 'nausea', 'fatigue', 'dizziness', 'rash', 'swelling', 'remedy', 'cure'}

with open('medical_data.json', 'r') as f:
    medical_data = json.load(f)

with open('compound_phrases.json', 'r') as f:
    compound_phrases = json.load(f)

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # compound phrases normalization
    for phrase, normalized in compound_phrases.items():
        text = text.replace(phrase, normalized)

    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def get_medicine_info(query):
    medications = medical_data['content']['Subsystems'][0]['Medications']['General']
    best_match = None
    highest_ratio = 0

    # matching query as phrase
    for medicine in medications:
        ratio = fuzz.ratio(query.lower(), medicine['name'].lower())
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = medicine

    # token based matching
    if highest_ratio < 70:
        tokens = preprocess_text(query)
        for medicine in medications:
            for token in tokens:
                ratio = fuzz.ratio(token, medicine['name'].lower())
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = medicine

    if best_match and highest_ratio > 70:
        return f"**Medicine**: {best_match['name']}\n\n**Uses**: {best_match['uses']}"
    return "Sorry, I couldn't find information about that medicine."

def get_symptom_info(query):
    symptoms = medical_data['content']['Subsystems'][1]['Categories']['General']
    best_match = None
    highest_ratio = 0

    for symptom in symptoms:
        ratio = fuzz.ratio(query.lower(), symptom['symptom'].lower())
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = symptom

    if highest_ratio < 70:
        tokens = preprocess_text(query)
        for symptom in symptoms:
            for token in tokens:
                ratio = fuzz.ratio(token, symptom['symptom'].lower())
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = symptom

    if best_match and highest_ratio > 70:
        return f"**Symptom**: {best_match['symptom']}\n\n**Remedies**: {', '.join(best_match['remedies'])}"
    return "Sorry, I couldn't find information about that symptom."

def get_response(user_input):
    # normalize input with known compound phrases before processing
    for phrase, normalized in compound_phrases.items():
        user_input = user_input.replace(phrase, normalized)
    
    # check if entire query matches any symptoms or medications
    if any(fuzz.ratio(user_input.lower(), keyword) > 80 for keyword in symptom_keywords):
        return get_symptom_info(user_input)
    
    if any(fuzz.ratio(user_input.lower(), keyword) > 80 for keyword in medicine_keywords):
        return get_medicine_info(user_input)

    # token-based matching if phrase doesn't match
    tokens = preprocess_text(user_input)
    
    if any(fuzz.ratio(token, keyword) > 80 for token in tokens for keyword in symptom_keywords):
        return get_symptom_info(user_input)
    elif any(fuzz.ratio(token, keyword) > 80 for token in tokens for keyword in medicine_keywords):
        return get_medicine_info(user_input)
    else:
        return "I'm not sure if you're asking about a medicine or a symptom. Please clarify or try rephrasing your question."

st.set_page_config(page_title="💊 Medical Info Chatbot", page_icon="💊", layout="centered")

st.markdown(
    """
    <style>
    .main {background-color: #f0f2f6;}
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .stMarkdown h3 {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("💊 Medical Information Chatbot")
st.write(
    """
    Welcome! You can ask about medicines or symptoms, and I'll provide general information.  
    Please note: This is **not** a substitute for professional medical advice.
    """
)

user_input = st.text_input(
    "Ask a question (e.g., 'Tell me about aspirin' or 'What are remedies for a headache?')", 
    placeholder="Type your query here..."
)

if st.button("Submit") and user_input:
    response = get_response(user_input)

    st.markdown("### 🤖 Chatbot Response:")
    st.write(response)

st.sidebar.title("🛠 How to use")
st.sidebar.write(
    """
    This chatbot can help you with:
    - Information about medications
    - Remedies for symptoms  
    - Type your query in the text box, and the chatbot will respond with relevant information.
    - Please ensure to use the following keywords:
        - symptom, pain, condition, remedy, illness
        - medicine, medication, drug, treatment, prescription
    """
)

st.sidebar.write("---")
st.sidebar.title("⚠️ Disclaimer")
st.sidebar.info(
    """
    **Note**: This chatbot provides **general information** only. 
    Always consult a healthcare professional for specific medical advice.
    """
)