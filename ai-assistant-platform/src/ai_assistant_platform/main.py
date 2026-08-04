"""Application entry point for the AI assistant platform."""

from ai_assistant_platform.core.logging import setup_logging


def main() -> None:
    """Initialize logging and start the AI assistant platform."""
    setup_logging()
    print("ai-assistant-platform ready")


if __name__ == "__main__":
    main()
