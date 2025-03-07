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
    year_from: int = None,
    year_to: int = None,
    save_output_to_df: bool = True,
    save_output_metadata: bool = True,
    save_results_to_pdf: bool = True,
    use_proxy: bool = True,
    working_papers_only: bool = False,
    max_pdf_downloads: int = STATIC.MAX_PDF_DOWNLOADS_DEFAULT,
    date_format: str = STATIC.DATE_FORMAT,
) -> pd.DataFrame:
    """
    Search Google Scholar for articles from a specified journal matching the provided query.

    Args:
    - query (str): The search query string, usually including keywords and logical operators.
    - output_path (str): The path to save the results to.
    - journals (list[str]): If provided, for each journal in the list, the search will be performed for that journal only. If not provided, the search will be performed on the whole database (default: None).
    - year_from (int, optional): The starting year to search from.
    - year_to (int, optional): The ending year to search to.
    - save_output_to_df (bool, optional): Whether to save the search results to a DataFrame (default: True).
    - save_output_metadata (bool, optional): Whether to save the metadata of the search results (default: True).
    - save_results_to_pdf (bool, optional): Whether to download available PDFs (default: True).
    - use_proxy (bool, optional): Whether to use a proxy server (default: True).
    - working_papers_only (bool, optional): Whether to search only working papers (default: False).
    - max_pdf_downloads (int, optional): The maximum number of PDF files to download per journal/search (default: 50).
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
        year_from, (int, type(None))
    ), "The year_from must be an integer or None."
    assert isinstance(
        year_to, (int, type(None))
    ), "The year_to must be an integer or None."
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
    assert isinstance(
        working_papers_only, bool
    ), "The working_papers_only flag must be a boolean."
    assert isinstance(
        max_pdf_downloads, int
    ), "The max_pdf_downloads must be an integer."
    assert isinstance(date_format, str), "The date_format must be a string."

    if working_papers_only:
        logger.info("Modifying the search query to include only working papers")
        query = f"{STATIC.WP_QUERY_PREFIX} {query}"

    logger.info("Running literature search")
    logger.info(f"Using the following search query: '{query}'")

    os.makedirs(output_path, exist_ok=True)

    run_key = time.strftime(date_format)

    if log_file_path := f"{output_path}/{PATHS.LOG_FILE_NAME}_{run_key}.log":
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
            year_from=year_from,
            year_to=year_to,
            save_results_to_pdf=save_results_to_pdf,
            output_path=output_path,
            max_pdf_downloads=max_pdf_downloads,
            working_papers_only=working_papers_only,
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

        if save_output_metadata:
            output_metadata_path = f"{output_path}/{PATHS.METADATA_FILE}_{run_key}.txt"
            save_metadata(
                out_df=merged_results,
                full_path=output_metadata_path,
                journal_count=len(journals) if journals else 0,
            )
    else:
        merged_results = do_search(journal_name=None, idx=0)  # Search all sources

    if save_output_to_df:
        output_df_path = f"{output_path}/{PATHS.SEARCH_OUTPUT_FILE}_{run_key}.csv"
        save_output(out_df=merged_results, full_path=output_df_path)

    logger.success("Literature search completed")

    return merged_results


def add_arguments(parser):
    """
    Adds command-line arguments for the search functionality.

    Args:
    - parser (argparse.ArgumentParser): The parser to add arguments to.
    """
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="The search query string, including keywords and logical operators.",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="The path to save the search results.",
    )
    parser.add_argument(
        "--journals",
        type=str,
        nargs="*",
        default=None,
        help="List of journals to limit the search to. If omitted, search the entire database.",
    )
    parser.add_argument(
        "--year-from",
        type=int,
        dest="year_from",
        default=None,
        help="The starting year to search from.",
    )
    parser.add_argument(
        "--year-to",
        type=int,
        dest="year_to",
        default=None,
        help="The ending year to search to.",
    )
    parser.add_argument(
        "--save-output-to-df",
        action="store_true",
        default=True,
        help="Flag to save the search results to a DataFrame (default: True).",
    )
    parser.add_argument(
        "--no-save-output-to-df",
        action="store_false",
        dest="save_output_to_df",
        help="Do not save the search results to a DataFrame.",
    )
    parser.add_argument(
        "--save-output-metadata",
        action="store_true",
        default=True,
        help="Flag to save the metadata of the search results (default: True).",
    )
    parser.add_argument(
        "--no-save-output-metadata",
        action="store_false",
        dest="save_output_metadata",
        help="Do not save the metadata of the search results.",
    )
    parser.add_argument(
        "--save-results-to-pdf",
        action="store_true",
        default=True,
        help="Flag to download available PDFs (default: True).",
    )
    parser.add_argument(
        "--no-save-results-to-pdf",
        action="store_false",
        dest="save_results_to_pdf",
        help="Do not download available PDFs.",
    )
    parser.add_argument(
        "--no-proxy",
        action="store_false",
        dest="use_proxy",
        default=True,
        help="Flag to use a proxy server (default: True).",
    )
    parser.add_argument(
        "--working-papers-only",
        action="store_true",
        default=False,
        help="Flag to search only working papers (default: False).",
    )
    parser.add_argument(
        "--max-pdf-downloads",
        type=int,
        default=STATIC.MAX_PDF_DOWNLOADS_DEFAULT,
        help=f"The maximum number of PDF files to download per journal/search (default: {STATIC.MAX_PDF_DOWNLOADS_DEFAULT}).",
    )
    parser.add_argument(
        "--date-format",
        type=str,
        default=STATIC.DATE_FORMAT,
        help=f"The date format to use for the output files (default: {STATIC.DATE_FORMAT}).",
    )


def run(args):
    """
    Executes the search functionality using parsed command-line arguments.

    Args:
    - args (argparse.Namespace): Parsed command-line arguments.
    """
    # Convert journals to list if it's not None
    journals = args.journals if args.journals else None

    # Call the search function with the parsed arguments
    search(
        query=args.query,
        output_path=args.output_path,
        journals=journals,
        year_from=args.year_from,
        year_to=args.year_to,
        save_output_to_df=args.save_output_to_df,
        save_output_metadata=args.save_output_metadata,
        save_results_to_pdf=args.save_results_to_pdf,
        use_proxy=args.use_proxy,
        working_papers_only=args.working_papers_only,
        max_pdf_downloads=args.max_pdf_downloads,
        date_format=args.date_format,
    )
