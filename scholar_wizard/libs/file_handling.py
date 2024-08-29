import os
from loguru import logger
import pandas as pd
from scholar_wizard import PATHS, STATIC, config


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


def save_output(out_df: pd.DataFrame, full_path: str) -> None:
    """
    Save the output data frame to a CSV file.

    Args:
    - out_df (pd.DataFrame): The data frame to save.
    - full_path (str): The path to save the file to, including the .csv suffix.
    """
    assert full_path.endswith(".csv"), "Output file must be a CSV file"

    save_dir = os.path.dirname(full_path)

    logger.debug(f"Saving output file to {full_path}")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    out_df.to_csv(full_path, index=False)
