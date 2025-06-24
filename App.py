import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time

st.title("Gioco con lo Sguardo 👀")
st.write("Sposta l'occhio nella direzione giusta per muovere l'emoji!")

# Griglia
if "pos" not in st.session_state:
    st.session_state.pos = [2, 2]  # centro griglia

# Mediapipe setup
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
cap = cv2.VideoCapture(0)

frame_placeholder = st.empty()

# Direzione dello sguardo
def get_gaze_direction(landmarks):
    right_eye = landmarks[474]  # pupilla destra approx
    x = right_eye.x
    if x < 0.4:
        return "left"
    elif x > 0.6:
        return "right"
    return "center"

# Gioco loop semplificato
for _ in range(100):  # 100 iterazioni al massimo
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    direction = "center"

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        direction = get_gaze_direction(landmarks)

    # Movimento sulla griglia
    if direction == "left":
        st.session_state.pos[1] = max(0, st.session_state.pos[1] - 1)
    elif direction == "right":
        st.session_state.pos[1] = min(4, st.session_state.pos[1] + 1)

    # Mostra frame webcam (opzionale)
    frame = cv2.resize(frame, (300, 200))
    frame_placeholder.image(frame, channels="BGR")

    # Mostra la griglia
    grid = [["⬜" for _ in range(5)] for _ in range(5)]
    x, y = st.session_state.pos
    grid[x][y] = "👁️"
    for row in grid:
        st.write(" ".join(row))

    time.sleep(1)  # aggiorna ogni secondo
