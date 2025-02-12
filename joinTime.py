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

# Funzione per cancellare tutti i dati (solo admin)
def clear_user_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)

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

    # Funzione per riavviare la sequenza
    def restart_sequence():
        st.session_state.image_counter = 1
        st.session_state.start_time = None
        st.session_state.end_time = None

    # Interfaccia utente
    st.title("Visualizzatore di Immagini con Timer")

    # Pulsante per mostrare l'immagine successiva (disabilitato dopo la decima immagine)
    if st.session_state.image_counter <= 10:
        if st.button("Mostra Immagine Successiva"):
            load_next_image()
    else:
        st.button("Mostra Immagine Successiva", disabled=True)

    # Pulsante per riavviare la sequenza
    if st.session_state.image_counter > 10:
        if st.button("Riavvia Sequenza"):
            restart_sequence()

    # Mostra il timer se è iniziato
    if st.session_state.start_time and not st.session_state.end_time:
        elapsed_time = time.time() - st.session_state.start_time
        st.info(f"Tempo trascorso: {elapsed_time:.2f} secondi")

    # Mostra i punteggi precedenti
    if user_data[nickname]["scores"]:
        st.subheader("I tuoi punteggi precedenti:")
        for i, score in enumerate(user_data[nickname]["scores"], 1):
            st.write(f"Partita {i}: {score:.2f} secondi")

    # Pulsante per mostrare i migliori punteggi di tutti gli utenti
    if st.button("Mostra Punteggi Migliori"):
        st.subheader("Classifica Generale")
        all_scores = [(user, min(data["scores"])) for user, data in user_data.items() if data["scores"]]
        all_scores.sort(key=lambda x: x[1])  # Ordina per punteggio migliore
        for rank, (user, score) in enumerate(all_scores, 1):
            st.write(f"{rank}. {user}: {score:.2f} secondi")

    # Funzionalità speciale per admin (nickname "000")
    if nickname == "000":
        st.warning("Sei loggato come Admin.")
        if st.button("Pulisci Tutti i Dati"):
            clear_user_data()
            user_data = {}
            st.success("Tutti i dati degli utenti sono stati cancellati.")
