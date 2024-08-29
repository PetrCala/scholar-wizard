import time
from loguru import logger
import pandas as pd
from src import PATHS, config
from src.libs.file_handling import load_src_file, save_search_output
from src.scholar import use_proxy
from src.libs.utils import save_metadata
from src.logs import clean_log_file 
from src.search import search_google_scholar


def search(query: str)->None:
    """Search Google Scholar for articles from a specified journal matching the provided query."""
    clean_log_file(PATHS.LIT_SEARCH_LOG_FILE)  # Clear the literature search log file upon each script execution
    logger.add(PATHS.LIT_SEARCH_LOG_FILE, rotation="10 MB", backtrace=True, diagnose=True)

    logger.info("Running literature search")

    query = query or config.QUERY
    logger.info("Using the following search query: {query}")

    df = load_src_file()
    merged_results = pd.DataFrame()
    idx = 0

    if config.USE_PROXY:
        use_proxy()

    logger.info("Starting literature search")

    for i, study in df.iterrows():
        logger.info(f"Processing journal {study["Journal"]} ({i+1}/{config.JOURNAL_COUNT})")
        search_results: pd.DataFrame = search_google_scholar(
          journal_name=study["Search Keyword"], 
          query=config.QUERY,
          idx = idx,
          save_results_to_pdf=config.SAVE_RESULS_TO_PDF
        )
        merged_results = pd.concat([merged_results, search_results], ignore_index=True)
        idx += search_results.shape[0]


    file_suffix= time.strftime("%Y%m%d-%H%M%S")
    save_search_output(merged_results, file_suffix=file_suffix)
    save_metadata(merged_results, file_suffix=file_suffix)

    logger.success("Literature search completed")


