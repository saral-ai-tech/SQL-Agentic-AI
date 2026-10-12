# Utility helpers
import re

def clean_sql(sql: str) -> str:
    return re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE).strip()
