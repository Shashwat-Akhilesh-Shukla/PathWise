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
    with st.spinner("Scraping LinkedIn profile..."):
        profile_data = scrape_linkedin_profile(linkedin_url)

    if not profile_data:
        st.error("❌ Failed to scrape profile. Try a different URL or check your cookies.")
    else:
        st.session_state.profile = profile_data
        st.session_state.job_role = job_role
        st.success("✅ Profile scraped successfully!")
        st.json(profile_data)


user_input = st.chat_input("Ask anything about your career or profile...")
if user_input:
    
    state = career_graph.invoke({
        "query": user_input,
        "profile": st.session_state.profile,
        "job": st.session_state.job_role,
        "messages": [msg for msg in st.session_state.chat_history],
        "configurable": {
            "thread_id": st.session_state.session_id
        }
    })

    
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", state["messages"][-1]))


for entry in st.session_state.chat_history:
    if isinstance(entry, tuple) and len(entry) == 2:
        role, msg = entry
    else:
        role, msg = "assistant", str(entry)
    with st.chat_message(role):
        st.markdown(msg)