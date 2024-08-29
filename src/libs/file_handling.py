import time
import os
from loguru import logger
import pandas as pd
from src import PATHS, STATIC, config


def load_src_file() -> pd.DataFrame:
    """Load the source excel file with the studies and return it as a DataFrame."""
    logger.debug("Loading source file")
    assert os.path.exists(PATHS.SRC_FILE), f"File {PATHS.SRC_FILE} not found"

    try:
        df = pd.read_excel(PATHS.SRC_FILE, sheet_name=STATIC.JOURNALS_SHEET)
        assert (
            df.shape[0] == config.JOURNAL_COUNT
        ), f"Expected {config.JOURNAL_COUNT} journals, found {df.shape[0]}"
        return df
    except Exception as e:
        logger.error(f"Error loading source file: {e}")
        raise e


def save_output(
    out_df: pd.DataFrame, output_path_wo_suffix: str, file_suffix: str = None
) -> None:
    """
    Save the output data frame to a CSV file.

    Args:
    - out_df (pd.DataFrame): The data frame to save.
    - output_path_wo_suffix (str): The path to save the file to, without the suffix.
        Example: "output/search_results"
    - file_suffix (str): The suffix to add to the file name. If None, the current date and time will be used.
    """
    file_suffix = file_suffix or time.strftime("%Y%m%d-%H%M%S")
    full_path = f"{output_path_wo_suffix}_{file_suffix}.csv"
    logger.debug(f"Saving output file to {full_path}")
    if not os.path.exists(PATHS.OUTPUT_DIR):
        os.makedirs(PATHS.OUTPUT_DIR)
    out_df.to_csv(full_path, index=False)


def save_search_output(out_df: pd.DataFrame, file_suffix: str = None) -> None:
    """Save the search output to a CSV file."""
    save_output(out_df, PATHS.SEARCH_OUTPUT_FILE, file_suffix)
