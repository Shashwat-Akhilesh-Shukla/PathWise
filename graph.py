from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, List
from agents import profile_analyzer, job_fit_agent, rewrite_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import os


class CareerState(TypedDict):
    query: str
    profile: dict
    job_role: str
    messages: List[str]
    current_tool: str


analyze_agent = profile_analyzer()
job_fit_analyzer = job_fit_agent() 
rewrite_analyzer = rewrite_agent()


tool_map = {
    "analyze_profile": analyze_agent,
    "job_fit": job_fit_analyzer,
    "rewrite_profile": rewrite_analyzer
}


keywords = {
    "analyze": "analyze_profile",
    "match": "job_fit", 
    "score": "job_fit",
    "rewrite": "rewrite_profile",
    "improve": "rewrite_profile"
}

def router_node(state: CareerState) -> CareerState:
    """Router node to determine which tool to use based on query"""
    query = state["query"].lower()
    
    
    selected_tool = "analyze_profile"  
    for keyword, tool_name in keywords.items():
        if keyword in query:
            selected_tool = tool_name
            break
    
    state["current_tool"] = selected_tool
    return state

def agent_node(agent_func):
    """Wrapper to create a proper node function from an agent"""
    def node_func(state: CareerState) -> CareerState:
        
        current_tool = state["current_tool"]
        
        
        inputs = {}
        if current_tool == "analyze_profile":
            inputs["profile"] = state["profile"] 
        elif current_tool == "job_fit":
            inputs["profile"] = state["profile"] 
            inputs["job"] = state["job_role"]         
        elif current_tool == "rewrite_profile":
            inputs["profile"] = state["profile"] 
            inputs["job"] = state["job_role"]         
        
        
        
        inputs["query"] = state["query"]

        try:
            
            result = agent_func.invoke(inputs)
        except Exception as e:
            result = f"Error calling agent {current_tool}: {str(e)}"
        
        
        if "messages" not in state:
            state["messages"] = []
        state["messages"].append(str(result))
        
        return state
    return node_func





builder = StateGraph(CareerState)


builder.add_node("router", router_node)

def route_to_tool(state: CareerState) -> str:
    """Conditional edge function to route to appropriate tool"""
    return state["current_tool"]


for tool_name, agent in tool_map.items():
    builder.add_node(tool_name, agent_node(agent))

builder.set_entry_point("router")

builder.add_conditional_edges(
    "router",
    route_to_tool,
    {
        "analyze_profile": "analyze_profile",
        "job_fit": "job_fit", 
        "rewrite_profile": "rewrite_profile"
    }
)

for tool_name in tool_map:
    builder.add_edge(tool_name, END)

career_graph = builder.compile()