from rest_framework.views import exception_handler


def _flatten(detail):
    if isinstance(detail, list):
        return " ".join(str(item) for item in detail)
    if isinstance(detail, dict):
        parts = []
        for key, value in detail.items():
            parts.append(f"{key}: {_flatten(value)}")
        return " ".join(parts)
    return str(detail)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        detail = response.data.get("detail", response.data)
        response.data = {
            "success": False,
            "message": _flatten(detail),
            "errors": response.data,
        }
    return response
