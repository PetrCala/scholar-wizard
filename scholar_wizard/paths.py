import os
from enum import StrEnum

MODULE_PATH = f"{os.path.dirname(__file__)}"
PROJECT_ROOT = os.path.dirname(MODULE_PATH)


class PATHS(StrEnum):
    """A collection of paths that are used throughout the project"""

    MODULE_PATH = MODULE_PATH
    PROJECT_ROOT = PROJECT_ROOT

    PDF_DOWNLOADS_FOLDER = "pdf_downloads"
    SEARCH_OUTPUT_FILE = "search"
    SNOWBALL_OUTPUT_FILE = "snowball"
    SNOWBALL_UNPARSED_OUTPUT_FILE = "snowball_unparsed"
    METADATA_FILE = "metadata"
    LOG_FILE_NAME = "literature_search"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
