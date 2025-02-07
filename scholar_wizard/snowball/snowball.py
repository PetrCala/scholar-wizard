import os
import time
from loguru import logger
import pandas as pd
from scholar_wizard import STATIC, PATHS
from scholar_wizard.libs.file_handling import save_output
from scholar_wizard.libs.scholar_utils import setup_proxy
from scholar_wizard.libs.logs import clean_log_file
from .utils import snowball_a_study


def snowball(
    output_path: str,
    journals: list[str] = None,
    use_proxy: bool = True,
    date_format: str = STATIC.DATE_FORMAT,
):
    assert isinstance(output_path, str), "The output path must be a string."
    assert isinstance(
        journals, (list, type(None))
    ), "The journals must be a list of strings or None."
    assert isinstance(use_proxy, bool), "The use_proxy flag must be a boolean."
    assert isinstance(date_format, str), "The date_format must be a string."

    logger.info("Running snowballing...")

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

    merged_results = pd.DataFrame()

    src_citations = [
        "Gneezy, U., Rau, H., Samek, A., & Zhurakhovska, L. (2017). Do I care if you are paid? A field experiment on charitable donations (No. 307). cege Discussion Papers."
    ]

    for i, citation in enumerate(src_citations):
        logger.info(f"Processing study {i + 1}/{len(src_citations)}: {citation}")
        df = snowball_a_study(citation)
        if not df.empty:
            merged_results = pd.concat([merged_results, df], ignore_index=True)

    # if save_output_to_df:
    output_df_path = f"{output_path}/{PATHS.SNOWBALL_OUTPUT_FILE}_{run_key}.csv"
    save_output(out_df=merged_results, full_path=output_df_path)

    logger.success("Snowballing completed")

    return merged_results


def add_arguments(parser):
    """
    Adds command-line arguments for the snowball functionality.

    Args:
    - parser (argparse.ArgumentParser): The parser to add arguments to.
    """
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="The path to save the snowballing results.",
    )
    parser.add_argument(
        "--journals",
        type=str,
        nargs="*",
        default=None,
        help="List of journals to limit the snowballing process. If omitted, all journals are considered.",
    )
    parser.add_argument(
        "--no-proxy",
        action="store_false",
        dest="use_proxy",
        default=True,
        help="Flag to use a proxy server (default: True).",
    )
    parser.add_argument(
        "--date-format",
        type=str,
        default=STATIC.DATE_FORMAT,
        help=f"The date format to use for the output files (default: {STATIC.DATE_FORMAT}).",
    )


def run(args):
    """
    Executes the snowball functionality using parsed command-line arguments.

    Args:
    - args (argparse.Namespace): Parsed command-line arguments.
    """
    # Convert journals to list if it's not None
    journals = args.journals if args.journals else None

    # Call the snowball function with the parsed arguments
    snowball(
        output_path=args.output_path,
        journals=journals,
        use_proxy=args.use_proxy,
        date_format=args.date_format,
    )
