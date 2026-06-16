# Chat Response Feature Development

[en](#) · [id](../../../id/features/01-chat-response/01-chat-response.md)

[up](../../INDEX.md)

## Overview

The **Chat Response** feature allows the backend to send queries to the RAG system and receive answers based on the knowledge base.

At a high level, the system flow is:

```
Backend
   │
   ▼
IPC Server
   │
   ▼
RAG Pipeline
   │
   ▼
LLM + Vector DB
   │
   ▼
Response → Backend
```

The backend communicates with the RAG process through **IPC**, then the query is processed by the **RAG pipeline** to generate an answer.

---

## Implementation Order

The development of this feature is carried out in two main stages.

### 1. IPC Server

Provides the **communication entry point** between the backend and the RAG process.

Main responsibilities:

* receive requests from the backend
* validate payloads
* invoke the RAG pipeline
* send responses back to the backend

Detailed documentation:

[IPC Serving Documentation](./serving-ipc.md)

---

### 2. RAG Pipeline

Implements the query processing flow to generate answers from the LLM.

Main process:

```
query
→ retrieval
→ context building
→ LLM generation
→ response

```

Detailed documentation:

[RAG Pipeline Documentation](./rag-pipeline.md)

---

## Notes

When this stage is completed, the **Chat Response feature** progress reaches **80%**.  
Its contribution to the overall RAG system progress is **24%**.

At this point, the **Chat Response feature has reached the MVP stage** and can already be used to answer user queries based on the knowledge base.

Further development will focus on:

1. Handling **replies / follow-up queries** from users  
2. **Chat object generalization**  
3. **LLM handler generalization**  
4. Adding a **handler for the Ollama LLM**
```
