import os
import argparse
from loguru import logger
from src import PATHS, config
from src.search import search

if __name__ == "__main__":

    logger.debug(f"Changing directory to {PATHS.RUN_DIR}")
    os.chdir(PATHS.RUN_DIR)

    parser = argparse.ArgumentParser(description="Literature Search")
    parser.add_argument(
        "--search",
        help="Search Google Scholar for articles from all journals using the provided query.",
        action="store_true",
    )
    parser.add_argument(
        "--snowball", help="Run snowballing on the search results.", action="store_true"
    )
    args = parser.parse_args()

    if args.search:
        search(config.QUERY)
    elif args.snowball:
        print("Snowballing not implemented yet")
        pass
