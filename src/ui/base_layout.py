import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #5865F2 !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: #E0E3FF !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            :root {
                --snap-primary: #5865F2;
                --snap-accent: #EB459E;
                --snap-bg: #E0E3FF;
                --snap-text: #1F2340;
                --snap-muted: #4B527A;
                --snap-surface: #FFFFFF;
            }

                
         /* Hide Top Bar of streamlit */
                
            #MainMenu, footer, header {
                visibility: hidden;
            }

            .stApp {
                color: var(--snap-text) !important;
            }
                
            .block-container {
                padding-top:1.5rem !important;
                padding-bottom:2rem !important;
                max-width: 1040px;
            }

            h1 {
                font-family: 'Outfit', sans-serif !important;
                color: var(--snap-text) !important;
                font-size: 3rem !important;
                font-weight: 900 !important;
                line-height:1.08 !important;
                margin-bottom:0.75rem !important;
            }
                

            h2 {
                font-family: 'Outfit', sans-serif !important;
                color: var(--snap-text) !important;
                font-size: 2rem !important;
                font-weight: 850 !important;
                line-height:1.15 !important;
                margin-bottom:0.7rem !important;
            }
                
            h3, h4, h5, h6, p, label, span, div {
                font-family: 'Outfit', sans-serif;
            }

            h3, h4, h5, h6,
            p, label,
            .stMarkdown, .stMarkdown p,
            div[data-testid="stText"],
            div[data-testid="stCaptionContainer"],
            div[data-testid="stWidgetLabel"] p {
                color: var(--snap-text) !important;
            }

            .stMarkdown p,
            div[data-testid="stCaptionContainer"],
            div[data-testid="stWidgetLabel"] p {
                font-size: 1rem !important;
                font-weight: 600 !important;
                line-height: 1.45 !important;
            }

            div[data-testid="stAlert"] p {
                color: inherit !important;
                font-weight: 700 !important;
            }

            input, textarea,
            div[data-baseweb="select"] * {
                color: var(--snap-text) !important;
                font-family: 'Outfit', sans-serif !important;
            }

            input::placeholder,
            textarea::placeholder {
                color: #6B7195 !important;
                opacity: 1 !important;
            }

            div[data-testid="stTextInput"] label p,
            div[data-testid="stSelectbox"] label p,
            div[data-testid="stFileUploader"] label p,
            div[data-testid="stCameraInput"] label p,
            div[data-testid="stAudioInput"] label p {
                color: var(--snap-text) !important;
                font-weight: 800 !important;
                font-size: 1rem !important;
            }

            div[data-testid="stFileUploader"] {
                color: var(--snap-text) !important;
            }
                

            button{
                border-radius: 1.5rem !important;
                background-color: var(--snap-primary) !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: var(--snap-accent) !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 800 !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform :scale(1.05)}

            @media (max-width: 720px) {
                .block-container {
                    padding-left: 1rem !important;
                    padding-right: 1rem !important;
                }

                h1 {
                    font-size: 2.1rem !important;
                }

                h2 {
                    font-size: 1.55rem !important;
                }
            }
        </style>  

                """
            ,unsafe_allow_html=True)
