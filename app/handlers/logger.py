import logging


def _set_up_logger() -> None:
    logger = logging.getLogger("code-review-agent")
    if logger.hasHandlers():
        return

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(levelname)s: [%(asctime)s] [%(name)s.%(module)s:%(lineno)s] %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info("code-review-agent logger setup complete.")


def get_logger() -> logging.Logger:
    _set_up_logger()
    logger = logging.getLogger("code-review-agent")
    return logger
