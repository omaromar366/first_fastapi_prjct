import uuid

from fastapi import Request


def get_or_create_session_id(request: Request) -> tuple[str, bool]:
    session_id = request.cookies.get("session_id")

    if session_id is not None:
        return session_id, False

    new_session_id = str(uuid.uuid4())

    return new_session_id, True
