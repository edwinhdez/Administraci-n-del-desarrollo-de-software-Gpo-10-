from langchain.vectorstores import Chroma
from loguru import logger
class RetrieverManager:
    def __init__(self, vectorstore: Chroma, k=3):
        logger.info("[bold cyan]Initializing RetrieverManager with Chroma vectorstore...[/bold cyan]")
        if not isinstance(vectorstore, Chroma):
            logger.error("[bold red]vectorstore must be an instance of Chroma.[/bold red]")
            raise TypeError("vectorstore must be an instance of Chroma.")
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": k})

        # Verifica cuántos documentos hay en el vectorstore
        doc_count = vectorstore._collection.count()
        print("Document count:", doc_count)
        logger.info(f"[bold cyan]Document count in vectorstore: {doc_count}[/bold cyan]")
        # Muestra los primeros documentos para depuración
        if doc_count > 0:
            docs = vectorstore._collection.get(limit=2)
            logger.info(f"[bold cyan]Primeros documentos: {docs}[/bold cyan]")

    def get_context(self, question, k=1):
        """
        Recupera los documentos más relevantes para una pregunta.
        """
        logger.info(f"[bold cyan]Retrieving context for question: {question} with k={k}...[/bold cyan]")
        if not isinstance(question, str):
            logger.error("[bold red]Question must be a string.[/bold red]")
            raise TypeError("Question must be a string.")
        
        relevant_docs = self.retriever.get_relevant_documents(question, k=k)
        if not relevant_docs:
            logger.warning("[bold yellow]No relevant documents found for the question.[/bold yellow]")
        else:
            logger.info(f"[bold green]Retrieved {len(relevant_docs)} relevant documents.[/bold green]")

        if relevant_docs:
            return relevant_docs[0]
        else:
            logger.warning("[bold yellow]No relevant documents found for the question.[/bold yellow]")
            return None
    

# Inicializa el RetrieverManager
#retriever_manager = RetrieverManager(vectorstore, k=3)

# Recupera el contexto relevante
#context = retriever_manager.get_context(question, k=1)