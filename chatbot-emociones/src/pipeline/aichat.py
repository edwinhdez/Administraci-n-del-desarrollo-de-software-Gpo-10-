import gradio as gr
from langchain.document_loaders import PyPDFLoader
import requests

class GradioChat:
    def __init__(self, llm_chain_wrapper, sentiment_analyzer, retriever):
        self.llm_chain_wrapper = llm_chain_wrapper
        self.sentiment_analyzer = sentiment_analyzer
        self.retriever = retriever

    def chat(self, question, history, file_url):
        # Procesa el archivo si se carga uno
        file_info = ""
        if file_url:
            try:
                response = requests.get(file_url)
                temp_path = "temp_doc.pdf"
                with open(temp_path, "wb") as f:
                    f.write(response.content)
                file_info = f"Documento descargado de: {file_url}\n"
                # Procesa el PDF y agrégalo a la base vectorial
                loader = PyPDFLoader(temp_path)
                docs = loader.load()
                # Aquí deberías tener una función para agregar docs a tu vectorstore
                self.retriever.vectorstore.add_documents(docs)
            except Exception as e:
                file_info = f"Error al descargar o procesar el archivo: {e}\n"
    
        context = self.retriever.get_context(question, k=1)
        sentiment = self.sentiment_analyzer.analyze(context, use_gpt4o=True, summarize=True)
        response = self.llm_chain_wrapper.run({
            "context": context,
            "question": question,
            "sentiment": sentiment
        })
        context_text = context.page_content if hasattr(context, "page_content") else str(context)
        # Agrega la pregunta y respuesta al historial
        history = history or []
        # Tooltip para el contexto
        safe_context = context_text.replace('\n', ' ').replace('"', '&quot;')
        tooltip_context = (
            f"<span class='context-tooltip' title=\"{safe_context}\">Contexto</span>"
        )
        history.append((
            question,
            f"<div class='context'>{file_info}{tooltip_context}</div>"
            f"<div class='bubble'>Respuesta:<br>{response}</div>"
        ))
        chat_text = ""
        for q, r in history:
            chat_text += (
                f"<div style='margin-bottom:10px;'>"
                f"<div class='question'>Pregunta: {q}</div>"
                f"{r}"
                f"</div>"
            )

        # Inyecta el CSS al inicio del HTML (solo una vez)
        style = """
        <style>
        .chat-container {
            background: #181c24;
            border-radius: 12px;
            padding: 20px;
            /* min-height: 350px; */
            /* max-height: 400px; */
            /* overflow-y: auto; */
            border: 1px solid #23272f;
            margin-bottom: 16px;
            color: #f1f1f1;
        }
        .bubble {
            background: #232b3a;
            border-radius: 15px;
            padding: 10px 15px;
            display: inline-block;
            border: 1px solid #3b4252;
            margin-top: 8px;
            margin-bottom: 8px;
            max-width: 90%;
            color: #e0e6ed;
        }
        .question {
            font-weight: bold;
            font-size: 1.1em;
            color: #8ecae6;
            margin-bottom: 4px;
        }
        .context {
            color: #bfc9d1;
            font-size: 0.98em;
            margin-bottom: 4px;
        }
        .context-tooltip {
            text-decoration: underline dotted;
            cursor: help;
            color: #bfc9d1;
            font-size: 0.98em;
            margin-bottom: 4px;
        }
        </style>
        """
        # Envuelve todo en un div con la clase chat-container
        return f"{style}<div class='chat-container'>{chat_text}</div>", history

    def launch_old(self):
        with gr.Blocks(title="LLM RAG Chatbot Emociones") as demo:
            gr.Markdown("##LLM RAG Chatbot Emociones\nHaz preguntas y conversa con el chatbot. El historial se muestra en el mismo textbox. Puedes cargar un documento.")
            chat_output = gr.Textbox(lines=15, label="LLM RAG Chat")
            state = gr.State()
            with gr.Row():
                question = gr.Textbox(lines=2, label="Pregunta")
                file_url = gr.Textbox(lines=1, label="URL de documento (PDF)")
            send_btn = gr.Button("Enviar")
    
            def chat_wrapper(q, h, url):
                return self.chat(q, h, url)
    
            send_btn.click(
                chat_wrapper,
                inputs=[question, state, file_url],
                outputs=[chat_output, state]
            )
    
        demo.launch(share=True)

    def launch_and_load_pdf(self):
        with gr.Blocks(title="LLM RAG Chatbot Emociones") as demo:
            gr.Markdown("""
            <style>
            .chat-container {
                background: #f5f7fa;
                border-radius: 12px;
                padding: 20px;
                /* min-height: 350px; */
                /* max-height: 400px; */
                / *overflow-y: auto; */
                border: 1px solid #d1d5db;
                margin-bottom: 16px;
            }
            .bubble {
                background: #e0eaff;
                border-radius: 15px;
                padding: 10px 15px;
                display: inline-block;
                border: 1px solid #b3c6ff;
                margin-top: 8px;
                margin-bottom: 8px;
                max-width: 90%;
            }
            .question {
                font-weight: bold;
                font-size: 1.1em;
                color: #2d3748;
                margin-bottom: 4px;
            }
            .context {
                color: #4a5568;
                font-size: 0.98em;
                margin-bottom: 4px;
            }
            .context-tooltip {
                text-decoration: underline dotted;
                cursor: help;
                color: #4a5568;
                font-size: 0.98em;
                margin-bottom: 4px;
            }
                        /* Cambia el color de fondo de los textboxes */
            input[type="text"], textarea {
                background-color: #e0eaff !important;
                border: 1.5px solid #2563eb !important;
                color: #1e293b !important;
            }
            /* Cambia el color del botón principal */
            #send-btn button, .gr-button-primary {
                background-color: #2563eb !important;
                color: #fff !important;
                border: none !important;
            }
            #send-btn button:hover, .gr-button-primary:hover {
                background-color: #1d4ed8 !important;
            }
            </style>
            <h2 style="color:#ffffff;">🤖 LLM RAG Chatbot Emociones</h2>
            <p>Haz preguntas y conversa con el chatbot. El historial se muestra en el mismo panel. Puedes cargar un documento por URL para enriquecer el contexto.</p>
            """)
            chat_output = gr.HTML(label="Conversación", elem_classes="chat-container")
            state = gr.State()
            with gr.Row():
                question = gr.Textbox(lines=2, label="Pregunta", placeholder="Escribe tu pregunta aquí...")
                file_url = gr.Textbox(lines=1, label="URL de documento (PDF)", placeholder="https://ejemplo.com/archivo.pdf")
            send_btn = gr.Button("Enviar", elem_id="send-btn", variant="primary")

            def chat_wrapper(q, h, url):
                return self.chat(q, h, url)

            send_btn.click(
                chat_wrapper,
                inputs=[question, state, file_url],
                outputs=[chat_output, state]
            )

        demo.launch(share=True)

    def launch(self):
        with gr.Blocks(title="LLM RAG Chatbot Emociones") as demo:
            gr.Markdown("""
            <style>
            /* Fuerza el color azul en el botón Enviar */
            #send-btn button, 
            #send-btn > button, 
            .gr-button-primary, 
            button[data-testid="button-element"], 
            [id^="send-btn"] button, 
            [class*="primary"] {
                background-color: #2563eb !important;
                color: #fff !important;
                border: none !important;
                box-shadow: none !important;
            }
            #send-btn button:hover, 
            #send-btn > button:hover, 
            .gr-button-primary:hover, 
            button[data-testid="button-element"]:hover, 
            [id^="send-btn"] button:hover, 
            [class*="primary"]:hover {
                background-color: #1d4ed8 !important;
                color: #fff !important;
            }
            /* Resto de tu CSS... */
            .chat-container {
                background: #f5f7fa;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #d1d5db;
                margin-bottom: 16px;
            }
            .bubble {
                background: #e0eaff;
                border-radius: 15px;
                padding: 10px 15px;
                display: inline-block;
                border: 1px solid #b3c6ff;
                margin-top: 8px;
                margin-bottom: 8px;
                max-width: 90%;
            }
            .question {
                font-weight: bold;
                font-size: 1.1em;
                color: #2d3748;
                margin-bottom: 4px;
            }
            .context {
                color: #4a5568;
                font-size: 0.98em;
                margin-bottom: 4px;
            }
            .context-tooltip {
                text-decoration: underline dotted;
                cursor: help;
                color: #4a5568;
                font-size: 0.98em;
                margin-bottom: 4px;
            }
            input[type="text"], textarea {
                background-color: #e0eaff !important;
                border: 1.5px solid #2563eb !important;
                color: #1e293b !important;
            }
            </style>
            <h2 style="color:#ffffff;">🤖 LLM RAG Chatbot Emociones</h2>
            <p>Haz preguntas y conversa con el chatbot. El historial se muestra en el mismo panel.</p>
            """)
            chat_output = gr.HTML(label="Conversación", elem_classes="chat-container")
            state = gr.State()
            with gr.Row():
                question = gr.Textbox(lines=2, label="Pregunta", placeholder="Escribe tu pregunta aquí...")
            send_btn = gr.Button("Enviar", elem_id="send-btn", variant="primary")

            def chat_wrapper(q, h):
                return self.chat(q, h, None)

            send_btn.click(
                chat_wrapper,
                inputs=[question, state],
                outputs=[chat_output, state]
            )

        demo.launch(share=True)