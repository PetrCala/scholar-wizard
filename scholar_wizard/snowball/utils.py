import pandas as pd
from loguru import logger
from scholarly import scholarly


def get_study_publication(citation: str) -> dict | None:
    """Using a study citation, search for a publication. Return it as a dictionary."""

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

        return publication

    except Exception as e:
        logger.warning(
            f"Failed to retrieve publication data for citation: {citation}: {e}"
        )
        return None


def snowball_a_study(citation: str) -> pd.DataFrame:
    """Using a study citation, get it's data, find relevant studies, and extract their data into a pandas data frame."""

    publication = get_study_publication(citation)
    # OR
    # publication = scholarly.search_single_pub(pub_title=citation, filled=True)

    if not publication:
        return pd.DataFrame({})

    url_related_articles = publication["bib"]["url_related_articles"]
    related_studies = scholarly.search_pubs_custom_url(url=url_related_articles)

    results = []

    for index, result in enumerate(related_studies):

        title = result["bib"]["title"]
        authors = result["bib"]["author"]
        year = result["bib"]["pub_year"]
        journal = result["bib"]["venue"]
        num_citations = result["num_citations"]
        source = result["bib"]["venue"]
        pdf_link = result.get("eprint_url", None)

        logger.info(f"Processing relevant study: {title}")

        # Format authors for the table format
        author_list = authors.split(", ") if isinstance(authors, str) else authors
        main_author = author_list[0]
        # additional_authors = ", ".join(author_list[1:]) if len(author_list) > 1 else ""
        formatted_authors = (
            f"{main_author} et al." if len(author_list) > 1 else main_author
        )

        # Create a full citation
        citation_full = f"{', '.join(author_list)} ({year}). {title}. {source}."

        row = [
            index + 1,
            citation,  # Of the source study
            f"{formatted_authors} ({year})",
            year,
            num_citations,
            title,
            "",
            citation_full,
            pdf_link,
        ]

        results.append(row)

    columns = [
        "Index",
        "Source Study",
        "Formatted Author(s) and Year",
        "Publication Year",
        "Citation Count",
        "Article Title",
        "Additional Data",
        "Full Citation",
        "PDF Link",
    ]

    # Convert the list of results into a DataFrame
    df = pd.DataFrame(results, columns=columns)

    return df
