import os
from loguru import logger


def clean_log_file(log_file_path: str) -> None:
    """
    Clear the log file upon each script execution

    Args:
    - log_file_path (str): The path to the log file
    """
    if not os.path.exists(log_file_path):
        logger.warning(f"Log file {log_file_path} not found")
        return
    with open(log_file_path, "w"):
        pass
