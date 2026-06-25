import dlib
import numpy as np
import face_recognition_models
import streamlit as st

from src.database.db import get_all_students


# ---------------------------------------------------
# Load Dlib models once and cache them
# ---------------------------------------------------
@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    shape_predictor = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    face_rec_model = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, shape_predictor, face_rec_model


# ---------------------------------------------------
# Extract face embeddings from an image
# Returns a list of 128D numpy embeddings
# ---------------------------------------------------
def get_face_embeddings(image_np):
    detector, shape_predictor, face_rec_model = load_dlib_models()
    faces = detector(image_np, 1)

    embeddings = []

    for face in faces:
        shape = shape_predictor(image_np, face)
        descriptor = face_rec_model.compute_face_descriptor(image_np, shape, 1)
        embeddings.append(np.array(descriptor))

    return embeddings


# ---------------------------------------------------
# Load all registered student face embeddings from DB
# Returns a list of dictionaries:
# [
#   {
#       "student_id": 1,
#       "name": "Akash",
#       "embedding": np.array([...])
#   },
#   ...
# ]
# ---------------------------------------------------
@st.cache_data(show_spinner=False)
def get_registered_student_embeddings():
    students = get_all_students()
    registered_students = []

    for student in students:
        face_embedding = student.get("face_embedding")

        if face_embedding:
            registered_students.append({
                "student_id": student["student_id"],
                "name": student["name"],
                "embedding": np.array(face_embedding)
            })

    return registered_students


# ---------------------------------------------------
# Refresh cached student embeddings after a new student
# is registered
# ---------------------------------------------------
def train_classifier():
    # Kept same function name so your existing student_screen
    # code does not break.
    get_registered_student_embeddings.clear()
    updated_students = get_registered_student_embeddings()
    return len(updated_students) > 0


# ---------------------------------------------------
# Predict attendance from a classroom image
#
# Returns:
# detected_students -> {student_id: True, ...}
# all_student_ids   -> [1, 2, 3, ...]
# num_faces         -> total number of faces found in image
# ---------------------------------------------------
def predict_attendance(class_image_np, resemblance_threshold=0.50):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    registered_students = get_registered_student_embeddings()

    # Number of faces detected in the classroom image
    num_faces = len(encodings)

    # If no registered students are available in DB
    if not registered_students:
        return detected_students, [], num_faces

    all_student_ids = [student["student_id"] for student in registered_students]

    # Compare every detected face embedding with all registered student embeddings
    for encoding in encodings:
        best_match_student_id = None
        best_match_distance = float("inf")

        for student in registered_students:
            stored_embedding = student["embedding"]
            distance = np.linalg.norm(stored_embedding - encoding)

            if distance < best_match_distance:
                best_match_distance = distance
                best_match_student_id = student["student_id"]

        # Accept match only if closest face is within threshold
        if best_match_student_id is not None and best_match_distance <= resemblance_threshold:
            detected_students[best_match_student_id] = True

    return detected_students, all_student_ids, num_faces
