import decimal
import datetime
import pandas as pd
import streamlit as st


def normalize_value(v):
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return v


def rows_to_dataframe(rows: list) -> pd.DataFrame:
    """Convert list-of-dicts rows to a pandas DataFrame with normalized values."""
    return pd.DataFrame([{k: normalize_value(v) for k, v in row.items()} for row in rows])


def show_table(rows: list):
    try:
        df = rows_to_dataframe(rows)
        st.table(df)
    except Exception:
        st.code(str(rows))
