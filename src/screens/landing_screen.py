import streamlit as st


def landing_screen():

   

    # ---------------------------
    # STYLES
    # ---------------------------
    st.markdown("""
    <style>
    .navbar{
        background:#000000;
        padding:20px 40px;
        border-radius:20px;
        margin-bottom:30px;
    }

    .logo{
        color:white;
        font-size:40px;
        font-weight:700;
    }

    .feature-card{
        background:#111827;
        padding:25px;
        border-radius:20px;
        height:280px;
        border:1px solid #374151;
    }
    .feature-card h3{ color:white; }
    .feature-card p{ color:#d1d5db; }
    .feature-icon{ font-size:40px; }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------
    # NAVBAR
    # ---------------------------
    st.markdown("""
    <div class="navbar">
        <div class="logo">🎓 SnapClass</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------
    # HERO SECTION
    # ---------------------------
    st.markdown("<h3 style='text-align:center;'>Welcome to SnapClass</h3>", unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align:center;font-size:64px;'>
    AI Powered Attendance <span style='color:#7C3AED;'>System</span>
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center;font-size:22px;max-width:900px;margin:auto;'>
    Revolutionizing the classroom with next-gen computer vision and voice biometrics.
    Trusted by educators for speed, accuracy, and security.
    </p>
    """, unsafe_allow_html=True)

    # ---------------------------
    # CTA BUTTON (IMPORTANT CHANGE)
    # ---------------------------
    # ---------------------------
    # CTA BUTTON (IMPORTANT CHANGE)
    # ---------------------------
    c1, c2, c3 = st.columns([2, 2, 2])

    with c2:
        if st.button("🚀 Start AI Attendance", use_container_width=True):
            # 1. Tell app.py that the user bypassed the landing page
            st.session_state['started'] = True
            
            # 2. Set your default destination screen (e.g., 'student' or None for home_screen)
            st.session_state['login_type'] = None  # Or 'student', depending on where you want them to land
            st.rerun()

    with c2:
        if st.button("Explore Journey", use_container_width=True):
            st.info("Scroll down to explore the platform details.")

    # ---------------------------
    # FEATURES
    # ---------------------------
    st.markdown("<h2 style='text-align:center;'>Innovative Features</h2>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📸</div>
            <h3>AI Face Analysis</h3>
            <p>Instant recognition from class photo using neural embeddings.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3>Sequential Voice ID</h3>
            <p>Real-time voice biometric verification for attendance marking.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3>QR-Driven Roster</h3>
            <p>Instant enrollment via QR-based class joining system.</p>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------
    # TEACHER STEPS
    # ---------------------------
    teacher_steps = [
        ("Step 01", "Secure Login", "Encrypted authentication system."),
        ("Step 02", "Dashboard", "Unified attendance control panel."),
        ("Step 03", "Course Setup", "One-click subject creation."),
        ("Step 04", "Face Attendance", "AI-based class scan."),
        ("Step 05", "Voice Attendance", "Sequential voice matching."),
        ("Step 06", "Reports", "Download analytics & logs.")
    ]

    for step, title, desc in teacher_steps:
        st.info(step)
        st.subheader(title)
        st.write(desc)
        st.divider()

    # ---------------------------
    # TECH STACK
    # ---------------------------
    st.markdown("---")

    st.markdown("""
    <h4 style='text-align:center;color:#8b5cf6;'>— Backend —</h4>
    <h1 style='text-align:center;'>Tech Stack</h1>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.info("⚡ Platform")
        st.subheader("Streamlit + Flask")
        st.write("Frontend + backend hybrid architecture.")

        st.info("👁️ Vision AI")
        st.subheader("Face Recognition")
        st.write("Dlib-based facial embedding system.")

    with col2:
        st.info("🎙️ Audio AI")
        st.subheader("Voice Embeddings")
        st.write("Speaker identification via ML embeddings.")

        st.info("☁️ Storage")
        st.subheader("Cloud DB")
        st.write("Secure real-time database backend.")

    # ---------------------------
    # FINAL CTA
    # ---------------------------
    
