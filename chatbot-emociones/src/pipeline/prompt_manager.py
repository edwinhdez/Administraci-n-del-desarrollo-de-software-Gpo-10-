from langchain.prompts import PromptTemplate
from loguru import logger
class PromptManager:
    def __init__(self):
        self.templates = {}

    @staticmethod
    def create_prompt():

        logger.info("[bold cyan]Creating prompt template for emotional analysis...[/bold cyan]")
        """
        Crea y guarda un PromptTemplate para análisis emocional con contexto y sentimiento.
        """
        template = """
        Eres experto en análisis emocional. Dado un contexto, una pregunta y el resultado de un análisis de sentimientos, proporciona una respuesta detallada usando el contexto.
        Contexto: {context}

        Resultado del análisis de sentimientos: {sentiment}

        Respuesta:

        """
        prompt_template = PromptTemplate(
            input_variables=["context", "sentiment"],
            template=template
        )
        logger.info("[bold green]Prompt template created successfully.[/bold green]")
        return prompt_template