# SQLChat-Bot

A Streamlit app that wraps an LLM (Anthropic Claude) to query a SQL Server database safely using tools (get_schema, execute_sql).

Setup

1. Create and activate a Python virtual environment.

2. Copy `.env.example` to `.env` and fill values.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

Files

- `app.py` — Streamlit application and agent wiring
- `requirements.txt` — Python dependencies
- `.env.example` — example environment variables

Notes

This project assumes a local SQL Server reachable from the host and an Anthropic API-compatible LLM setup.
