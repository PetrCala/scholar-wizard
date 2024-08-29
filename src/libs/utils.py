import time
from loguru import logger
import pandas as pd
from src import PATHS, config


def save_metadata(out_df: pd.DataFrame, file_suffix: str = None) -> None:
    """Save the metadata to a TXT file."""
    logger.debug("Saving metadata")
    file_suffix = file_suffix or time.strftime("%Y%m%d-%H%M%S")
    unique_journals = out_df["Journal Name"].nunique()
    full_path = f"{PATHS.METADATA_FILE}_{file_suffix}.txt"
    with open(full_path, "w") as f:
        f.write(f"Journals searched: {config.JOURNAL_COUNT}\n")
        f.write(f"Total number of studies: {out_df.shape[0]}\n")
        f.write(f"Number of journals with results: {unique_journals}\n")
        f.write(
            f"Number of journals with no results: {config.JOURNAL_COUNT - unique_journals}\n"
        )
