# Pengembangan Fitur Respon Chat

[en](../../../en/features/01-chat-response/01-chat-response.md) · [id](#)

[up](../../INDEX.md)

## Ringkasan

Fitur **Respon Chat** memungkinkan backend mengirim query ke sistem RAG dan menerima jawaban berbasis knowledge base.

Secara garis besar, alur sistem:

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

Backend berkomunikasi dengan proses RAG melalui **IPC**, kemudian query diproses oleh **RAG pipeline** untuk menghasilkan jawaban.

---

## Urutan Implementasi

Pengembangan fitur ini dilakukan dalam dua tahap utama.

### 1. IPC Server

Menyediakan **pintu masuk komunikasi** antara backend dan proses RAG.

Tugas utama:

* menerima request dari backend
* memvalidasi payload
* memanggil pipeline RAG
* mengirim response kembali ke backend

Dokumentasi detail:

[Dokumentasi Menyediakan IPC](./serving-ipc.md)

---

### 2. RAG Pipeline

Mengimplementasikan alur pemrosesan query hingga menghasilkan jawaban dari LLM.

Proses utama:

```
query
 → retrieval
 → context building
 → LLM generation
 → response
```

Dokumentasi detail:

[Dokumentasi RAG Pipeline](./rag-pipeline.md)

---

Berikut versi yang **lebih rapi dan konsisten** bahasanya, tanpa menambah panjang.

---

## Catatan

Saat tahap ini selesai, progress **fitur Chat Response** mencapai **80%**.
Kontribusinya terhadap progress keseluruhan sistem RAG adalah **24%**.

Pada titik ini, fitur **Chat Response sudah mencapai tahap MVP** dan dapat digunakan untuk menjawab query user berbasis knowledge base.

Pengembangan selanjutnya akan berfokus pada:

1. Menangani **balasan / follow-up query** dari user
2. **Generalisasi objek chat**
3. **Generalisasi handler LLM**
4. Menambahkan **handler untuk LLM Ollama**