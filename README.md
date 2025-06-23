# LinkedIn Career Agent 🚀

This AI chatbot is designed to help you optimize your LinkedIn profile to better match specific job roles. Built with Streamlit for the user interface, Apify for profile scraping, and Krutrim Cloud (DeepSeek-R1) for AI capabilities, it allows you to analyze your profile, get job fit evaluations, and receive suggestions for rewriting your content to boost your chances.

## Features

  * **LinkedIn Profile Scraping**: Easily pull your LinkedIn profile data using a URL.
  * **Profile Analysis**: Get an AI-powered analysis of your current LinkedIn profile.
  * **Job Fit Evaluation**: Compare your profile against a target job role to see how well you match.
  * **Profile Rewriting Suggestions**: Receive AI-generated suggestions to improve and rewrite sections of your profile for a better fit with your desired job.
  * **Interactive Chat Interface**: Engage with the agent through a user-friendly Streamlit chat.

## Setup Instructions

Follow these steps to get your LinkedIn Career Agent up and running.

### Prerequisites

  * Python 3.11
  * An Apify account and API token.
  * A Krutrim Cloud account and API key.

### 1\. Clone the Repository

```bash
git clone https://github.com/Shashwat-Akhilesh-Shukla/Linkedin_Chat_System
```

### 2\. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add your API keys:

```
TOKEN_APIFY="YOUR_APIFY_API_TOKEN"
API_KEY="YOUR_KRUTRIM_CLOUD_API_KEY"
```

### 3\. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```
```
streamlit
openai
langchain
langgraph
langgraph-checkpoint-sqlite
apify-client
krutrim-cloud
```

### 4\. Run the Application

Once dependencies are installed and environment variables are set, run the Streamlit application:

```bash
streamlit run app.py
```

This will open the application in your web browser.

## How to Use

1.  **Enter LinkedIn Profile URL**: In the Streamlit app, paste the URL of the LinkedIn profile you want to analyze.
2.  **Enter Target Job Role**: Provide the job role you are aiming for (e.g., "Senior Software Engineer," "Data Scientist").
3.  **Analyze Profile**: Click the "Analyze Profile" button. The application will scrape the profile data.
4.  **Start Chatting**: Once the profile is scraped, you can ask questions or give commands in the chat input, such as:
      * "Analyze my profile."
      * "How well does my profile match a Data Scientist role?"
      * "Rewrite my experience section to better suit a Product Manager role."

The AI agent will then process your request and provide a relevant response based on the scraped profile data and the target job role.
