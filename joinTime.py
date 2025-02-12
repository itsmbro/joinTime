import streamlit as st
import time
from PIL import Image


# Configurazione iniziale
st.set_page_config(page_title="Sequenza di Immagini con Timer", layout="centered")

# Inizializzazione delle variabili di stato
if 'image_counter' not in st.session_state:
    st.session_state.image_counter = 1
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

# Funzione per caricare la prossima immagine
def load_next_image():
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()  # Avvia il timer

    if st.session_state.image_counter <= 10:
        image_path = f"{st.session_state.image_counter}.jpg"
        try:
            image = Image.open(image_path)
            st.image(image, caption=f"Immagine {st.session_state.image_counter}", use_container_width=True)
        except FileNotFoundError:
            st.warning(f"Immagine {st.session_state.image_counter}.jpg non trovata.")

        st.session_state.image_counter += 1

    if st.session_state.image_counter > 10:
        if st.session_state.end_time is None:
            st.session_state.end_time = time.time()  # Ferma il timer

        total_time = st.session_state.end_time - st.session_state.start_time
        st.success(f"Hai finito il J in {total_time:.2f} secondi!")

# Interfaccia utente
st.title("Creatore di Jointssss :) <3 by MickyBi")

if st.button("falla suuuu!"):
    load_next_image()

# Mostra il timer se è iniziato
if st.session_state.start_time and not st.session_state.end_time:
    elapsed_time = time.time() - st.session_state.start_time
    st.info(f"Tempo trascorso: {elapsed_time:.2f} secondi")
