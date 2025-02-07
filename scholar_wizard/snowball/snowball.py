import os
import time
from loguru import logger
import pandas as pd
from scholar_wizard import STATIC, PATHS
from scholar_wizard.libs.file_handling import save_output
from scholar_wizard.libs.scholar_utils import setup_proxy
from scholar_wizard.libs.logs import clean_log_file
from .utils import (
    snowball_a_study,
    parse_snowballing_results,
    download_snowballing_pdfs,
)


def snowball(
    output_dir: str,
    use_proxy: bool = True,
    date_format: str = STATIC.DATE_FORMAT,
    save_unparsed_output: bool = True,
    download_pdfs: bool = True,
):
    assert isinstance(output_dir, str), "The output directory must be a string."
    assert isinstance(use_proxy, bool), "The use_proxy flag must be a boolean."
    assert isinstance(date_format, str), "The date_format must be a string."

    logger.info("Running snowballing...")

    os.makedirs(output_dir, exist_ok=True)

    run_key = time.strftime(date_format)

    if log_file_path := f"{output_dir}/{PATHS.LOG_FILE_NAME}_{run_key}.log":
        logger.debug("Setting up logging to a file")
        clean_log_file(
            log_file_path
        )  # Clear the literature search log file upon each script execution
        logger.add(log_file_path, rotation="10 MB", backtrace=True, diagnose=True)

    if use_proxy:
        setup_proxy()

    relevant_studies_df = pd.DataFrame()

    src_citations = [
        "Gneezy, U., Rau, H., Samek, A., & Zhurakhovska, L. (2017). Do I care if you are paid? A field experiment on charitable donations (No. 307). cege Discussion Papers."
    ]

    for i, citation in enumerate(src_citations):
        logger.info(f"Processing study {i + 1}/{len(src_citations)}: {citation}")
        df = snowball_a_study(citation)
        if not df.empty:
            relevant_studies_df = pd.concat(
                [relevant_studies_df, df], ignore_index=True
            )

    if save_unparsed_output:
        unparsed_output_path = (
            f"{output_dir}/{PATHS.SNOWBALL_UNPARSED_OUTPUT_FILE}_{run_key}.csv"
        )
        save_output(out_df=relevant_studies_df, full_path=unparsed_output_path)

    snowballing_df = parse_snowballing_results(relevant_studies_df=relevant_studies_df)

    output_df_path = f"{output_dir}/{PATHS.SNOWBALL_OUTPUT_FILE}_{run_key}.csv"
    save_output(out_df=snowballing_df, full_path=output_df_path)

    if download_pdfs:
        download_snowballing_pdfs(
            parsed_df=snowballing_df,
            output_dir=f"{output_dir}/{PATHS.PDF_DOWNLOADS_FOLDER}_{run_key}",
        )
    else:
        logger.info("Skipping PDF downloads")

    logger.success("Snowballing completed")

    return snowballing_df


def add_arguments(parser):
    """
    Adds command-line arguments for the snowball functionality.

    Args:
    - parser (argparse.ArgumentParser): The parser to add arguments to.
    """
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="The path to the directory where to save the snowballing results.",
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
    parser.add_argument(
        "--save-unparsed-output",
        action="store_true",
        default=True,
        help="Flag to save the unparsed snowballing results (default: True).",
    )
    parser.add_argument(
        "--download-pdfs",
        action="store_true",
        default=True,
        help="Flag to download PDFs for the snowballing results (default: True).",
    )


def run(args):
    """
    Executes the snowball functionality using parsed command-line arguments.

    Args:
    - args (argparse.Namespace): Parsed command-line arguments.
    """
    # Call the snowball function with the parsed arguments
    snowball(
        output_path=args.output_path,
        use_proxy=args.use_proxy,
        date_format=args.date_format,
    )
