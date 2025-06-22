import torch
from loguru import logger
def check_cuda():
    """
    Imprime si CUDA está disponible y la versión de PyTorch instalada.
    """
    logger.info(f"[cyan]CUDA available: {torch.cuda.is_available()}[/cyan]")
    print(torch.__version__)