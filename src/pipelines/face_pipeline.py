import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st   

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() 

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec

def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []

    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1) #128 embedding
        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(int(student.get('student_id')))  # Ensure ID is an integer

    if len(X) == 0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X': X, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_student = {}

    model_data = get_trained_model()

    if not model_data or model_data == 0:
        return detected_student, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        # 1. Calculate direct Euclidean distance to ALL faces in the database to find the absolute closest match
        distances = [np.linalg.norm(np.array(student_emb) - encoding) for student_emb in X_train]
        best_match_idx = np.argmin(distances)
        best_match_score = distances[best_match_idx]
        predicted_id = y_train[best_match_idx]

        # 2. Strict Threshold: 0.50 is the perfect Sweet Spot for Dlib Face Recognition
        resemblance_threshold = 0.50

        # 3. Only accept the login if the mathematical distance is closer than the threshold
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
            
    return detected_student, all_students, len(encodings)