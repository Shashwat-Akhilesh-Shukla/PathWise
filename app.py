import streamlit as st
from scraper import scrape_linkedin_profile
from graph import career_graph
import uuid

st.set_page_config(page_title="LinkedIn Career Agent", layout="centered")
st.title("🚀 LinkedIn Career Optimizer")

# Initialize session state with persistence support
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "job_role" not in st.session_state:
    st.session_state.job_role = ""

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "conversation_active" not in st.session_state:
    st.session_state.conversation_active = False

# Sidebar for session management
with st.sidebar:
    st.header("Session Controls")
    if st.button("🔄 Reset Conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.session_state.conversation_active = False
        st.rerun()
    
    st.write(f"Session ID: {st.session_state.thread_id[:8]}...")

# Profile setup
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
            st.session_state.conversation_active = True
            st.success("✅ Profile scraped successfully!")
            
            # Show profile summary
            with st.expander("Profile Summary", expanded=False):
                st.json(profile_data)

# Chat interface with persistence
user_input = st.chat_input("Ask anything about your career or profile...")

if user_input and st.session_state.conversation_active:
    # Prepare state for graph invocation with resume capability
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    
    initial_state = {
        "query": user_input,
        "profile": st.session_state.profile,
        "job": st.session_state.job_role,
        "messages": [],
        "thread_id": st.session_state.thread_id,
        "conversation_context": {}
    }
    
    try:
        # Invoke graph with persistence
        result_state = career_graph.invoke(initial_state, config=config)
        
        # Extract response
        if result_state.get("messages"):
            response = result_state["messages"][-1]
        else:
            response = "I apologize, but I couldn't process your request. Please try again."
        
        # Update chat history
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response))
        
    except Exception as e:
        st.error(f"Error processing request: {str(e)}")
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", f"Error: {str(e)}"))

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Instructions
if not st.session_state.conversation_active:
    st.info("👆 Please enter your LinkedIn URL and target job role to start the conversation.")
else:
    st.info("💡 You can ask me to:\n- Analyze your profile\n- Check job fit\n- Rewrite specific sections (headline, about, experience, skills, etc.)")
