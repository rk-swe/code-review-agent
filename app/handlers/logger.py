import logging


def _set_up_logger() -> None:
    logger = logging.getLogger("app")
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
    logger.info("app logger setup complete.")


def get_logger() -> logging.Logger:
    _set_up_logger()
    logger = logging.getLogger("app")
    return logger
