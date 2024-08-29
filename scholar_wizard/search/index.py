import os
import time
from loguru import logger
import pandas as pd
from scholar_wizard import PATHS, STATIC
from scholar_wizard.libs.file_handling import save_output
from scholar_wizard.libs.scholar_utils import setup_proxy
from scholar_wizard.libs.utils import save_metadata
from scholar_wizard.libs.logs import clean_log_file
from scholar_wizard.search import search_google_scholar


def search(
    query: str,
    output_path: str,
    journals: list[str] = None,
    save_output_to_df: bool = True,
    save_output_metadata: bool = True,
    save_results_to_pdf: bool = True,
    use_proxy: bool = True,
    date_format: str = STATIC.DATE_FORMAT,
) -> pd.DataFrame:
    """
    Search Google Scholar for articles from a specified journal matching the provided query.

    Args:
    - query (str): The search query string, usually including keywords and logical operators.
    - output_path (str): The path to save the results to.
    - journals (list[str]): If provided, for each journal in the list, the search will be performed for that journal only. If not provided, the search will be performed on the whole database (default: None).
    - save_output_to_df (bool, optional): Whether to save the search results to a DataFrame (default: True).
    - save_output_metadata (bool, optional): Whether to save the metadata of the search results (default: True).
    - save_results_to_pdf (bool, optional): Whether to download available PDFs (default: True).
    - use_proxy (bool, optional): Whether to use a proxy server (default: True).
    - date_format (str, optional): The date format to use for the output files.

    Returns:
    - pd.DataFrame: A DataFrame where each row represents a search result with the following columns:
        - 'Index': Index of the search result (int)
        - 'Formatted Author(s) and Year': Formatted string of authors and publication year (str)
        - 'Publication Year': Year of publication (int)
        - 'Citation Count': Number of citations (int)
        - 'Journal Name': Name of the journal (str)
        - 'Article Title': Title of the article (str)
        - 'Additional Data': Placeholder for additional data (str)
        - 'Full Citation': Full citation of the article
    """
    assert isinstance(query, str), "The search query must be a string."
    assert output_path, "The output path must be provided."
    assert isinstance(
        journals, (list, type(None))
    ), "The journals must be a list of strings or None."
    assert isinstance(
        save_output_to_df, bool
    ), "The save_output_to_df flag must be a boolean."
    assert isinstance(
        save_output_metadata, bool
    ), "The save_output_metadata flag must be a boolean."
    assert isinstance(
        save_results_to_pdf, bool
    ), "The save_results_to_pdf flag must be a boolean."
    assert isinstance(use_proxy, bool), "The use_proxy flag must be a boolean."

    logger.info("Running literature search")
    logger.info(f"Using the following search query: {query}")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    run_key = time.strftime(date_format)

    log_file_path = f"{output_path}/{PATHS.LOG_FILE_NAME}_{run_key}.log"

    if log_file_path:
        logger.debug("Setting up logging to a file")
        clean_log_file(
            log_file_path
        )  # Clear the literature search log file upon each script execution
        logger.add(log_file_path, rotation="10 MB", backtrace=True, diagnose=True)

    if use_proxy:
        setup_proxy()

    def do_search(journal_name: str, idx: int):
        """A helper function to perform the search for a given journal."""
        return search_google_scholar(
            journal_name=journal_name,
            query=query,
            idx=idx,
            save_results_to_pdf=save_results_to_pdf,
            output_path=output_path,
        )

    logger.info("Starting literature search")

    merged_results = pd.DataFrame()

    if journals:
        idx = 0
        for i, journal in enumerate(journals):
            logger.info(f"Processing journal {journal} ({i+1}/{len(journals)})")
            search_results: pd.DataFrame = do_search(journal_name=journal, idx=idx)
            merged_results = pd.concat(
                [merged_results, search_results], ignore_index=True
            )
            idx += search_results.shape[0]
    else:
        merged_results = do_search(journal_name=None, idx=0)  # Search all sources

    if save_output_to_df:
        output_df_path = f"{output_path}/{PATHS.SERACH_OUTPUT_FILE}_{run_key}.csv"
        save_output(out_df=merged_results, full_path=output_df_path)
    if save_output_metadata:
        output_metadata_path = f"{output_path}/{PATHS.METADATA_FILE}_{run_key}.txt"
        save_metadata(
            out_df=merged_results,
            full_path=output_metadata_path,
            journal_count=len(journals),
        )

    logger.success("Literature search completed")

    return merged_results
