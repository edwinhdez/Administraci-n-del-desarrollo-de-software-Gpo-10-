import openai
from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from loguru import logger
from langchain.chat_models import ChatOpenAI

class SentimentAnalyzer:
    def __init__(self, llm = None, openai_api_key=None, model_name="finiteautomata/bertweet-base-sentiment-analysis",  device=0):
        logger.info("[bold cyan]Initializing SentimentAnalyzer...[/bold cyan]")
        if not isinstance(model_name, str) or not model_name:
            logger.error("[bold red]model_name must be a non-empty string.[/bold red]")
            raise ValueError("model_name must be a non-empty string.")
        self.pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            tokenizer=model_name,
            device=device
        )

        self.huggingface_pipeline = None
        self.openai_api_key = openai_api_key
        self.llm = llm

    def create_huggingface_pipeline(self):
        """
        Crea y retorna un pipeline de Hugging Face para análisis de sentimientos.
        """
        logger.info("[bold cyan]Creating HuggingFacePipeline...[/bold cyan]")
        self.huggingface_pipeline = HuggingFacePipeline(pipeline = self.pipeline)
        logger.info("[bold green]HuggingFacePipeline created successfully.[/bold green]")
        return self.huggingface_pipeline

    def analyze(self, context_text, use_gpt4o=False, summarize=False):
        """
        Analiza el sentimiento de un texto y retorna el resultado.
        Si use_gpt4o=True, utiliza GPT-4o de OpenAI para el análisis.
        Si summarize=True, primero resume el contexto usando un LLM de LangChain.
        """
        logger.info("[bold cyan]Analyzing sentiment...[/bold cyan]")
        # Obtener el page_content si context_text es un documento, si no, usar el string directamente
        if hasattr(context_text, "page_content"):
            text = context_text.page_content
        else:
            text = context_text
    
        if not isinstance(text, str) or not text:
            logger.error("[bold red]context_text must be a non-empty string or have a non-empty page_content attribute.[/bold red]")
            raise ValueError("context_text must be a non-empty string or have a non-empty page_content attribute.")
    
        # Si se solicita resumen, usar el LLM de LangChain para resumir el texto
        if summarize:
            if not hasattr(self, "llm") or self.llm is None:
                logger.error("[bold red]No LLM available for summarization.[/bold red]")
                raise RuntimeError("No LLM available for summarization.")
            logger.info("[bold cyan]Summarizing context with LangChain LLM...[/bold cyan]")
            summary_prompt = f"Resume el siguiente texto en 2-3 oraciones:\n\n{text}"
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": summary_prompt}]
            )
            summary = response.choices[0].message.content
            text = summary  # Actualizar text con el resumen
            logger.info(f"[bold green]Summary completed: {summary}[/bold green]")
    
        logger.info(f"[cyan]Analyzing sentiment for context...[/cyan]")
    
        if use_gpt4o:
            if not self.openai_api_key:
                logger.error("[bold red]OpenAI API key is required for GPT-4o sentiment analysis.[/bold red]")
                raise ValueError("OpenAI API key is required for GPT-4o sentiment analysis.")
            prompt = f"Analiza el sentimiento del siguiente texto y responde solo con 'positivo', 'negativo' o 'neutral':\n\n{text}"
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            sentiment = response.choices[0].message.content
            logger.info(f"[bold green]Sentiment analysis (GPT-4o) completed: {sentiment}[/bold green]")
            return sentiment
        else:
            if not self.huggingface_pipeline:
                logger.error("[bold red]HuggingFacePipeline has not been created. Call create_huggingface_pipeline() first.[/bold red]")
                raise RuntimeError("HuggingFacePipeline has not been created. Call create_huggingface_pipeline() first.")
            sent_context_text = self.huggingface_pipeline(text)
            logger.info(f"[bold green]Sentiment analysis (HuggingFace) completed: {sent_context_text}[/bold green]")
            return sent_context_text