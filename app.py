import streamlit as st
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier  # Ensure this is imported for pickle to load the model

# --- Configuration and Page Setup ---
st.set_page_config(
    page_title="Advanced Phishing Detector",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Custom CSS for Professional and Colorful UI ---
st.markdown("""
    <style>
    /* Global Styles */
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #e0f2f7; /* Light blue background */
    }

    .stApp > header { 
        display: none; /* Hide Streamlit default header */
    }

    .main .block-container {
        background-color: #ffffff; 
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
        margin-bottom: 30px;
    }

    /* Title Styling */
    h1 {
        color: #0056b3;
        text-align: center;
        margin-bottom: 25px;
        font-size: 2.8em;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }

    h2, h3 {
        color: #007bff;
        margin-top: 35px;
        margin-bottom: 18px;
        border-bottom: 2px solid #a7d9ed;
        padding-bottom: 8px;
        font-weight: 600;
    }

    /* Input Fields Styling */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        border: 1px solid #ced4da;
        border-radius: 8px;
        padding: 10px 15px;
        color: #343a40;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        outline: none;
    }

    /* FIX: Proper label styling */
    div[data-testid="stNumberInputLabel"] > label,
    div[data-testid="stTextInputLabel"] > label {
        color: #212529 !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
        text-align: left !important;
        font-size: 1.15em !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #28a745, #218838);
        color: white;
        font-weight: bold;
        padding: 12px 25px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 30px;
        font-size: 1.1em;
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #218838, #1e7e34);
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 123, 255, 0.3);
    }

    /* Result Boxes */
    .result-phishing {
        background-color: #ffebee;
        color: #d32f2f;
        padding: 25px;
        border-radius: 12px;
        font-size: 1.6em;
        font-weight: bold;
        text-align: center;
        margin-top: 40px;
        border: 2px solid #ef5350;
        box-shadow: 0 6px 15px rgba(255, 0, 0, 0.1);
    }
    .result-not-phishing {
        background-color: #e8f5e9;
        color: #388e3c;
        padding: 25px;
        border-radius: 12px;
        font-size: 1.6em;
        font-weight: bold;
        text-align: center;
        margin-top: 40px;
        border: 2px solid #66bb6a;
        box-shadow: 0 6px 15px rgba(0, 255, 0, 0.1);
    }

    /* Sidebar Styling */
    .css-1lcbmhc {
        background-color: #2c3e50;
        color: white;
        padding: 20px;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    .css-1lcbmhc h2 {
        color: #e0f2f7;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    .css-1lcbmhc .stText {
        color: #a7d9ed;
    }
    .css-1lcbmhc .stAlert {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px;
    }

    /* Disclaimer */
    .stMarkdown p {
        color: #6c757d;
        text-align: center;
        margin-top: 30px;
        font-size: 0.9em;
    }
    /* Universal Label Styling Fix */
label, div[data-testid="stNumberInputLabel"] label, div[data-testid="stTextInputLabel"] label {
    color: #212529 !important;   /* Dark visible text */
    font-weight: 700 !important; /* Bold */
    font-size: 1.1em !important; /* Bigger size */
    margin-bottom: 6px !important;
    display: block !important;   /* Force labels to show */
    visibility: visible !important;
}

    </style>
""", unsafe_allow_html=True)

# --- Model Loading ---
model = None
try:
    with open('random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)
    st.sidebar.success("Model loaded successfully!")
except FileNotFoundError:
    st.error("Error: 'random_forest_model.pkl' not found.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# --- Features ---
input_features = [
    'having_IP_Address', 'URL_Length', 'Shortining_Service',
    'having_Sub_Domain', 'no_of_dot', 'double_slash_redirecting',
    'no_of_ports', 'on_mouseover', 'RightClick', 'URL_of_Anchor',
    'Links_in_tags', 'SFH', 'Submitting_to_email', 'Redirect',
    'DNSRecord', 'Abnormal_URL'
]

# Sidebar Info
with st.sidebar:
    st.header("About This App")
    st.info("This app uses a Random Forest Classifier to detect phishing sites.")
    st.markdown("---")
    st.write("Developed for Phishing Detection Project")
    st.write("Model Type: Random Forest Classifier")

# --- User Input ---
st.header("Enter Website Feature Values")
st.markdown("Provide the numerical values for the 16 selected features.")

feature_inputs = {}
col1, col2 = st.columns(2)

for i, feature in enumerate(input_features):
    help_text = ""
    if feature == 'having_IP_Address': help_text = "Is an IP address used instead of a domain? (0=No, 1=Yes)"
    elif feature == 'URL_Length': help_text = "Number of characters in the URL."
    elif feature == 'Shortining_Service': help_text = "URL shortener used? (0=No, 1=Yes)"
    elif feature == 'having_Sub_Domain': help_text = "Multiple subdomains present? (0=No, 1=Yes)"
    elif feature == '_of_dot': help_text = "Number of dots in the URL."
    elif feature == 'double_slash_redirecting': help_text = "Contains '//' after protocol? (0=No, 1=Yes)"
    elif feature == '__of_ports': help_text = "Number of ports present in the URL."
    elif feature == 'on_mouseover': help_text = "Uses onmouseover to hide links? (0=No, 1=Yes)"
    elif feature == 'RightClick': help_text = "Is right-click disabled? (0=No, 1=Yes)"
    elif feature == 'URL_of_Anchor': help_text = "Ratio of anchor URLs to total URLs."
    elif feature == 'Links_in_tags': help_text = "Ratio of links in common HTML tags."
    elif feature == 'SFH': help_text = "Form handler submits to external URL? (0=No, 1=Yes)"
    elif feature == 'Submitting_to_email': help_text = "Form submits to email? (0=No, 1=Yes)"
    elif feature == 'Redirect': help_text = "Number of redirects."
    elif feature == 'DNSRecord': help_text = "Domain has valid DNS record? (0=No, 1=Yes)"
    elif feature == 'Abnormal_URL': help_text = "URL looks abnormal? (0=No, 1=Yes)"

    if i % 2 == 0:
        with col1:
            feature_inputs[feature] = st.number_input(f"**{feature.replace('_', ' ')}**", key=f"input_{feature}", help=help_text)
    else:
        with col2:
            feature_inputs[feature] = st.number_input(f"**{feature.replace('_', ' ')}**", key=f"input_{feature}", help=help_text)

st.markdown("---")

# --- Prediction Button ---
if st.button("Predict if Phishing"):
    input_data = [feature_inputs[f] for f in input_features]
    input_array = np.array(input_data).reshape(1, -1)

    try:
        prediction = model.predict(input_array)
        prediction_proba = model.predict_proba(input_array)[0] if hasattr(model, 'predict_proba') else None

        st.subheader("Prediction Result")
        if prediction[0] == 1:
            st.markdown("<div class='result-phishing'>🚨 **PHISHING DETECTED!** 🚨</div>", unsafe_allow_html=True)
            if prediction_proba is not None:
                st.write(f"Confidence (Phishing): **{prediction_proba[1]*100:.2f}%**")
        else:
            st.markdown("<div class='result-not-phishing'>✅ **NO PHISHING DETECTED.** ✅</div>", unsafe_allow_html=True)
            if prediction_proba is not None:
                st.write(f"Confidence (Not Phishing): **{prediction_proba[0]*100:.2f}%**")
    except Exception as e:
        st.error(f"Error during prediction: {e}")

st.markdown("---")
st.caption("Disclaimer: Educational tool only. Accuracy depends on the model and training data.")
