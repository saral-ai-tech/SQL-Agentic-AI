# LangGraph wiring helpers (placeholder)
# Move core graph construction logic here if splitting from app.py
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode


def build_graph(agent_node, tools, tools_condition):
    """Construct and compile the StateGraph for the agent.

    Returns the compiled agent callable.
    """
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    return graph.compile()
