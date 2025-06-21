import streamlit as st
from scraper import scrape_linkedin_profile
from graph import career_graph
import uuid

st.set_page_config(page_title="LinkedIn Career Agent", layout="centered")
st.title("🚀 LinkedIn Career Optimizer")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "job_role" not in st.session_state:
    st.session_state.job_role = ""
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

linkedin_url = st.text_input("Enter your LinkedIn Profile URL:")
job_role = st.text_input("Enter your Target Job Role:")

if st.button("Analyze Profile") and linkedin_url and job_role:
    with st.spinner("Scraping LinkedIn data..."):
        profile_data = scrape_linkedin_profile(linkedin_url)

    if not profile_data:
        st.error("Failed to scrape LinkedIn. Try another URL.")
    else:
        st.session_state.profile = profile_data
        st.session_state.job_role = job_role
        st.success("Profile scraped successfully!")
        st.json(profile_data)

user_input = st.chat_input("Ask something about your career profile")
if user_input:
    with st.spinner("Processing..."):
        inputs = {
            "query": user_input,
            "profile": st.session_state.profile,
            "job": st.session_state.job_role,
            "chat_history": st.session_state.chat_history,
            "config": {"configurable": {"thread_id": st.session_state.session_id}}
        }
        response = career_graph.invoke(inputs)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response["result"]))

for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)