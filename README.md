﻿# personality_prediction_frontend
This is an AI-powered handwriting analysis system that predicts an individual’s Big Five personality traits—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—just from their handwriting! The dataset I used for this was from Kaggle:
https://www.kaggle.com/datasets/khushikyad001/handwriting-and-personality-traits-dataset/data

🛠️ How it works:
Users submit a handwritten sample via a digital canvas interface.

The system extracts both visual features (like slant angle, spacing, letter size) and behavioral features (like writing speed and pen lift frequency).

These features are analyzed using a hybrid approach:
🔹 Rule-based reasoning rooted in psychological graphology
🔹 Machine learning models including Ridge Regression, SVR, MLP, and XGBoost

🧪 What’s innovative:
I used Information Gain for intelligent feature selection—keeping only the most predictive traits.

The system combines interpretable logic with the predictive power of AI, ensuring both accuracy and transparency.

Results are presented in form of score blocks with intiutive summary of each trait score. Users can easily understand their personality analysis.

🧰 Technologies used:
Python (scikit-learn, XGBoost, Streamlit)

Custom feature extraction pipeline (OpenCV, NumPy)

Streamlit for a responsive and interactive UI

Real-time input via canvas interface

Whether you're in HR, education, or psychology, this system opens the door to non-intrusive, AI-driven personality profiling.
