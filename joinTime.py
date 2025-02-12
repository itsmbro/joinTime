import streamlit as st
import time
from PIL import Image
import json
import os

# Configurazione iniziale
st.set_page_config(page_title="Sequenza di Immagini con Timer", layout="centered")

# File per salvare i dati degli utenti
DATA_FILE = "user_data.json"

# Carica i dati esistenti o inizializza un dizionario vuoto
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Salva i dati degli utenti su file
def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Inizializzazione dei dati degli utenti
user_data = load_user_data()

# Inserimento del nickname
nickname = st.text_input("Inserisci il tuo nickname:")
if nickname:
    if nickname not in user_data:
        user_data[nickname] = {"scores": []}
        save_user_data(user_data)

    st.success(f"Benvenuto {nickname}!")

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
            st.success(f"Hai completato la sequenza in {total_time:.2f} secondi!")

            # Salva il punteggio dell'utente
            user_data[nickname]["scores"].append(total_time)
            save_user_data(user_data)

    # Interfaccia utente
    st.title("Visualizzatore di Immagini con Timer")

    if st.button("Mostra Immagine Successiva"):
        load_next_image()

    # Mostra il timer se è iniziato
    if st.session_state.start_time and not st.session_state.end_time:
        elapsed_time = time.time() - st.session_state.start_time
        st.info(f"Tempo trascorso: {elapsed_time:.2f} secondi")

    # Mostra i punteggi precedenti
    if user_data[nickname]["scores"]:
        st.subheader("I tuoi punteggi precedenti:")
        for i, score in enumerate(user_data[nickname]["scores"], 1):
            st.write(f"Partita {i}: {score:.2f} secondi")
