def ok(status_code: int, data, message: str) -> dict:
    """Build the standard {status_code, data, message} response body."""
    return {"status_code": status_code, "data": data, "message": message}
