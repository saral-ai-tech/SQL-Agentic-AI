# Agent nodes for LangGraph
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage


def build_agent_node(llm_with_tools, system_prompt: str):
    """Return an `agent_node` callable that LangGraph can invoke.

    The returned function accepts a `state: MessagesState` and returns
    a dict with updated `messages` produced by the LLM.
    """

    def agent_node(state: MessagesState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    return agent_node
