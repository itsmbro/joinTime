import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(layout="wide")
st.title("Controllo con lo sguardo su video registrato 👁️")

uploaded_file = st.file_uploader("Carica un video MP4", type=["mp4"])

if uploaded_file:
    # Carica video in memoria temporanea
    tfile = open("temp_video.mp4", 'wb')
    tfile.write(uploaded_file.read())

    # Setup Mediapipe
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

    cap = cv2.VideoCapture("temp_video.mp4")

    # Inizializza posizione griglia
    if "pos" not in st.session_state:
        st.session_state.pos = [2, 2]  # centro griglia 5x5

    frame_display = st.empty()
    grid_display = st.empty()

    def get_direction(landmarks):
        eye = landmarks[468]  # pupilla approx
        x = eye.x
        if x < 0.4:
            return "left"
        elif x > 0.6:
            return "right"
        return "center"

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        direction = "center"
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            direction = get_direction(landmarks)

        # Movimento semplice su griglia
        if direction == "left":
            st.session_state.pos[1] = max(0, st.session_state.pos[1] - 1)
        elif direction == "right":
            st.session_state.pos[1] = min(4, st.session_state.pos[1] + 1)

        # Mostra frame
        resized = cv2.resize(frame, (400, 300))
        frame_display.image(resized, channels="BGR")

        # Griglia 5x5
        grid = [["⬜" for _ in range(5)] for _ in range(5)]
        x, y = st.session_state.pos
        grid[x][y] = "👁️"
        grid_display.write("\n".join([" ".join(row) for row in grid]))

        # Attendi un po’ per simulare frame-by-frame
        cv2.waitKey(100)

    cap.release()
