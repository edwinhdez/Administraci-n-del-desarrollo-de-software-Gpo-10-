from langchain.chat_models import ChatOpenAI
from loguru import logger
class OpenAILLMWrapper:
    def __init__(self, openai_api_key, model_name="gpt-4o", temperature=0.2, max_tokens=1000):
        logger.info("[bold cyan]Initializing OpenAILLMWrapper...[/bold cyan]")
        if not isinstance(openai_api_key, str) or not openai_api_key:
            logger.error("[bold red]openai_api_key must be a non-empty string.[/bold red]")
            raise ValueError("openai_api_key must be a non-empty string.")
        try:
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                openai_api_key=openai_api_key
            )
            logger.info(f"[bold green]OpenAI LLM initialized successfully with model: {model_name}[/bold green]")
        except Exception as e:
            logger.error(f"[bold red]Failed to initialize OpenAI LLM: {e}[/bold red]")
            raise RuntimeError(f"Failed to initialize OpenAI LLM: {e}")

    def get_llm(self):
        logger.info("[bold cyan]Returning OpenAI LLM instance...[/bold cyan]")
        return self.llm