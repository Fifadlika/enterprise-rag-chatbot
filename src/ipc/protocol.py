"""Serialization and deserialization of IPC messages using length-prefix framing."""

import socket
from typing import Any

"""Implemented in a future version."""
# def encode_message(data: dict[str, Any]) -> bytes:
    """Convert a dict to bytes with a length-prefix header (4 bytes, big-endian).

    Args:
        data: Dict to be encoded into JSON bytes.

    Returns:
        Bytes formatted as: [4-byte length][JSON payload].
    """
    # ...


"""Implemented in a future version."""
# def decode_message(raw: bytes) -> dict[str, Any]:
    """Parse JSON bytes into a dict.

    Args:
        raw: JSON payload bytes without the length-prefix header.

    Returns:
        Decoded dict.
    """
    # ...


def read_message(conn: socket.socket) -> dict[str, Any]:
    """Read one complete message from a socket connection.

    First reads the 4-byte header to determine the payload length,
    then reads the payload with that number of bytes.

    Args:
        conn: Active socket connection from the client.

    Returns:
        Decoded dict from the received message.
    """
    ...


def send_message(conn: socket.socket, data: dict[str, Any]) -> None:
    """Send one message to the socket connection.

    Args:
        conn: Active socket connection to the client.
        data: Dict to be sent.
    """
    ...


"""Implemented in a future version."""
# def _recv_exact(conn: socket.socket, n: int) -> bytes:
    """Read exactly n bytes from the socket, handling partial reads.

    Args:
        conn: Active socket connection.
        n:    Number of bytes that must be read.

    Returns:
        n bytes from the connection.
    """
    # ...