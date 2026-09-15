"""Main entry point for POD classification pipeline."""

import argparse
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run POD Classification Pipeline")
    parser.add_argument("--config", default="configs/config.yaml", help="Path to config file")
    parser.add_argument("--input", default="data/sample", help="Path to input document/images")
    args = parser.parse_args()

    logger.info("Starting POD Classification Pipeline...")
    logger.info("Config: %s | Input: %s", args.config, args.input)


if __name__ == "__main__":
    main()
