import os
from enum import StrEnum


# Paths and static
SRC_DIR = os.path.abspath(os.path.dirname(__file__))
RUN_DIR = os.path.abspath(os.path.join(SRC_DIR, ".."))
OUTPUT_FOLDER = "output"
PDF_DOWNLOADS_FOLDER = "pdf_downloads"


class PATHS(StrEnum):
    """A collection of paths that are used throughout the project"""

    BASE_DIR = "literature_search"  # Where the script is located
    RUN_DIR = RUN_DIR
    OUTPUT_DIR = os.path.join(RUN_DIR, OUTPUT_FOLDER)
    PDF_DOWNLOADS_DIR = os.path.join(OUTPUT_DIR, PDF_DOWNLOADS_FOLDER)

    SRC_FILE = os.path.join(RUN_DIR, "LoS_incentives_revision_micro.xlsx")
    SEARCH_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "search")  # No suffix here
    SNOWBALLING_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "snowballing")  # No suffix here
    METADATA_FILE = os.path.join(OUTPUT_DIR, "metadata")  # No suffix here

    LIT_SEARCH_LOG_FILE = os.path.join(OUTPUT_DIR, "literature_search.log")

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
