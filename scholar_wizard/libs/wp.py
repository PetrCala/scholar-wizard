import time
from scholarly.publication_parser import _SearchScholarIterator
import requests
from loguru import logger
from scholar_wizard.static import STATIC


def check_doi_resolution(doi: str) -> bool:
    """
    Returns True if the DOI resolves to a recognized journal/publisher URL,
    False if it appears to be a preprint, unknown source, or can't be resolved.
    """
    # e.g., https://doi.org/api/handles/10.1016/j.cognition.2024.01.001?type=URL
    api_url = STATIC.DOI_API_URL.format(doi=doi)
    headers = {
        "Access-Control-Allow-Origin": "*",
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        time.sleep(0.1)

        if response.status_code == 200:
            data = response.json()

            if "values" not in data:
                return False

            # The "values" field typically contains the "data" or "url" for the redirect
            for val in data["values"]:
                if val.get("type") == "URL":
                    resolved_url = val["data"]["value"].lower()

                    if resolved_url:
                        # By default, if the DOI resolved, we assume it's published
                        return True

                    return False

                    # If it resolves to arxiv.org, ssrn.com, or researchgate,
                    # we treat it as a working paper or preprint:
                    # if any(
                    #     preprint_site in resolved_url
                    #     for preprint_site in [
                    #         "arxiv.org",
                    #         "ssrn.com",
                    #         "researchgate.net",
                    #     ]
                    # ):
                    #     return False

                    # # Naive check of the resolved URL to see if it's a recognized publisher
                    # if any(
                    #     pub_site in resolved_url
                    #     for pub_site in [
                    #         "springer",
                    #         "wiley",
                    #         "elsevier",
                    #         "tandfonline",
                    #         "nature.com",
                    #         "ieee",
                    #         "science.org",
                    #         "onlinelibrary",
                    #     ]
                    # ):
                    #     return True
                    # else:
                    #     # If none of the recognized publisher sites are in the URL,
                    #     # we default to "unknown" (False).
                    #     return False
        else:
            # If the API call fails, treat it as unknown
            return False

    except Exception:
        # If there's any error, treat it as unresolved or unknown
        return False

    return False


def is_likely_published(pub) -> bool:
    """
    Returns True if the publication is likely published based on
    metadata from scholarly (journal name, volume, issue, etc.)
    and whether the DOI resolves to a recognized publisher.
    """

    # 1) Check if there's a 'bib' field with typical "volume", "issue", "pages"
    bib = pub.get("bib", {})
    journal = bib.get(
        "journal", ""
    )  # e.g., "Cognition", "arXiv preprint", "SSRN", "..."
    volume = bib.get("volume", "")
    issue = bib.get("issue", "")
    pages = bib.get("pages", "")
    # Some DOIs may be in bib["doi"], or sometimes only in "pub_url" or nowhere at all.
    doi = bib.get("doi", "")

    # -- Heuristic checks --

    # A) If the journal name looks like a recognized preprint server, we do NOT mark as published
    if any(
        preprint in journal.lower() for preprint in ["arxiv", "ssrn", "researchgate"]
    ):
        return False

    # B) If there's a volume/issue/pages and a non-suspicious journal name,
    # that strongly indicates it's published
    if journal and volume and issue and pages:
        return True

    # C) If there's a DOI, try to see if it resolves to a recognized publisher
    if doi:
        if check_doi_resolution(doi):
            # If it resolves to a recognized publisher => published
            return True
        else:
            # If it resolves to something else or can’t be resolved => possibly not published
            return False

    # D) Sometimes you can check the snippet for phrases like "accepted for publication" or "in press"
    # If snippet has "in press" or "accepted for publication" => not fully published
    snippet = pub.get("snippet", "").lower()
    if "accepted for publication" in snippet or "in press" in snippet:
        return False

    # E) If none of the above gave a clear "published" signal, assume it's not published.
    return False


def subset_search_results_to_wps(
    search_results: _SearchScholarIterator, max_results: int = 10
) -> list:
    """
    Takes a list of search results from scholarly (or a similar API)
    and returns only those that appear to be a working paper / unpublished.
    """
    working_papers = []

    count = 0
    for pub in search_results:
        pub_title = pub.get("bib", {}).get("title", "unknown title")

        # Fetch the full "fill" to get more metadata (volume, issue, pages, doi,...)
        logger.debug(f"Filling publication: {pub_title}")
        pub_filled_dict = search_results.pub_parser.fill(pub)
        time.sleep(0.1)

        if not is_likely_published(pub_filled_dict):
            working_papers.append(pub_filled_dict)

        count += 1
        if count >= max_results:
            break

    return working_papers
