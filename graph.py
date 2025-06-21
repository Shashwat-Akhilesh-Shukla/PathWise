from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, ToolExecutor, RouterNode
from agents import profile_analyzer, job_fit_agent, rewrite_agent
from langchain_core.runnables import RunnableLambda
from langgraph.checkpoint.sqlite import SqliteSaver
import os

tools = {
    "analyze_profile": profile_analyzer(),
    "job_fit": job_fit_agent(),
    "rewrite_profile": rewrite_agent()
}

executor = ToolExecutor(tools)

keywords = {
    "analyze": "analyze_profile",
    "match": "job_fit",
    "score": "job_fit",
    "rewrite": "rewrite_profile",
    "improve": "rewrite_profile"
}

def router(inputs):
    query = inputs["query"].lower()
    for k, v in keywords.items():
        if k in query:
            return v
    return "analyze_profile"

storage_path = os.path.join(os.path.dirname(__file__), "memory.sqlite")
saver = SqliteSaver.from_conn_string(f"sqlite:///{storage_path}")

builder = StateGraph()
builder.add_node("router", RouterNode(func=router))
for name in tools:
    builder.add_node(name, ToolNode(name=name, tool=executor))
    builder.add_edge(name, END)

builder.set_entry_point("router")
for name in tools:
    builder.add_conditional_edges("router", lambda x: router(x) == name, {name: lambda x: True})

career_graph = builder.compile(checkpointer=saver)
