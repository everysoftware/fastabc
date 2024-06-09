import os
from typing import Sequence

from dotenv import load_dotenv

from fastabc.exceptions import EnvironmentNotFound


def load_env(
    env_files: Sequence[str] = (".dev.env", ".prod.env", ".env"),
    cancel_var: str | None = "NO_ENV_FILE",
) -> str | None:
    """
    Prioritized environment loading.

    Return the loaded file path or raise an exception if no file is found.
    Return `None` if the `cancel_var` is set in the environment.
    """
    if cancel_var and os.getenv(cancel_var):
        return None
    for file in env_files:
        if load_dotenv(file):
            return file
    raise EnvironmentNotFound(f"Environment file not found: {env_files}")
