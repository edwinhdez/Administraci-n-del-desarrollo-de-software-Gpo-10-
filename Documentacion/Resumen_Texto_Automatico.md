# SCRUM‑42 · Resumen automático del texto ingresado

## Historia de Usuario

**Como** usuario del chatbot (*Chatbot‑Emociones*)
**Quiero** que el sistema me devuelva un **resumen** claro y conciso del texto que proporciono
**Para** comprender rápidamente la idea principal sin leer el documento completo.

---

## Criterios de Aceptación

| Nº | Criterio                                                                                                                         | Prioridad |
| -- | -------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1  | El usuario ingresa o pega un bloque de texto ≥ 50 palabras y presiona **«Resumen»**.                                             | Alta      |
| 2  | El chatbot devuelve un resumen en ≤ 25 % del tamaño original (máx. 150 palabras).                                                | Alta      |
| 3  | El resumen mantiene ideas clave, tono y coherencia; no introduce información externa ni citas literales extensas (>20 palabras). | Alta      |
| 4  | Si el texto es < 50 palabras, el sistema advierte que el contenido es muy corto para resumir.                                    | Media     |
| 5  | El tiempo de respuesta no supera los 5 s con GPU y 15 s sin GPU en <1 000 palabras.                                              | Media     |
| 6  | El resultado se muestra en la UI Gradio, con opción de copiar al portapapeles.                                                   | Baja      |

---

## Definición de «Hecho» (DoD)

* [ ] Criterios de aceptación cumplidos y validados por QA.
* [ ] Pruebas unitarias (>90 % coverage) para `llm_chain_wrapper.run()` con parámetro `summarize=True`.
* [ ] Prueba end‑to‑end desde la UI: carga de texto → resumen mostrado.
* [ ] Documentación actualizada (`README.md` y `/docs/usage.md`).
* [ ] Despliegue estable en entorno de staging.

---

## Diseño Técnico

```mermaid
flowchart LR
    subgraph Chatbot
        A[Usuario UI<br>Gradio] -- texto --> B(aichat.py)
        B --> C{{sentiment_analyzer.analyze<br>use_gpt4o=True<br>summarize=True}}
        C -->|«sentiment»| D[llm_chain_wrapper.run<br>prompt="summary_template"]
        subgraph RAG
            E[retriever_manager<br>(ChromaDB)] -- context --> D
            D -- respuesta JSON --> B
        end
    end
```

**Puntos clave:**

* La clase `AIChat` ahora llama a `sentiment_analyzer.analyze(..., summarize=True)` para generar *contexto resumido*.
* `llm_chain_wrapper` usa **LangChain LLM** con un *prompt* de resumen (`summary_template.jinja`).
* La longitud del resumen está regulada con `max_tokens=200` y una *stop sequence* `"***"`.

---
