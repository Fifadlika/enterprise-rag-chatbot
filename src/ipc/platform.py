"""Platform detection and IPC socket path resolution."""

import sys
from pathlib import Path


UNIX_SOCKET_PATH = "/var/run/epson-chatbot/rag"
WINDOWS_PIPE_NAME = r"\\.\pipe\epson-chatbot-rag"


def is_windows() -> bool:
    """Returns True if the process is running on Windows.

    Returns:
        True if the platform is Windows, False otherwise.
    """
    ...


def get_socket_path() -> str:
    """Returns the IPC socket path appropriate for the current platform.

    Returns:
        Unix Domain Socket path on Linux, or Named Pipe path on Windows.
    """
    ...


def ensure_socket_dir(path: str) -> None:
    """Ensures that the parent directory of the socket path exists.

    Args:
        path: Socket path whose parent directory will be created.
    """
    ...


def cleanup_stale_socket(path: str) -> None:
    """Removes a stale socket file left over from a previous process.

    Only relevant on Linux. Ignored on Windows.

    Args:
        path: Path to the socket file to be removed if it exists.
    """
    ...