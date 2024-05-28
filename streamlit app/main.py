import streamlit as st
import joblib
import re
import pandas as pd
from text_normalization import text_normalizer

# Load the model and vectorizer
xgb_opt = joblib.load('pkl files/best_xgb_model.pkl')
bow_vectorizer = joblib.load('pkl files/bow_vectorizer.pkl')

# Streamlit app
st.set_page_config(page_title="Emotion Prediction", page_icon=":smiley:", layout="wide")

st.markdown(
    """
    <div style="background-color:#f5deb3;padding:12px;border-radius:12px">
    <h1 style="color:#4B0082;text-align:center;">Emotion Prediction App: 😊😠😢</h1>
    </div>
    """, unsafe_allow_html=True
)

st.write("## Enter Text for Emotion Prediction")

# Text input
input_text = st.text_area("Enter your text here:")

if st.button("Predict"):
    if input_text:
        # Preprocess the input text
        preprocessed_text = text_normalizer(input_text)
        # Transform the text using the loaded vectorizer
        vectorized_text = bow_vectorizer.transform([preprocessed_text])
        # Predict the emotion
        prediction = xgb_opt.predict(vectorized_text)

        label_to_emotion = {
            0: ("happiness", "😊"),
            1: ("angry", "😠"),
            2: ("sad", "😢")
        }
        emotion, emoji = label_to_emotion[prediction[0]]

        # Display the result
        st.write(f"### Predicted Emotion: {emotion} {emoji}")
    else:
        st.error("Please enter some text for prediction.")

# Add a sidebar for additional information or options
st.sidebar.header("About")
st.sidebar.info(
    """
    This app uses a pretrained XGBoost model to predict emotions from text.
    The model has been trained on a dataset with various emotions and uses 
    text preprocessing techniques to improve prediction accuracy.
    """
)

st.sidebar.header("Instructions")
st.sidebar.info(
    """
    1. Enter the text you want to analyze in the text area.
    2. Click the 'Predict' button to see the predicted emotion.
    """
)
