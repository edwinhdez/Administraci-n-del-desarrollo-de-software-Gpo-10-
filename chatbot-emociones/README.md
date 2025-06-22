# Chatbot‑Emociones

> **Proyecto de clase – Equipo 17 (Arquitectura de Software)**
> Sistema de *Retrieval‑Augmented Generation* (**RAG**) para **clasificación de emociones** en texto.
> **Sprint 2 (abr – jun 2025)**: ingesta refinada, UI en **Gradio**, motor vectorial **ChromaDB**, y orquestación de LLM con **LangChain**.

---

## ✨  Logros del Sprint 2

| Feature                                       | Estado | Notas breves                             |
| --------------------------------------------- | :----: | ---------------------------------------- |
| Pipeline de ingesta PDF → chunks → embeddings |    ✅   | Sentence‑Transformers *all‑MiniLM‑L6‑v2* |
| Almacenamiento vectorial en ChromaDB          |    ✅   | HNSW (M=32, ef=200)                      |
| Servicio RAG (retriever + LLM)                |    ✅   | LangChain LLM wrapper                    |
| UI en Gradio                                  |    ✅   | Conversación tipo chat                   |
| Clasificación emocional (8 clases)            |    ✅   | *sentiment\_analyzer.py*                 |

---

## 📁  Estructura del Repositorio

```text
chatbot-emociones/
├── app/                 # Capa de presentación (Gradio)
├── data/
│   └── pdfs/            # Documentos fuente para ingesta
├── helpers/             # Archivos de apoyo (cuda.txt, others.txt)
├── src/
│   ├── config/          # YAML y settings del proyecto
│   ├── ingest/          # Loaders, splitters y utilidades de ingesta
│   ├── models/          # sentiment_analyzer.py, etc.
│   ├── pipeline/        # Orquestación RAG (llm_chain_wrapper, etc.)
│   ├── services/        # Endpoints o adaptadores externos
│   ├── utils/           # Funciones comunes de apoyo
│   └── main.py          # Punto de entrada CLI
└── README.md
```

---

## 🏗️  Arquitectura General del Sistema

```text
┌──────────────┐             ┌──────────────────────┐
│   Gradio UI  │──texto──▶︎│       aichat.py       │
└──────────────┘             └─────────────┬────────┘
                                          │  LLM (LangChain)
                           ┌──────────────▼───────────────┐
                           │     llm_chain_wrapper.py      │
                           └───────▲───────────────▲───────┘
                                   │               │
         ┌──────────────┐          │               │
         │ prompt_      │          │               │
         │ manager.py   │◀─────────┘               │
         └──────────────┘                          │
                                                   │
                          ┌────────────────────────▼─────────────┐
                          │   retriever_manager.py  (ChromaDB)   │
                          └────────────────┬─────────────────────┘
                                           │
                ┌──────────────────────────▼────────────────────┐
                │ chroma_db_manager.py  +  MiniLM embeddings     │
                └───────────────────────────────────────────────┘
```

* El **usuario** interactúa mediante la UI en *Gradio* (`app/aichat.py`).
* El **LLM** se envuelve a través de `llm_chain_wrapper.py`, usando **LangChain** para abstraer el proveedor (e.g. Together AI, OpenAI, etc.).
* `retriever_manager.py` recupera los chunks más relevantes desde **ChromaDB**, alimentando al LLM con contexto.
* Los vectores se generan con *Sentence‑Transformers* y se almacenan vía `chroma_db_manager.py`.

---

## ⚙️  Instalación Rápida (Entorno Local)

```bash
# 1. Clona el repo y entra al directorio
$ git clone https://github.com/<tu‑usuario>/chatbot-emociones.git
$ cd chatbot-emociones

# 2. Crea entorno y depende
$ python -m venv .venv && source .venv/bin/activate  # Linux/macOS
# o
$ py -m venv .venv && .venv\Scripts\activate         # Windows

$ pip install -r requirements.txt

# 3. Arranca la UI
$ python app/aichat.py
```

> **Nota**: Para ejecutar GPU con CUDA, revisa `helpers/cuda.txt` y ajusta las versiones de *torch*.

---

## 🛣️  Roadmap (Sprint 3 en adelante)

1. **Mejorar UX** – botones de carga de PDF en UI, barra de progreso.
2. **Fine‑tuning** del analizador emocional con dataset propio.
3. **Resumen automático** de textos extensos (chain adicional en LangChain).
4. Despliegue en Azure / GCP con CI/CD.

---

## 👥  Equipo

| Alumno                          | Matrícula |
| ------------------------------- | --------- |
| Gustavo Adolfo Morales García   | A00828432 |
| Luis Axel González Hernández    | A01795321 |
| Ignacio José Aguilar García     | A00819762 |
| Edwin David Hernández Alejandre | A01794692 |

---

© Jun 2025 – Tec de Monterrey. Proyecto académico, uso educativo.
