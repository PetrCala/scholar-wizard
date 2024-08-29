import os
from loguru import logger
import pandas as pd
from scholar_wizard import PATHS, STATIC


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
