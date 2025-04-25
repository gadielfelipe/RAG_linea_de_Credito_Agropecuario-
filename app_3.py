import streamlit as st
import requests
import json
import fitz  # PyMuPDF

st.set_page_config(page_title="Asistente Virtual Línea ANT - Finagro", page_icon="logo_finagro.png")


API_KEY = "AIzaSyAD7fHhvjm4VmGZI1AjXsmNlkXeluit5a4" 
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
HEADERS = {"Content-Type": "application/json"}

# --- Function to Extract Text from PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

pdf_text = extract_text_from_pdf("Resolucion2025.pdf")

st.image("logo_finagro.png", width=200)

st.title("¿Necesitas información sobre la Línea ANT de Finagro? Pregunta aquí sobre requisitos, condiciones y beneficiarios.")


question = st.text_input("Ingresa tu pregunta sobre la Línea ANT de Finagro:", placeholder="Ejemplo: ¿Cuáles son los requisitos para acceder?")

# --- Process Question and Call API ---
if st.button("Obtener respuesta") and question:
    with st.spinner("Buscando respuesta..."):
        # Prepare request payload
        data = {
            "contents": [{
                "parts": [
                    {"text": "Responde en español."},
                    {"text": f"Contexto: {pdf_text[:50000]}"},
                    {"text": f"Pregunta: {question}"}
                ]
            }]
        }

        # Make API request
        response = requests.post(GEMINI_URL, headers=HEADERS, data=json.dumps(data))

        if response.status_code == 200:
            try:
                answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]

                # Handle empty or irrelevant responses
                if not answer.strip() or "no se encuentra" in answer.lower() or "no está disponible" in answer.lower():
                    st.error("No se encontró información relevante para tu pregunta. Contáctenos en:\n\n"
                             "📱 WhatsApp: 3143292434\n"
                             "📧 Correo electrónico: finagro@finagro.com.co")
                else:
                    st.write("**Respuesta:**", answer)
            except (KeyError, IndexError):
                st.error("Error en la respuesta. Intente nuevamente más tarde.")
        else:
            st.error("Error: No se pudo obtener una respuesta. Intente nuevamente más tarde.")


if 'first_visit' not in st.session_state:
    st.session_state['first_visit'] = True
    st.info("¡Bienvenido! Este asistente virtual te ayudará con tus preguntas sobre la Línea ANT de Finagro.")
