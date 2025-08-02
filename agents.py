import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from krutrim_cloud import KrutrimCloud
import re

client = KrutrimCloud(api_key=os.environ.get("API_KEY"))
model_name = "DeepSeek-R1"

def krutrim_chain(template):
    def _invoke(inputs):
        chat_history = inputs.get("chat_history", [])
        history_text = "\n".join([f"{r}: {m}" for r, m in chat_history])
        rendered_prompt = template.format(**inputs)
        prompt = f"Previous chat history:\n{history_text}\n\n{rendered_prompt}" if history_text else rendered_prompt
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = client.chat.completions.create(model=model_name, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    return RunnableLambda(_invoke) | StrOutputParser()

# Load comprehensive prompts from files
def load_prompt(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: {filename} not found"

analyze_template = load_prompt('analyze_prompt.txt')
jobfit_template = load_prompt('jobfit_prompt.txt')
rewrite_template = load_prompt('rewrite_prompt.txt')

# Intent classification for routing
intent_classification_template = """
You are an intent classifier for LinkedIn profile assistance. 

Analyze the user query: "{query}"

Determine the primary intent and extract relevant information:

1. **Intent**: Choose ONE from [analyze_profile, job_fit, rewrite_profile, general_chat]
2. **Section** (if rewrite_profile): Extract specific sections mentioned (headline, about, experience, skills, education, certifications, etc.)
3. **Instructions**: Any specific user requirements or preferences

Response format:
INTENT: [intent_name]
SECTION: [section_name or "general" if not specified]
INSTRUCTIONS: [user specific instructions or "none"]

Examples:
- "Analyze my profile" → INTENT: analyze_profile, SECTION: general, INSTRUCTIONS: none
- "Rewrite my about section for product manager role" → INTENT: rewrite_profile, SECTION: about, INSTRUCTIONS: none
- "Improve my headline and skills for data science" → INTENT: rewrite_profile, SECTION: headline,skills, INSTRUCTIONS: for data science
"""

def intent_classifier():
    return krutrim_chain(intent_classification_template)

def profile_analyzer():
    return krutrim_chain(analyze_template)

def job_fit_agent():
    return krutrim_chain(jobfit_template)

def rewrite_agent():
    return krutrim_chain(rewrite_template)

def extract_section_content(profile, section):
    """Extract specific section content from profile"""
    section_mapping = {
        'headline': profile.get('headline', ''),
        'about': profile.get('about', ''),
        'summary': profile.get('about', ''),
        'experience': str(profile.get('experience', [])),
        'skills': str(profile.get('skills', [])),
        'education': str(profile.get('education', [])),
        'certifications': str(profile.get('certifications', [])),
        'general': str(profile)
    }
    
    return section_mapping.get(section.lower(), str(profile))

def parse_intent_response(response):
    """Parse the intent classification response"""
    intent_match = re.search(r'INTENT:\s*(\w+)', response)
    section_match = re.search(r'SECTION:\s*([^\n]+)', response)
    instructions_match = re.search(r'INSTRUCTIONS:\s*([^\n]+)', response)
    
    intent = intent_match.group(1) if intent_match else "analyze_profile"
    section = section_match.group(1).strip() if section_match else "general"
    instructions = instructions_match.group(1).strip() if instructions_match else "none"
    
    return intent, section, instructions
