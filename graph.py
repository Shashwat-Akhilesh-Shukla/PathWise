from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from agents import (
    profile_analyzer, job_fit_agent, rewrite_agent, 
    intent_classifier, extract_section_content, parse_intent_response
)
from langgraph.checkpoint.sqlite import SqliteSaver
import os

class CareerState(TypedDict):
    query: str
    profile: dict
    job: str
    messages: List[str]
    current_tool: str
    section: Optional[str]
    user_instructions: Optional[str]
    conversation_context: dict
    thread_id: str

# Initialize agents
analyze_agent = profile_analyzer()
job_fit_analyzer = job_fit_agent()
rewrite_analyzer = rewrite_agent()
classifier = intent_classifier()

tool_map = {
    "analyze_profile": analyze_agent,
    "job_fit": job_fit_analyzer,
    "rewrite_profile": rewrite_analyzer
}

def smart_router_node(state: CareerState) -> CareerState:
    """Intelligent router using LLM for intent classification"""
    query = state["query"]
    
    try:
        # Use LLM to classify intent
        classification_result = classifier.invoke({"query": query})
        intent, section, instructions = parse_intent_response(classification_result)
        
        state["current_tool"] = intent
        state["section"] = section
        state["user_instructions"] = instructions
        
    except Exception as e:
        # Fallback to basic analysis if classification fails
        state["current_tool"] = "analyze_profile"
        state["section"] = "general"
        state["user_instructions"] = "none"
    
    return state

def agent_node(agent_func):
    """Enhanced agent node with section-specific handling"""
    def node_func(state: CareerState) -> CareerState:
        current_tool = state["current_tool"]
        inputs = {"chat_history": state.get("messages", [])}
        
        if current_tool == "analyze_profile":
            inputs["profile"] = str(state["profile"])
            
        elif current_tool == "job_fit":
            inputs["profile"] = str(state["profile"])
            inputs["job"] = state.get("job", "")
            
        elif current_tool == "rewrite_profile":
            section = state.get("section", "general")
            original_content = extract_section_content(state["profile"], section)
            
            inputs.update({
                "profile": str(state["profile"]),
                "job": state.get("job", ""),
                "section": section,
                "original_content": original_content,
                "user_instructions": state.get("user_instructions", "none")
            })
        
        try:
            result = agent_func.invoke(inputs)
        except Exception as e:
            result = f"Error calling agent {current_tool}: {str(e)}"
        
        if "messages" not in state:
            state["messages"] = []
        
        state["messages"].append(str(result))
        
        # Update conversation context
        if "conversation_context" not in state:
            state["conversation_context"] = {}
        
        state["conversation_context"]["last_action"] = current_tool
        state["conversation_context"]["last_section"] = state.get("section")
        
        return state
    
    return node_func

def route_to_tool(state: CareerState) -> str:
    """Enhanced routing with fallback"""
    tool = state.get("current_tool", "analyze_profile")
    return tool if tool in tool_map else "analyze_profile"

# Build graph with persistence support
builder = StateGraph(CareerState)

# Add nodes
builder.add_node("router", smart_router_node)

for tool_name, agent in tool_map.items():
    builder.add_node(tool_name, agent_node(agent))

# Set entry point
builder.set_entry_point("router")

# Add conditional edges
builder.add_conditional_edges(
    "router",
    route_to_tool,
    {
        "analyze_profile": "analyze_profile",
        "job_fit": "job_fit", 
        "rewrite_profile": "rewrite_profile"
    }
)

# Add end edges
for tool_name in tool_map:
    builder.add_edge(tool_name, END)

# Compile with persistence
memory = SqliteSaver.from_conn_string(":memory:")
career_graph = builder.compile(checkpointer=memory)
