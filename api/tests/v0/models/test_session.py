import pytest

from src.v0.models.session import SessionData


def test_SessionData():
    SessionData(
        index="0",
        owner="John Doe",
        shared="True",
        tag=["subsurface"],
        name="this is an objective",
        description="objectively objecting the objectives",
    )

    SessionData(
        index="0",
        owner="John Doe",
        shared="False",
        tag=["subsurface"],
        name="this is an objective",
        description="objectively objecting the objectives",
    )

    SessionData(name="no name")

    with pytest.raises(Exception) as exc:
        SessionData(name="no name", shared="Nop!")
    assert "Value error, must be None or in True/False" in str(exc.value)
