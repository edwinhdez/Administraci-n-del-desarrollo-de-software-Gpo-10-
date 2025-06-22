#ignrorewarnings
import warnings
# Ignorar todos los LangChainDeprecationWarning
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=".*LangChainDeprecationWarning.*"
)

from loguru import logger
from dotenv import load_dotenv
import os
from utils.logger_config import LoggerConfig
from utils.utils import check_cuda
from ingest.dataloader import DocumentLoader
from ingest.chunker import DocumentChunker
from ingest.chroma_db_manager import ChromaDBManager
from langchain.document_loaders import PyPDFLoader
from pipeline.llm_wrapper import OpenAILLMWrapper
from pipeline.retriever_manager import RetrieverManager
from pipeline.llm_chain_wrapper import LLMChainWrapper
from pipeline.prompt_manager import PromptManager
from pipeline.sentiment_analyzer import SentimentAnalyzer
from pipeline.aichat import GradioChat


RECREATE_CHROMA_DB = True


def main():
    try:
        # Step 1> Se configura el logger
        LoggerConfig.configure_logger()
        logger.info("[bold cyan]Starting the chatbot-emociones application...[/bold cyan]")

        vectorstore = None

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("[bold red]OPENAI_API_KEY no encontrado en las variables de entorno.[/bold red]")
            #return

        if not openai_api_key:
            logger.error("[bold red]OPENAI_API_KEY is not set.[/bold red]")
            return
        
        # Verifica si CUDA está disponible 
        check_cuda() 
        
        if RECREATE_CHROMA_DB:
            logger.info("[bold yellow]Recreating ChromaDB...[/bold yellow]")
            # Step 2> Se carga la configuración desde el archivo config.yaml y se cargan los documentos PDF
            loader = DocumentLoader(DocumentLoader.load_config, PyPDFLoader)
            documents = loader.load_documents()

            # Step 3> Se divide los documentos en fragmentos
            chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
            split_documents = chunker.split_documents(documents)

            # Step 4> Se crea la base de datos Chroma con los fragmentos
            # Note: Ensure using ChomaDB verson chromadb==0.4.15
            chroma_db_manager = ChromaDBManager(
                path="./chatbot-emociones/src/chromadb", 
                recreate_chroma_db=RECREATE_CHROMA_DB)
            vectorstore = chroma_db_manager.create_embeddings(split_documents)

        else:
            logger.info("[bold yellow]Using existing ChromaDB...[/bold yellow]")
            vectorstore = ChromaDBManager(
                path="./chatbot-emociones/src/chromadb", 
                recreate_chroma_db=RECREATE_CHROMA_DB).load_chroma_db()
        if vectorstore is None:
            logger.error("[bold red]Failed to initialize vectorstore.[/bold red]")
            return
        else:
            logger.info("[bold green]ChromaDB initialized successfully.[/bold green]")

        # Step 5> Inicializa el wrapper del LLM de OpenAI
        llm = OpenAILLMWrapper(openai_api_key).get_llm() 

        # Step 6> Create the prompt template for the LLM
        prompt_template = PromptManager.create_prompt()
        
        # Step 7> Create HuggingFace pipeline for sentiment analysis
        sentimentAnalyzer = SentimentAnalyzer(llm, openai_api_key)
        hf_pipeline = sentimentAnalyzer.create_huggingface_pipeline()

        # Step 8> Initialize the LLMChain with the LLM and prompt template
        llmChainWrapper = LLMChainWrapper(llm, prompt_template)
        llm_chain = llmChainWrapper.get_llm_chain()

        # Step 9> Set up the retriever for the vectorstore
        #question = "Era un hombre de mediana edad, de complexión recia, buena talla, ancho de espaldas, resuelto de ademanes, firme de andadura, basto de facciones, de mirar osado y vivo, ligero a pesar de su regular obesidad, y (dígase de una vez aunque sea prematuro) excelente persona por doquiera que se le mirara."

        retriever = RetrieverManager(vectorstore, k=5)
        #context = retriever.get_context(question, k=1)

        # Step 10> Analizar el sentimiento del contexto
        #sentiment_context = sentimentAnalyzer.analyze(context, use_gpt4o=True, summarize=True)

        # Step 11> Run the chatbot with the retrieved context and sentiment analysis
        """ response = llmChainWrapper.run(
            {
                "context": context,
                "question": question,
                "sentiment": sentiment_context
            }
        ) """

        # Step 12> UI with Gradio
        logger.info("[bold cyan]Launching Gradio UI...[/bold cyan]")
        gradio_chat = GradioChat(llmChainWrapper, sentimentAnalyzer, retriever)
        gradio_chat.launch()


    except Exception as e:
        logger.error(f"[bold red]An error occurred: {e}[/bold red]")
        raise e


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Run the main function
    main()
   
   