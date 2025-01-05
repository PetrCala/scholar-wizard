from typing import TypedDict


class STATIC(TypedDict):
    """A collection of static variables that are used throughout the project"""

    DATE_FORMAT = "%Y%m%d"
    MAX_PDF_DOWNLOADS_DEFAULT = 50
    STUDY_DF_COLUMNS = [
        "Index",
        "Formatted Author(s) and Year",
        "Publication Year",
        "Citation Count",
        "Journal Name",
        "Article Title",
        "Additional Data",
        "Full Citation",
    ]
