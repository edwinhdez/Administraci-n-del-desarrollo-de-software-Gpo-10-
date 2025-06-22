from langchain.chains import LLMChain
from loguru import logger

class LLMChainWrapper:
    def __init__(self, llm, prompt_template):
        logger.info("[bold cyan]Initializing LLMChain in LLMChainWrapper...[/bold cyan]")
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=prompt_template
        )

    def get_llm_chain(self):
        logger.info("[bold cyan]Returning LLMChain instance...[/bold cyan]")
        return self.llm_chain

    def run(self, inputs):
        logger.info("[bold cyan]Running LLMChain with inputs...[/bold cyan]")
        if not isinstance(inputs, dict):
            logger.error("[bold red]Inputs must be a dictionary.[/bold red]")
            raise TypeError("Inputs must be a dictionary.")
        
        response = self.llm_chain.run(inputs)
        logger.info(f"[bold green]Chatbot response: {response}[/bold green]")
        logger.info("[bold green]LLMChain run completed successfully.[/bold green]")
        return response