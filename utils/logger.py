import logging
from rich.console import Console
from rich.logging import RichHandler

console = Console()

def setup_logger(name: str = "ai_toolkit"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = RichHandler(console=console, rich_tracebacks=True)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger