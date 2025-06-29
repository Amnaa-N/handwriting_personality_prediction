import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
import numpy as np
import sys
import os
from PIL import Image
import base64
from pathlib import Path
from streamlit_lottie import st_lottie
import json
import requests


# Add backend folder to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(backend_path)

from feature_extractor import extract_handwriting_features

# Set page config
st.set_page_config(page_title="Handwriting Personality Assessment", layout="wide")


# Custom CSS for styling
st.markdown(
    """
    <style>

     [data-testid="stAppViewContainer"] {
        background-image: url("https://wallpapercave.com/wp/wp4207176.jpg");
        background-size: cover;
        color: #ffe097;
        text-shadow: 2px 2px 5px grey;
        margin-top: -40px;  
    }

       /* Apply font to everything */
    html, body, [data-testid="stAppViewContainer"] *, .stMarkdown, .stButton, .stTextInput {
        font-family: 'Poppins', sans-serif !important;
    }
   
    footer {visibility: hidden;}
    header {visibility: hidden;}


    h1, h2, h3 {
        color: white;
    }

    .stTitle{
    font-size:200px;
    }
    .trait-card {
        background-color: #fff4da;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        color:black
    }
    .long-card {
        background-color:  #fff4da 
;
        border-left: 5px solid #f0c929;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
         color:black
    }

    button[kind="primary"] {
    background-color: #f0c929 !important;
    color: white !important;
    font-size: 20px !important;
    padding: 12px 30px !important;
    border-radius: 8px !important;
    transition: background-color 0.3s ease;
    border: none;
}

button[kind="primary"]:hover {
    background-color: #ddb300 !important;
}
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🖊️ Personality Prediction from Handwriting")

st.markdown("Draw in the box below and click **Predict** to analyze handwriting features.")

# Canvas widget
canvas_result = st_canvas(
   
    stroke_width=6,
    stroke_color="#000000",
    background_color="#FFFFFF",
    update_streamlit=True,
    height=300,
    width=1300,
    drawing_mode="freedraw",
    key="canvas",
)


def interpret_trait(trait, score):
    description = ""
    if trait == "Openness":
        if score >= 0.66:
            description = "🧠 Highly imaginative and curious. Open to new experiences."
        elif score >= 0.33:
            description = "🎨 Moderately open-minded and creative."
        else:
            description = "📘 Prefers routine, traditional thinking, and familiar experiences."

    elif trait == "Conscientiousness":
        if score >= 0.66:
            description = "📋 Very organized, reliable, and goal-driven."
        elif score >= 0.33:
            description = "🗂️ Moderately dependable and structured."
        else:
            description = "🎲 Spontaneous, disorganized, or flexible."

    elif trait == "Extraversion":
        if score >= 0.66:
            description = "😄 Very outgoing, energetic, and sociable."
        elif score >= 0.33:
            description = "🙂 Balanced between introversion and extroversion."
        else:
            description = "🤫 Quiet, reserved, and introspective."

    elif trait == "Agreeableness":
        if score >= 0.66:
            description = "🤝 Highly compassionate, cooperative, and empathetic."
        elif score >= 0.33:
            description = "🙂 Moderately warm and considerate."
        else:
            description = "🧍‍♂️ More competitive, skeptical, or blunt."

    elif trait == "Neuroticism":
        if score >= 0.66:
            description = "😰 Emotionally sensitive, may experience stress or anxiety."
        elif score >= 0.33:
            description = "😌 Generally calm with occasional stress."
        else:
            description = "🧘‍♀️ Emotionally stable and resilient."

    return description


predict_btn = st.button("🔍 Predict Personality", key="predict")

if predict_btn:

    if canvas_result.image_data is not None:
        try:
            # Save canvas image
            img = Image.fromarray((canvas_result.image_data[:, :, :3] * 255).astype(np.uint8))
            img_path = "temp_handwriting.png"
            img.save(img_path)

            # Send image file to backend
            with open(img_path, "rb") as f:
                files = {"file": f}
                response = requests.post("http://localhost:5000/predict", files=files)

            # Delete temp image
            #if os.path.exists(img_path):
             #   os.remove(img_path)

            # Handle backend response
            if response.status_code == 200:
                predictions = response.json()


                st.markdown("## ✒️ Handwriting-Based Observations")
                rule_based_text = predictions.get("rule_based", "")
                st.markdown(f"<div class='long-card'>{rule_based_text}</div>", unsafe_allow_html=True)

                # Display individual trait scores
                st.markdown("## 📊 Trait Scores")
                traits = predictions.get("traits", {})
                for trait, score in traits.items():
                    try:
                        score = float(score)
                        st.markdown(f"""
                            <div class="trait-card">
                                <h4>{trait}: {score:.2f}</h4>
                                <p>{interpret_trait(trait, score)}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    except (ValueError, TypeError):
                        st.markdown(f"<div class='trait-card'><strong>{trait}</strong>: {score}</div>", unsafe_allow_html=True)

            else:
                st.error(f"🚫 Server error: {response.text}")

        except Exception as e:
            st.exception(f"An error occurred: {e}")
    else:
        st.warning("✍️ Please draw something on the canvas before predicting.")
