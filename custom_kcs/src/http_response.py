import frappe

def _respond(code: int, status: str, message: str | None = None, **extra):
    frappe.local.response["http_status_code"] = code
    payload = {"status": status}
    if message:
        payload["message"] = message
    if extra:
        payload.update(extra)
    return payload

def _ok(message="OK", **extra):          return _respond(200, "success", message, **extra)
def _created(message="Created", **extra): return _respond(201, "success", message, **extra)
def _bad_request(message="Bad request", **extra):   return _respond(400, "error", message, **extra)
def _forbidden(message="Forbidden", **extra):       return _respond(403, "error", message, **extra)
def _not_found(message="Not Found", **extra):       return _respond(404, "error", message, **extra)
def _conflict(message="Conflict", **extra):         return _respond(409, "error", message, **extra)
def _unprocessable(message="Unprocessable Entity", **extra): return _respond(422, "error", message, **extra)
def _server_error(message="Internal Server Error", **extra): return _respond(500, "error", message, **extra)

__all__ = [
    "_respond",
    "_ok", "_created", "_bad_request", "_forbidden",
    "_not_found", "_conflict", "_unprocessable", "_server_error",
]
