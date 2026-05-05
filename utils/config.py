import yaml
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger()

def load_config():
    path = Path("config/default.yaml")
    if not path.exists():
        logger.warning("Config not found, using defaults")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}