import logging
import sys

def setup_logging():
    root = logging.getLogger()

    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
            )
        )
        root.addHandler(handler)

    root.setLevel(logging.INFO)

    logging.getLogger("Odin").info("=" * 60)
    logging.getLogger("Odin").info("Asgard Realms logging initialized.")
    logging.getLogger("Odin").info("=" * 60)