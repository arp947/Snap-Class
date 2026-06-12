import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject
import time
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def style_student_login():
    st.markdown("""
        <style>
            .student-login-hero {
                max-width: 860px;
                margin: 0 auto 1.5rem auto;
                text-align: center;
            }

            .student-login-hero h3 {
                color: #1F2340;
                font-size: 2.25rem;
                font-weight: 800;
                margin-bottom: 0.35rem;
            }

            .student-login-hero p {
                color: #4B527A;
                font-size: 1.05rem;
                margin: 0 auto;
                max-width: 560px;
            }

            .student-camera-wrap {
                max-width: 780px;
                margin: 0 auto;
            }

            div[data-testid="stCameraInput"] {
                background: #FFFFFF;
                border: 1px solid rgba(88, 101, 242, 0.18);
                border-radius: 1.4rem;
                padding: 1.1rem 1.1rem 1.25rem;
                box-shadow: 0 18px 45px rgba(31, 35, 64, 0.12);
                max-width: 780px;
                margin: 0 auto;
            }

            div[data-testid="stCameraInput"] label p {
                color: #1F2340 !important;
                font-size: 1rem !important;
                font-weight: 700 !important;
                margin-bottom: 0.65rem !important;
            }

            div[data-testid="stCameraInput"] section p,
            div[data-testid="stCameraInput"] section span,
            div[data-testid="stCameraInput"] section div {
                color: #FFFFFF !important;
            }

            div[data-testid="stCameraInput"] video,
            div[data-testid="stCameraInput"] img {
                border-radius: 1rem !important;
                max-height: 430px;
                object-fit: cover;
            }

            div[data-testid="stCameraInput"] button {
                border-radius: 0.9rem !important;
                min-height: 3rem;
                font-weight: 700 !important;
            }

            @media (max-width: 720px) {
                .student-login-hero h3 {
                    font-size: 1.7rem;
                }

                .student-login-hero p {
                    font-size: 0.95rem;
                }

                div[data-testid="stCameraInput"] {
                    padding: 0.75rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')

    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']}""")
        if st.button("Logout",type= 'secondary', key='loginbackbtn', shortcut="control + backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in subject', type='primary', width='stretch'):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total":0,"attended":0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total": 0,"attended":0})

        def unenroll_button(s=sub, s_id=sid):
            if st.button("Unenroll from this course", key=f"unenroll_{s_id}", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id, s_id)
                st.toast(f"Unenrolled from {s['name']} successfully")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📆','Total',stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()
    style_student_login()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1,c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",type= 'secondary', key='loginbackbtn', shortcut="control + backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.space()
    show_registration = False

    st.markdown("""
        <div class="student-login-hero">
            <h3>Login using Face ID</h3>
            <p>Allow camera access, keep your face centered, and take a clear photo to sign in.</p>
        </div>
        <div class="student-camera-wrap">
    """, unsafe_allow_html=True)
    photo_source = st.camera_input("Position your face in the center")
    st.markdown("</div>", unsafe_allow_html=True)

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning...'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces > 1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Arpit Singh')
            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")

            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Arpit.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type="primary"):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration')
                else:
                    st.warning('Please enter your name!')

    footer_dashboard()
