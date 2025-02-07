import pandas as pd
from loguru import logger
import requests
from scholarly import Publication, scholarly
from scholar_wizard.libs.scholar_utils import setup_proxy
from scholar_wizard import STATIC


def get_study_publication(citation: str) -> Publication | None:
    """Using a study citation, search for a publication"""

    setup_proxy()
    logger.info(f"Searching for publication data for citation: {citation}")
    search_results = scholarly.search_pubs(citation)

    try:
        publication = next(search_results, None)

        if publication is None:
            logger.warning("Iterator is empty.")
            return None

        try:
            _ = next(publication)  # Check if there are more elements
            logger.warning(
                f"Found more results when trying to retrieve publication data for citation: {citation}"
            )
            return None
        except StopIteration:
            pass

        citation_url = publication["bib"]["url_scholarbib"]

        logger.debug(f"Fetching citation data...")
        citation = requests.get(
            "https://scholar.google.com" + citation_url, timeout=10
        ).text

        # TODO: Parse the citation data

        return citation

    except Exception as e:
        logger.warning(
            f"Failed to retrieve publication data for citation: {citation}: {e}"
        )
        return None


def get_study_snowball_results(citation: str) -> pd.DataFrame:
    """Using a study citation, search for a"""
    return pd.DataFrame(columns=STATIC.STUDY_DF_COLUMNS)
