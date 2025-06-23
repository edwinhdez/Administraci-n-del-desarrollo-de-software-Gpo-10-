# Minutas de Daily Scrum – Sprint 2
Periodo: 9 de junio al 20 de junio de 2025

## Lunes 9 de junio

* **Avances**: Se revisó el objetivo general y se refinó el backlog (SCRUM‑42, 13, 20, 24, 14, 41). Se asignaron responsables por historia.
* **Plan**: Iniciar implementación del `SentimentAnalyzer` (SCRUM‑13) y crear esqueleto de `aichat.py`.
* **Bloqueos**: Pendiente configurar API Key de OpenAI en todos los entornos.

## Martes 10 de junio

* **Avances**: `SentimentAnalyzer` operativo con GPT‑4o; primeros tests unitarios > 80 % precisión.
* **Plan**: Conectar analizador a `aichat.py` y diseñar prompt de resumen (SCRUM‑42).
* **Bloqueos**: Límite de tokens; se evaluará truncado de contexto.

## Miércoles 11 de junio

* **Avances**: Integración de sentimiento en pipeline; `llm_chain_wrapper` listo.
* **Plan**: Activar parámetro `summarize=True` y generar plantilla de prompt.
* **Bloqueos**: Inferencia local sin GPU demasiado lenta.

## Jueves 12 de junio

* **Avances**: Primeras pruebas de resumen (ROUGE‑1 0.42).
* **Plan**: Optimizar `retriever_manager` (k = 1) y mejorar logging.
* **Bloqueos**: Error CORS al cargar PDF desde la UI.

## Viernes 13 de junio

* **Avances**: Endpoint `/predict` expuesto; UI Gradio muestra sentimiento.
* **Plan**: Añadir casilla “Resumir” y mostrar output en panel separado.
* **Bloqueos**: Falta manejar textos vacíos (SCRUM‑41).

## Lunes 16 de junio

* **Avances**: Validación de texto vacío implementada; mensaje de error amigable.
* **Plan**: Terminar lógica de resumen y actualizar README (SCRUM‑14).
* **Bloqueos**: Conflictos de merge en README entre ramas.

## Martes 17 de junio

* **Avances**: README unificado; diagrama ASCII actualizado; UI movida a `app/`.
* **Plan**: Pulir estilos Gradio y preparar demo interna.
* **Bloqueos**: Dependencia `gradio-md` causa desalineación de layout.

## Miércoles 18 de junio

* **Avances**: Demo interna exitosa; tiempo medio de resumen ≈ 2.5 s.
* **Plan**: Añadir logs a archivo y GitHub Actions para tests automáticos.
* **Bloqueos**: Cuota diaria de API agotada; se usó fallback local MiniLM.

## Jueves 19 de junio

* **Avances**: Pipeline final de resumen + sentimiento integrado; accuracy 88 %.
* **Plan**: Preparar Sprint Review y Retro; cerrar issues.
* **Bloqueos**: Ninguno crítico.

## Viernes 20 de junio

* **Avances**: Todas las historias SCRUM marcadas como *Done*; tablero actualizado.
* **Plan**: Realizar Review final con equipo
* **Bloqueos**: N/A


## Sábado 21 de junio – Retrospective Meeting (Sprint 2)

**Participantes:** Todo el equipo

### ¿Qué hicimos bien?

* Se completaron las historias clave (SCRUM‑13 y SCRUM‑42) dentro del tiempo del sprint.
* El pipeline CI/CD corrió sin fallos críticos durante toda la iteración.
* La comunicación en las *dailies* se mantuvo concisa y orientada a quitar bloqueos.

### ¿Qué podemos mejorar?

* Diseñar una **interfaz de usuario más flexible** que se adapte mejor a las diferentes situaciones de uso.
* Ampliar la **cobertura de pruebas**, incluyendo más casos de error y escenarios límite para validar la robustez.
* Documentar la *Definition of Done* al inicio de cada historia para alinear expectativas y evitar re‑trabajos.

### ¿Qué haremos diferente en el próximo Sprint?

* **Investigar otros LLM** (p. ej. Mistral, Gemma) para evaluar rendimiento y coste frente a la solución actual.
* Redactar **historias SCRUM más claras y orientadas a valor**, usando plantillas homogéneas que faciliten el seguimiento.
* **Integrar completamente Jira con GitHub** (smart‑commits, PR templates) para mejorar la trazabilidad y la evidenciación del trabajo.
