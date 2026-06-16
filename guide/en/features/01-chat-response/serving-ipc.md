# Providing IPC

[en](#) · [id](../../../id/features/01-chat-response/serving-ipc.md)

[up](./01-chat-response.md#1-ipc-server)

## Project Summary

The enterprise RAG chatbot receives queries from the backend via IPC, processes them using an LLM + vector database, and returns answers via IPC as well.

---

## Goal of This Step

Provide an IPC server as the entry point for communication between the backend and the RAG process.

---

## About IPC

IPC (*Inter-Process Communication*) is a method that allows two programs to communicate on the same computer without using a network (for example HTTP or the internet).

---

## Roles

The backend acts as the IPC client. The RAG process acts as the IPC server.

---

## Socket Location

RAG creates a socket at a predefined path during startup. The backend will access that path to communicate with RAG.

| Platform | Location                                          |
| -------- | ------------------------------------------------- |
| Linux    | `/var/run/epson-chatbot/rag` (Unix Domain Socket) |
| Windows  | `\\.\pipe\epson-chatbot-rag` (Named Pipe)         |

> **Note for Linux:** The `/var/run/epson-chatbot/` directory must be created manually with root privileges if it does not already exist.

---

## Module Structure

```
src/
├── ipc/ (new)
│   ├── __init__.py  (new)
│   ├── server.py    (new)     # IPC server entry point
│   ├── handler.py   (new)     # Process incoming requests
│   ├── protocol.py  (new)     # Message serialization/deserialization
│   └── platform.py  (new)     # OS detection and socket path resolution
├── config.py
└── logger.py
```

---

## Module Structure

```
src/
├── ipc/ (new)
│   ├── __init__.py  (new)
│   ├── server.py    (new)     # IPC server entry point
│   ├── handler.py   (new)     # Process incoming requests
│   ├── protocol.py  (new)     # Message serialization/deserialization
│   └── platform.py  (new)     # OS detection and socket path resolution
├── config.py
└── logger.py
```

---

## System Flow

![System Flow](../../../asset/rag_ipc_system_flow.png)

---

## Recommended Implementation Order

---

### 1. `platform.py`

* [ ] `is_windows()` — return `true` if the platform is Windows
* [ ] `get_socket_path()` — return the platform-specific constant
* [ ] `ensure_socket_dir()` — create the parent directory using `Path.mkdir(parents=True, exist_ok=True)`; ensure there is a condition to skip this on Windows
* [ ] `cleanup_stale_socket()` — remove the socket file if it exists using `Path.unlink(missing_ok=True)`; ensure there is a condition to skip this on Windows

---

### 2. `protocol.py`

* [ ] `read_message()` — read a message using `conn.recv`
* [ ] `send_message()` — send a message using `conn.sendall()`

---

### 3. `handler.py`

* [ ] `_validate_payload()` — check that `query` exists and is not empty; ensure `k` is between 1–20
* [ ] `_build_error_response()` — return `{"ok": False, "error": message}`
* [ ] `handle_request()` — call `_validate_payload()`, then call the RAG pipeline (stub for now), return the response

> **Note:** At this stage, the RAG pipeline may be stubbed with a dummy response such as:
>
> ```
> Based on the available information, the issue may be caused by system configuration or a process that is not running correctly. Please verify that the required services are active and that there are no errors in the connection settings or the path being used. If the problem persists, try restarting the application and ensure that all dependencies are properly installed.
> ```

---

### 4. `server.py`

* [V] `_setup_socket()` — call `cleanup_stale_socket()` and `ensure_socket_dir()`, create the socket, bind to the path, then `listen()`
* [V] `_accept_connection()` — `read_message()` → `handle_request()` → `send_message()` → close connection
* [ ] `start_server()` — call `_setup_socket()`, loop `accept()`, for each incoming connection call `_accept_connection()`

---

### 5. Manual Verification

* [ ] Run `start_server()` in one terminal
* [ ] Send a dummy request from a `Backend Emulator` or a simple client script in another terminal
* [ ] Ensure the response is received correctly

---

<span style="color: gray;">← Prev</span> | [Next →](./rag-pipeline.md)