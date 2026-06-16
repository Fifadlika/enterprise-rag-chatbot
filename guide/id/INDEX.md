# Project Overview

[en](../en/INDEX.md) · [id](#)

## Ringkasan

Chatbot berbasis RAG untuk kebutuhan enterprise, dibangun dengan LangChain dan Vector Database.

---

## Progress Keseluruhan

| Urutan | Fitur                 | Kontribusi | Status                 | Progress Total |
| ------ | --------------------- | ---------- | ---------------------- | -------------- |
| 1      | Respon Chat           | 30%        | ⚠️ Selesai 50%         | 15%            |
| 2      | Tambah Knowledge Base | 50%        | ❌ Belum Diimplementasi | 0%             |
| 3      | Hapus Knowledge Base  | 20%        | ❌ Belum Diimplementasi | 0%             |
|        | **Total**             | **100%**   |                        | **15%**        |

---

## Fitur Utama

* **Respon Chat** — Query user → retrieve konteks → jawaban LLM.
* **Tambah Knowledge Base** — Upload dokumen → embedding → simpan ke vector DB.
* **Hapus Knowledge Base** — Hapus dokumen dan vector dari vector DB.


---

## Urutan Pengerjaan

Rekomendasi urutan implementasi berikut.

1. **Respon Chat**

   Query user → retrieve konteks → jawaban LLM.

   Dokumentasi: [Petunjuk Pengembangan Fitur Respon Chat](./features/01-chat-response/01-chat-response.md)

2. **Tambah Knowledge Base**

   Upload dokumen → chunking → embedding → simpan ke vector DB.

   Dokumentasi: *Belum dibuat*

3. **Hapus Knowledge Base**

   Hapus dokumen dan vector dari vector DB.

   Dokumentasi: *Belum dibuat*