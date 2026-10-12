import streamlit as st
from langchain_core.messages import HumanMessage
from ui_helpers import show_table


from langchain_anthropic import ChatAnthropic

from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import tools_condition
from graph import build_graph
from nodes import build_agent_node
from tools import get_schema, execute_sql
from llm import create_llm

# Import config and prompts
from config import SERVER, DATABASE, TABLE, MODEL
from prompts import SYSTEM_PROMPT as RAW_SYSTEM_PROMPT


# LLM and agent wiring

tools = [get_schema, execute_sql]
llm = create_llm(MODEL, max_tokens=1000)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = RAW_SYSTEM_PROMPT.replace("{TABLE}", TABLE)


# Build agent node and compile LangGraph agent from `graph.py`
agent_node = build_agent_node(llm_with_tools, SYSTEM_PROMPT)
agent = build_graph(agent_node, tools, tools_condition)

# Streamlit UI

st.title("🤖 SQL Agentic AI")
st.caption("Ask a database question. The agent decides whether to inspect schema or run SQL.")

question = st.text_input("Ask a question:", placeholder="Example: Show employees in Sales earning less than 50000")

if st.button("Run Agent") and question:
    with st.spinner("🤖 Agent is working..."):
        result = agent.invoke({"messages": [HumanMessage(content=question)]})

    st.subheader("Agent Activity")
    for message in result.get("messages", []):
        if message.type == "human":
            st.write("User: " + message.content)
        elif message.type == "ai":
            content = message.content
            if isinstance(content, list):
                parts = [b.get("text", "") for b in content if isinstance(b, dict)]
                st.write("Agent: " + " ".join(parts))
            else:
                st.write("Agent: " + str(content))
        elif message.type == "tool":
            st.write("Tool: " + message.name)
            content = message.content
            # If tool returned structured data under key "DATA", show a table
            if message.name == "execute_sql" and isinstance(content, dict) and content.get("DATA"):
                rows = content.get("DATA")
                show_table(rows)
            else:
                st.code(str(content))
