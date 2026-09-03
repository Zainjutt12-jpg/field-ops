from enum import Enum


class ResponseMessage(str, Enum):
    OK = "OK"
    CREATED = "Created successfully"
    UPDATED = "Updated successfully"
    NOT_FOUND = "Resource not found"
    FORBIDDEN = "You do not have permission to perform this action"
