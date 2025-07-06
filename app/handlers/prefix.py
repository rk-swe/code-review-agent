import logging

from dotenv import load_dotenv


def run_prefix():
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: [%(asctime)s] [%(name)s.%(module)s:%(lineno)s] %(message)s",
    )
