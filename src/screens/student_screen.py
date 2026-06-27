import streamlit as st
from PIL import Image
import numpy as np
import time

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)
from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    # ---------------- HEADER ----------------
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            st.session_state['user_role'] = None
            if "student_data" in st.session_state:
                del st.session_state["student_data"]
            st.rerun()

    st.space()

    # ---------------- TITLE + ENROLL BUTTON ----------------
    c1, c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject", type='primary', use_container_width=True):
            enroll_dialog()

    st.divider()

    # ---------------- FETCH SUBJECTS + ATTENDANCE ----------------
    with st.spinner("Loading your enrolled subjects..."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # ---------------- BUILD ATTENDANCE STATS MAP ----------------
    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]["total"] += 1

        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    # ---------------- HANDLE NO SUBJECTS ----------------
    if not subjects:
        st.info("You are not enrolled in any subjects yet.")
        footer_dashboard()
        return

    # ---------------- RENDER SUBJECT CARDS ----------------
    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node.get("subjects", sub_node)

        sid = sub.get("subject_id")
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def make_unenroll_callback(subject_id=sid, subject_name=sub.get("name", "this subject")):
            def unenroll_button():
                if st.button(
                    "Unenroll from this course",
                    type='tertiary',
                    use_container_width=True,
                    icon=':material/delete_forever:',
                    key=f"unenroll_{subject_id}"
                ):
                    try:
                        unenroll_student_to_subject(student_id, subject_id)
                        st.toast(f"Unenrolled from {subject_name}")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to unenroll: {e}")
            return unenroll_button

        with cols[i % 2]:
            subject_card(
                name=sub.get("name", "Unknown Subject"),
                code=sub.get("subject_code", "N/A"),
                section=sub.get("section", "N/A"),
                stats=[
                    ("📅", "Total", stats["total"]),
                    ("✅", "Attended", stats["attended"]),
                ],
                footer_callback=make_unenroll_callback()
            )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    # If student already logged in, show dashboard
    if "student_data" in st.session_state:
        student_dashboard()
        return

    # ---------------- LOGIN HEADER ----------------
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='gobackhomebtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    # ---------------- WHATSAPP / IN-APP BROWSER DETECTION ----------------
    # Safe check context headers for webview environments
    user_agent = st.context.headers.get("User-Agent", "")
    
    if "WhatsApp" in user_agent:
        st.space()
        st.error("⚠️ In-app browsers do not support FaceID scanning hardware.")
        st.info(
            "To mark your attendance, please tap the **three dots** (or menu icon) "
            "in the top-right corner of your screen and select **'Open in Browser'** "
            "(Chrome / Safari)."
        )
        footer_dashboard()
        return

    # ---------------- REGULAR FACE LOGIN FLOW ----------------
    st.header("Login using FaceID", text_alignment='center')
    st.space()
    st.space()

    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found!")
            elif num_faces > 1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s['student_id'] == student_id),
                        None
                    )

                    if student:
                        st.session_state['is_logged_in'] = True
                        st.session_state['user_role'] = 'student'
                        st.session_state['student_data'] = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognized! You might be a new student!")
                    show_registration = True

    # ---------------- REGISTRATION FLOW ----------------
    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile")
            new_name = st.text_input("Enter your name", placeholder="E.g. Hamza Rizvi")

            st.subheader("Optional: Voice Enrollment")
            st.info("Enroll your voice for voice-only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input(
                    "Record a short phrase like: I am present, my name is Akash."
                )
            except Exception:
                st.error("Audio input failed!")

            if st.button("Create Account", type='primary'):
                if not new_name:
                    st.warning("Please enter your name!")
                else:
                    with st.spinner("Creating profile..."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)

                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                              )

                            if response_data:
                                train_classifier()
                                st.session_state['is_logged_in'] = True
                                st.session_state['user_role'] = 'student'
                                st.session_state['student_data'] = response_data[0]
                                st.toast(f"Profile Created! Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Failed to create student profile.")
                        else:
                            st.error("Couldn't capture facial features for registration.")

    footer_dashboard()
