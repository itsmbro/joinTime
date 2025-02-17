import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw

# Impostazioni
LARGHEZZA, ALTEZZA = 500, 700
NAVICELLA_X = 225
ASTEROIDI = []
GIOCO_ATTIVO = True

# Crea sfondo
def crea_sfondo():
    img = Image.new("RGB", (LARGHEZZA, ALTEZZA), "black")
    draw = ImageDraw.Draw(img)
    
    # Disegna asteroidi
    for ast in ASTEROIDI:
        draw.ellipse((ast[0], ast[1], ast[0]+50, ast[1]+50), fill="gray")

    # Disegna navicella
    draw.rectangle((NAVICELLA_X, 600, NAVICELLA_X+50, 650), fill="blue")

    return img

# Loop del gioco
def aggiorna_gioco():
    global ASTEROIDI, NAVICELLA_X, GIOCO_ATTIVO

    while GIOCO_ATTIVO:
        time.sleep(0.2)  # Velocità gioco

        # Crea nuovi asteroidi
        if np.random.rand() < 0.2:
            ASTEROIDI.append([np.random.randint(0, LARGHEZZA-50), 0])

        # Muove asteroidi
        ASTEROIDI[:] = [[x, y+20] for x, y in ASTEROIDI if y < ALTEZZA]

        # Controllo collisione
        for x, y in ASTEROIDI:
            if abs(x - NAVICELLA_X) < 50 and y > 550:
                GIOCO_ATTIVO = False
                break
        
        # Aggiorna l'immagine
        img = crea_sfondo()
        img.save("game.png")

# INTERFACCIA STREAMLIT
st.title("🚀 Dodge The Asteroids!")

col1, col2, col3 = st.columns(3)
if col1.button("⬅️") and NAVICELLA_X > 0:
    NAVICELLA_X -= 30
if col3.button("➡️") and NAVICELLA_X < LARGHEZZA - 50:
    NAVICELLA_X += 30

st.image("game.png", caption="Gameplay in tempo reale!")

# Avvia il gioco
if GIOCO_ATTIVO:
    aggiorna_gioco()
else:
    st.error("💥 GAME OVER! Ricarica la pagina per giocare di nuovo!")
