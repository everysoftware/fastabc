from abc import ABC


class AbstractGateway(ABC):
    """
    Provides access to application services.

    e.g.::

        async def get_user(
            email: str, gateway: Annotated[Gateway, Depends(get_gateway)]
        ) -> None:
            user = await gateway.users.get_by_email(email)
            return user


        async def handler(message: types.Message, gateway: Gateway) -> None:
            user = await gateway.users.get_by_email(message.text)
            await message.answer(user.model_dump_json())
    """  # noqa: E501
