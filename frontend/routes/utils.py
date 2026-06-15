def get_error_message(res, default="An error occurred"):
    try:
        return res.json().get("detail", default)
    except Exception:
        return f"Server error (HTTP {res.status_code})"
