from typing import Any, Optional

def format_currency(value: Any) -> str:
    if value is None:
        return "—"
    # If it's already numeric
    if isinstance(value, (int, float)):
        return f"${float(value):,.2f}"
    # Otherwise treat as string
    s = str(value).strip()
    if not s:
        return "—"
    try:
        return f"${float(s.replace(',', '')):,.2f}"
    except Exception:
        return s