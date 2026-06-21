import streamlit as st

# 1. Import your landing_screen component here
from src.screens.landing_screen import landing_screen

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )
    
    # Initialize session state tracking variables
    if 'started' not in st.session_state:
        st.session_state['started'] = False

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # --- ROUTING LOGIC ---

    # 2. Check if they have clicked the "Start AI Attendance Now" button yet
    if not st.session_state['started']:
        landing_screen()  # Call your imported function
        
        # We handle query parameters here too so magic links can bypass the landing page
        join_code = st.query_params.get('join-code')
        if join_code:
            st.session_state['started'] = True
            st.rerun()
            
        return  # Stop execution here so regular screens don't render underneath

    # 3. Render application screens if app has started
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()

    # 4. Handle query parameters (e.g., auto-enrollment via link) for active sessions
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()