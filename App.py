import streamlit as st
import pygame
import threading
import time
from PIL import Image
import numpy as np

# Inizializza Pygame
pygame.init()

# Impostazioni Gioco
LARGHEZZA, ALTEZZA = 500, 700
ASTEROIDI = []
NAVICELLA_POS = [250, 600]
GIOCO_ATTIVO = True

# Creazione finestra di gioco (Pygame)
SCHERMO = pygame.Surface((LARGHEZZA, ALTEZZA))

# Caricamento immagini
NAVICELLA = pygame.image.load("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Space_shuttle_columbia_launching.jpg/200px-Space_shuttle_columbia_launching.jpg")
NAVICELLA = pygame.transform.scale(NAVICELLA, (50, 50))
ASTEROIDE = pygame.image.load("https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Asteroid_243_Ida_%28cropped%29.jpg/150px-Asteroid_243_Ida_%28cropped%29.jpg")
ASTEROIDE = pygame.transform.scale(ASTEROIDE, (50, 50))

def aggiorna_gioco():
    """Loop del gioco in background"""
    global ASTEROIDI, NAVICELLA_POS, GIOCO_ATTIVO
    
    while GIOCO_ATTIVO:
        SCHERMO.fill((0, 0, 0))  # Sfondo nero

        # Aggiunge nuovi asteroidi ogni secondo
        if time.time() % 1 < 0.05:
            ASTEROIDI.append([np.random.randint(0, LARGHEZZA - 50), 0])

        # Disegna la navicella
        SCHERMO.blit(NAVICELLA, (NAVICELLA_POS[0], NAVICELLA_POS[1]))

        # Muove gli asteroidi
        nuovi_asteroidi = []
        for ast in ASTEROIDI:
            ast[1] += 5
            if ast[1] < ALTEZZA:
                nuovi_asteroidi.append(ast)
            SCHERMO.blit(ASTEROIDE, (ast[0], ast[1]))
        ASTEROIDI = nuovi_asteroidi

        # Controllo collisioni
        for ast in ASTEROIDI:
            if abs(ast[0] - NAVICELLA_POS[0]) < 50 and abs(ast[1] - NAVICELLA_POS[1]) < 50:
                GIOCO_ATTIVO = False

        # Aggiorna schermo
        pygame.image.save(SCHERMO, "game.png")
        time.sleep(0.05)

# Avvia il thread del gioco
threading.Thread(target=aggiorna_gioco, daemon=True).start()

# INTERFACCIA STREAMLIT
st.title("🚀 Dodge The Asteroids!")
st.text("Muovi la navicella e evita gli asteroidi! 🔥")

col1, col2, col3 = st.columns(3)
if col1.button("⬅️"):
    NAVICELLA_POS[0] -= 20
if col3.button("➡️"):
    NAVICELLA_POS[0] += 20

st.image("game.png", caption="Gameplay in tempo reale!")

if not GIOCO_ATTIVO:
    st.error("💥 GAME OVER! Ricarica la pagina per giocare di nuovo!")
