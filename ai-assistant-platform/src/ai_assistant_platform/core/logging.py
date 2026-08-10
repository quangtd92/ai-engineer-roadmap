import logging

from ai_assistant_platform.core.middleware import request_id_var


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get("-")
        return True


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.FileHandler("logs.log")
    handler.addFilter(RequestIDFilter())
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(request_id)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[handler],
        force=True,
    )
