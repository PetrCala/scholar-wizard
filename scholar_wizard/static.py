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
    DOI_API_URL = "https://doi.org/api/handles/{doi}?type=URL"
    VALID_DOI = "10.47366/sabia.v5n1a3"

    # A prefix that subsets a search query to only include working papers (partially)
    WP_QUERY_PREFIX = '("working paper" OR "discussion paper") AND'
