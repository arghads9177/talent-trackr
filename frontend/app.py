import streamlit as st
from streamlit import session_state as ss
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import backend modules
from backend import database, ats_backend

st.set_page_config(page_title="TalentTrackr", layout="centered")

# Initialize session state variables
if "authenticated" not in ss:
    ss.authenticated = False
if "username" not in ss:
    ss.username = ""
if "page" not in ss:
    ss.page = "signin"  # Default page

def reload_page():
    st.rerun()  # Immediate reload
    # if ss.page == "signin":
    #     signin()
    # elif ss.page == "signup":
    #     signup()

def signup():
    st.subheader("Sign Up")
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if firstname and lastname and email and username and password:
            success, message = database.create_user(firstname, lastname, email, username, password)
            if success:
                st.success(message)
                st.info('You can now sign in from the Sign In Page.')
                ss.page = "signin"
                # st.set_query_params(page="signin")
                reload_page()
            else:
                st.error(message)
        else:
            st.error("All fields are mandatory.")
    if st.button("You already have account? Signin", type="tertiary"):
        ss.page = "signin"
        # st.set_query_params(page="signin")
        reload_page()

def signin():
    st.subheader("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        result = database.authenticate_user(username, password)
        if result["status"]:
            ss.authenticated = True
            ss.user_id = result["user_id"]
            ss.page = "home"
            # st.set_query_params(page="home")
            reload_page()
        else:
            st.error("Invalid username or password.")
    
    if st.button("Don't have an account? Signup", type="tertiary"):
        ss.page = "signup"
        # st.set_query_params(page="signup")
        reload_page()

def ats_score_generation():
    st.subheader("ATS Score Generation")
    
    if "user_id" not in ss or not ss.authenticated:
        st.warning("Please Sign In to access this feature.")
        return

    user_id = ss.user_id

    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area("Enter Job Description")

    if st.button("Generate ATS Score"):
        if resume_file and job_description:
            with st.spinner("Generating ATS Score..."):
                # score = ats_backend.generate_ats_score(user_id, resume_file, job_description)
                # st.success(f"ATS Score: {round(score * 100, 2)}%")
                result = ats_backend.evaluate_resume_ats_score(user_id, resume_file, job_description)
                st.write(result)
        else:
            st.error("Please upload a resume and enter a job description.")

def resume_summarization():
    st.subheader("Resume Summarization")
    st.write("Resume Summarization Placeholder")

def ats_friendly_resume_generation():
    st.subheader("ATS Friendly Resume Generation")
    st.write("ATS Friendly Resume Generation Placeholder")

def main():
    # query_params = st.experimental_get_query_params()
    # current_page = query_params.get("page", ["signin"])[0]
    # ss.page = current_page  # Sync with URL query params

    if not ss.authenticated:
        if ss.page == "signin":
            signin()
        elif ss.page == "signup":
            signup()
        # reload_page()
    else:
        menu = st.sidebar.radio("Menu", ["ATS Score Generation", "Resume Summarization", "ATS Friendly Resume Generation", "Sign Out"])

        if menu == "ATS Score Generation":
            ats_score_generation()
        elif menu == "Resume Summarization":
            resume_summarization()
        elif menu == "ATS Friendly Resume Generation":
            ats_friendly_resume_generation()
        elif menu == "Sign Out":
            ss.authenticated = False
            ss.username = ""
            ss.page = "signin"
            # st.set_query_params(page="signin")
            reload_page()

if __name__ == "__main__":
    main()
