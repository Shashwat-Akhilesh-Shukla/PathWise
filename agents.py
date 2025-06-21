import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from krutrim_cloud import KrutrimCloud

client = KrutrimCloud(api_key=os.environ.get("API_KEY"))
model_name = "DeepSeek-R1"

def krutrim_chain(template):
    def _invoke(inputs):
        chat_history = inputs.get("chat_history", [])
        history_text = "\n".join([f"{r}: {m}" for r, m in chat_history])
        rendered_prompt = template.format(**inputs)
        prompt = f"Previous chat history:\n{history_text}\n\n{rendered_prompt}" if history_text else rendered_prompt

        messages = [
            {"role": "user", "content": prompt}
        ]
        try:
            response = client.chat.completions.create(model=model_name, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    return RunnableLambda(_invoke) | StrOutputParser()

analyze_template = """
You are a LinkedIn career analyst.
Analyze this profile:
{profile}
"""

def profile_analyzer():
    return krutrim_chain(analyze_template)

jobfit_template = """
You are a job fit evaluator for LinkedIn profiles.
Compare this profile to the job role '{job}':
{profile}
"""

def job_fit_agent():
    return krutrim_chain(jobfit_template)

rewrite_template = """
You are a LinkedIn profile rewriting assistant.
Rewrite the profile to match the job role '{job}':
{profile}
"""

def rewrite_agent():
    return krutrim_chain(rewrite_template)
