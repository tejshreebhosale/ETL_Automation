import logging
from pathlib import Path


def get_logger(name: str = "elt_logger") -> logging.Logger:
    base_dir = Path(__file__).resolve().parent.parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # File Handler
    file_handler = logging.FileHandler(
        log_dir / "execution.log", mode="a", encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Console Handler (IMPORTANT - you were missing this)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(levelname)s | %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger