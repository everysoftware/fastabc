from typing import Any, Iterable

from onepattern.api.schemas import ErrorDetail


def get_multi_response(examples: Iterable[ErrorDetail]) -> dict[str, Any]:
    """
    Generate a multi-response object for OpenAPI.

    Usage::

        class AlreadyExists(ErrorDetail):
            code = "ALREADY_EXISTS"
            msg = "User with this email already exists"

        class InvalidOrganization(ErrorDetail):
            code = "INVALID_ORGANIZATION"
            msg = "No such organization"

        @router.post("/", responses={
            ...,  # Other responses
            status.HTTP_400_BAD_REQUEST: get_multi_response(AlreadyExists(), InvalidOrganization())
        )
        def create_user(...) -> UserRead:
            if users.exists(user.email):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AlreadyExists()))
            if not organizations.exists(user.organization_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=InvalidOrganization())
            ...
    """  # noqa: E501
    return {
        "content": {
            "application/json": {
                "examples": {
                    example.code: {
                        "summary": example.msg,
                        "value": {"detail": example.model_dump()},
                    }
                    for example in examples
                }
            }
        },
        "model": ErrorDetail,
    }
