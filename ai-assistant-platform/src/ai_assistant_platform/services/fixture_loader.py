import logging
from pathlib import Path
import json

logger = logging.getLogger(__name__)
current_file = Path(__file__)

file_message_path = current_file.parents[3] / "tests" / "fixtures" / "chat_messages.json"

def load_messages():
    try:
        with open(file_message_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        logger.warning("Not found the file")

    except PermissionError:
        logger.error("File permission denied")

    except UnicodeDecodeError:
        logger.error("File encoding error")

    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in %s: %s", file_message_path, e)