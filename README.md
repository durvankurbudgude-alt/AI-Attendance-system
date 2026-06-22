# 📸 SnapClass – AI-Powered Smart Attendance System

An automated, dual-factor biometric attendance logging system combining deep-learning facial recognition with voice acoustic profiling into an enterprise-ready, role-based Streamlit dashboard.

---

## 🚀 Features

* **Dual-Factor Biometric Verification:** Combines real-time computer vision facial matching and acoustic voice validation to completely eliminate proxying or attendance fraud.
* **High-Accuracy Face Matching:** Generates 128-dimensional vector face embeddings to accurately verify identities across diverse environments and challenging lighting conditions.
* **Acoustic Voice Profiling:** Extracts specific speaker voice print embeddings to isolate unique vocal timbres, blocking static audio playbacks or malicious identity spoofing.
* **Role-Based Portals:** Custom-tailored dashboard views optimizing the workflow for both administrators (`teacher_screen.py`) and standard tracking views (`student_screen.py`).
* **Modular Dialogue Controls:** Employs dynamic interactive modal UI components for automated onboarding, subject enrollment, voice verification tracking, and real-time ledger generation.
* **Cloud Storage & Relational Database:** Utilizes Supabase for robust PostgreSQL data logging, secure student database records, and instantaneous validation check updates.

---

## 🛠️ Tech Stack

* **Frontend & Dashboard Framework:** Streamlit
* **Computer Vision Core:** `face_recognition`, `dlib`, OpenCV
* **Voice Biometrics:** `Resemblyzer`, `librosa`
* **Database & Cloud Storage:** Supabase (PostgreSQL Relations)
* **Hosting Platforms:** Streamlit Cloud

---

## 📂 Project Architecture

```text
SNAPCLASS/
├── src/
│   ├── components/                 # Modular functional UI layout components
│   │   ├── dialog_add_photo.py     # Onboarding frame image uploader 
│   │   ├── dialog_attendance_results.py # Attendance validation verification view
│   │   ├── dialog_auto_enroll.py   # Bulk enrollment data parser
│   │   ├── dialog_create_subject.py # Class subject creation wizard
│   │   ├── dialog_enroll.py        # Student registration dialogue mapping
│   │   ├── dialog_share_subject.py # Share class rosters or tracking tables
│   │   ├── dialog_voice_attendance.py # Real-time voice feature capture modal
│   │   ├── footer.py               # Application layout footer elements
│   │   ├── header.py               # Application top navigation branding
│   │   └── subject_card.py         # Visual cards tracking specific metrics
│   ├── database/                   # Cloud data connector operations
│   │   ├── config.py               # Remote environmental state loaders
│   │   └── db.py                   # Supabase client query utilities
│   ├── pipelines/                  # Biometric extraction subroutines
│   │   ├── face_pipeline.py        # dlib 128-point vector embedding math
│   │   └── voice_pipeline.py       # Librosa/Resemblyzer acoustics logic
│   ├── screens/                    # Specialized application landing layouts
│   │   ├── home_screen.py          # Baseline centralized navigation index
│   │   ├── landing_screen.py       # Authentication gateway splash view
│   │   ├── student_screen.py       # Student dashboard biometric verification screen
│   │   └── teacher_screen.py       # Admin interface for attendance rosters
│   └── ui/                         # Custom design wrappers and frameworks
│       └── base_layout.py          # Unified system page theme layout
├── .gitignore                      # Git configuration tracking exclusions
├── app.py                          # Unified system engine initialization
└── requirements.txt                # System framework dependencies manifest

⚙️ Biometric Verification Pipeline
The authentication workflow runs through a dual-stage neural verification check inside our unified processing logic:

Visual Pass (face_pipeline.py): The system utilizes a deep learning residual network (ResNet-29) via dlib to scan the video frames captured on screen, map 68 distinct facial landmarks, and check the generated 128-point face print against authorized database records.

Acoustic Pass (voice_pipeline.py): Simultaneously, librosa processes incoming voice check-in samples, rendering Mel-frequency cepstral coefficients (MFCCs). Resemblyzer evaluates these voice matrices against baseline neural speaker profiles to authorize the identity match.

📦 Installation & Setup
1. Clone the Repository
Bash
git clone https://github.com/durvankurbudgude-alt/AI-Attendance-System.git
cd AI-Attendance-System
(Note: Replace the clone URL template parameter above with your actual separate SnapClass repository string if applicable.)

2. Set Up a Virtual Environment
Bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
3. Install Requirements
Note: Make sure your system has CMake installed locally before running the pip command to ensure a smooth compilation loop for dlib binaries.

Bash
pip install -r requirements.txt
4. Configure Cloud Secrets
Create a .env file in the root directory:

Code snippet
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_or_service_key
5. Start the Streamlit Dashboard Local Server
Bash
streamlit run app.py
☁️ Deployment Guide (Streamlit Cloud)
Commit and push your code repository cleanly to GitHub.

Log into the Streamlit Cloud Dashboard and choose New App.

Select your repository, target branch, and set the Main file path entry field to app.py.

Go to Advanced Settings ➡️ Secrets and paste your credentials inside the secure TOML configurations input field:

Ini, TOML
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_supabase_anon_or_service_key"
Click Deploy! 🚀
