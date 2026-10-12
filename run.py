# Lightweight runner for the app
from app import agent

if __name__ == "__main__":
    # simple interactive runner (placeholder)
    question = input("Ask a question: ")
    result = agent.invoke({"messages": [{"type": "human", "content": question}]})
    print(result)
