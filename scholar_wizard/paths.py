from enum import StrEnum


class PATHS(StrEnum):
    """A collection of paths that are used throughout the project"""

    PDF_DOWNLOADS_FOLDER = "pdf_downloads"
    SERACH_OUTPUT_FILE = "search"
    METADATA_FILE = "metadata"
    LOG_FILE_NAME = "literature_search"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
