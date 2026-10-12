# Tool implementations (get_schema, execute_sql)
import re
from dotenv import load_dotenv
from langchain_core.tools import tool
from config import TABLE
from db import connect_to_database

load_dotenv()


@tool
def get_schema() -> str:
    """Return columns and data types for the configured table."""
    connection = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """,
            TABLE,
        )
        rows = cursor.fetchall()
        if not rows:
            return "SCHEMA_ERROR: No columns found."
        schema = [f"{row.COLUMN_NAME} ({row.DATA_TYPE})" for row in rows]
        return "\n".join(schema)
    except Exception as e:
        return f"SCHEMA_ERROR: {str(e)}"
    finally:
        if connection:
            connection.close()


def is_safe_sql(sql: str) -> bool:
    sql = sql.strip().lower()
    if not sql.startswith("select"):
        return False
    dangerous_words = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "exec",
        "execute",
        "merge",
        "grant",
        "revoke",
    ]
    for word in dangerous_words:
        if re.search(rf"\b{word}\b", sql):
            return False
    if not re.search(rf"\b{re.escape(TABLE.lower())}\b", sql):
        return False
    return True


@tool
def execute_sql(sql: str) -> str:
    """Execute a safe SELECT query against the configured table and return results."""
    sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE).strip()
    if not is_safe_sql(sql):
        return (
            "SQL_BLOCKED\n"
            "The SQL was blocked because it is not a safe "
            "SELECT query against the allowed table."
        )
    connection = None
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(sql)
        column_names = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        if not rows:
            return (
                "QUERY_SUCCESS\n"
                "ROWS_RETURNED: 0\n"
                "No records match the requested conditions."
            )
        data = [dict(zip(column_names, row)) for row in rows[:50]]
        return (
            "QUERY_SUCCESS\n"
            f"ROWS_RETURNED: {len(rows)}\n"
            f"DATA: {data}"
        )
    except Exception as e:
        return (
            "SQL_ERROR\n"
            f"{str(e)}\n\n"
            "Analyze the SQL error and generate "
            "a corrected SELECT query."
        )
    finally:
        if connection:
            connection.close()
