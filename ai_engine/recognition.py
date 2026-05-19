import cv2
from deepface import DeepFace
import streamlit as st
import tempfile
import os
import pyttsx3
from database.database import save_attendance

# =========================================
# AI VOICE ENGINE
# =========================================

engine = pyttsx3.init()

engine.setProperty('rate', 160)

engine.setProperty('volume', 1.0)

# =========================================
# SECURITY MEMORY
# =========================================

security_alert_spoken = False

# =========================================
# FACE RECOGNITION SYSTEM
# =========================================

def run_face_recognition():
    st.title("📹 Real-Time Face Recognition")

    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)

    frame_count = 0

    while True:
        frame_count += 1
        ret, frame = cap.read()

        if not ret:
            st.error("Camera not detected")
            break

        # Flip mirror
        frame = cv2.flip(frame, 1)

        try:
            # Haar Cascade pour la détection rapide des rectangles
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades +
                "haarcascade_frontalface_default.xml"
            )

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # =====================================
            # ANTI-SPOOFING CHECK
            # =====================================
            laplacian_var = cv2.Laplacian(
                gray,
                cv2.CV_64F
            ).var()

            faces = face_cascade.detectMultiScale(
                gray,
                1.1,
                4
            )

            # =====================================
            # OPTIMIZED FACE RECOGNITION
            # =====================================
            result = []

            if frame_count % 10 == 0:
                result = DeepFace.find(
                    frame,
                    db_path="dataset",
                    model_name="ArcFace",
                    enforce_detection=False,
                    silent=True
                )

            if len(result) > 0 and not result[0].empty:
                identity = result[0].iloc[0]['identity']
                distance = result[0].iloc[0]['distance']

                # Seuil de reconnaissance ArcFace (Cosine Distance) + Anti-Spoofing
                if distance < 0.35 and laplacian_var > 80:
                    
                    security_alert_spoken = False

                    # 📌 CALCUL DU CONFIDENCE SCORE PROFESSIONNEL
                    confidence = round((1 - distance) * 100, 2)
                    
                    name = os.path.basename(os.path.dirname(identity))
                    save_attendance(name)

                    # =====================================
                    # AI VOICE ASSISTANT
                    # =====================================
                    engine.say(
                        f"Welcome {name}. Attendance recorded successfully."
                    )
                    engine.runAndWait()

                    # 📌 AFFICHAGE RECTANGLE VERT + NOM & SCORE
                    for (x, y, w, h) in faces:
                        cv2.rectangle(
                            frame,
                            (x, y),
                            (x+w, y+h),
                            (0, 255, 0),
                            3
                        )

                        cv2.putText(
                            frame,
                            f"{name} | {confidence}%",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 255, 0),
                            2
                        )

                else:
                    # 📌 AFFICHAGE RECTANGLE ROUGE (SPOOF / UNKNOWN)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(
                            frame,
                            (x, y),
                            (x+w, y+h),
                            (0, 0, 255),
                            3
                        )

                        # =====================================
                        # SECURITY ALERT SYSTEM
                        # =====================================
                        if not security_alert_spoken:
                            engine.say(
                                "Warning. Unknown person detected."
                            )
                            engine.runAndWait()
                            security_alert_spoken = True

                        cv2.putText(
                            frame,
                            "SPOOF / UNKNOWN",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 0, 255),
                            2
                        )

        except Exception as e:
            # Remplacer pass par st.warning(str(e)) uniquement en cas de debug
            pass

        # RGB conversion pour l'affichage Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    cap.release()