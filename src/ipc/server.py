"""IPC server — accepts connections and delegates to the request handler."""

import socket
from typing import Optional


# ── Module state ───────────────────────────────────────────────────────────

_server_socket: Optional[socket.socket] = None


# ── Helpers ────────────────────────────────────────────────────────────────

def _setup_socket() -> socket.socket:
    """Create, bind, and configure the server socket for the current platform.

    Calls platform.cleanup_stale_socket() and platform.ensure_socket_dir()
    before binding.

    Returns:
        Bound and listening server socket.
    """
    
    path = platform.get_socket_path()
    platform.cleanup_stale_socket(path)
    platform.ensure_socket_dir(path)

    if platform.is_windows():
        sock = socket.socket(socket.AF_PIPE, socket.SOCK_STREAM)
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    sock.bind(path)
    return sock


def _accept_connection(conn: socket.socket) -> None:
    """Handle one request–response cycle for a single client connection.

    Reads one message via protocol.read_message(), passes the payload to
    handler.handle_request(), then sends the response via
    protocol.send_message(). Closes the connection when done.

    If the RAG handler returns no response or an error occurs, an empty
    message is sent back to the client via protocol.send_message().

    Args:
        conn: Accepted client socket.
    """
    ...


# ── Public API ─────────────────────────────────────────────────────────────

def start_server() -> None:
    """Start the IPC server and enter the connection accept loop.

    Blocking. Calls _setup_socket() once, then loops on accept().
    Each accepted connection is handled by _accept_connection().
    """

    sock = _setup_socket()
    sock.listen()
    while True:
        conn, _ = sock.accept()
        with conn:
            _accept_connection(conn)

"""Implemented in a future version."""
# def stop_server() -> None:
    """Stop the IPC server and release the socket.

    Safe to call even if the server has not been started.
    """
    # ...
