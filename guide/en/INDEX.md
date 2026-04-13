# Project Overview

[en](#) · [id](../id/INDEX.md)

## Summary

RAG-based chatbot for enterprise needs, built with LangChain and Vector Database.

---

## Overall Progress

| # | Feature | Weight | Status | Total Progress |
|---|---|---|---|---|
| 1 | Chat Response | 30% | ⚠️ 50% Done | 15% |
| 2 | Add Knowledge Base | 50% | ❌ Not Implemented | 0% |
| 3 | Delete Knowledge Base | 20% | ❌ Not Implemented | 0% |
| | **Total** | **100%** | | **15%** |

---

## Key Features

- **Chat Response** — User query → retrieve context → LLM answer.
- **Add Knowledge Base** — Upload document → embedding → store to vector DB.
- **Delete Knowledge Base** — Remove document and vectors from vector DB.

---

## Implementation Order

Recommended implementation sequence below.

1. **Chat Response**

   User query → retrieve context → LLM answer.

   Documentation: [Chat Response Feature Development Guide](./features/01-chat-response/01-chat-response.md)

2. **Add Knowledge Base**

   Upload document → chunking → embedding → store in vector DB.

   Documentation: *Not created yet*

3. **Delete Knowledge Base**

   Delete document and vectors from vector DB.

   Documentation: *Not created yet*
