import os
from loguru import logger
import pandas as pd
from scholar_wizard import config


def save_metadata(out_df: pd.DataFrame, full_path: str) -> None:
    """
    Save the metadata to a TXT file.

    Args:
    - out_df (pd.DataFrame): The data frame with the search results.
    - full_path (str): The full path to save the metadata to, including the .txt suffix.
    """
    assert full_path.endswith(".txt"), "Metadata file must be a TXT file"

    logger.debug("Saving metadata")

    save_dir = os.path.dirname(full_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    unique_journals = out_df["Journal Name"].nunique()

    with open(full_path, "w") as f:
        f.write(f"Journals searched: {config.JOURNAL_COUNT}\n")
        f.write(f"Total number of studies: {out_df.shape[0]}\n")
        f.write(f"Number of journals with results: {unique_journals}\n")
        f.write(
            f"Number of journals with no results: {config.JOURNAL_COUNT - unique_journals}\n"
        )
