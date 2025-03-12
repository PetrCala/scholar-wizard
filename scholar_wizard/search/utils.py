import os
from loguru import logger
import pandas as pd
from scholarly import scholarly
from scholar_wizard import PATHS, STATIC
from scholar_wizard.libs.utils import save_pdf_file
from scholar_wizard.libs.wp import subset_search_results_to_wps


# pylint: disable=too-many-locals
def search_google_scholar(
    query: str,
    journal_name: str = None,
    idx: int = 0,
    year_from: int = None,
    year_to: int = None,
    save_results_to_pdf: bool = False,
    output_path: str = None,
    max_count: int = None,
    max_pdf_downloads: int = STATIC.MAX_PDF_DOWNLOADS_DEFAULT,
    working_papers_only: bool = False,
) -> pd.DataFrame:
    """
    Searches Google Scholar for articles from a specified journal matching the provided query.

    Args:
    - query (str): The search query string, usually including keywords and logical operators.
    - journal_name (str, optional): The name of the journal to search within. If not provided, search all sources.
    - idx (int, optional): The index of the first search result to return.
    - year_from (int, optional): The starting year for the search (default: None).
    - year_to (int, optional): The ending year for the search (default: None).
    - save_results_to_pdf (bool, optional): Whether to download available PDFs (default: False).
    - output_path (str, optional): Directory where PDFs should be saved (default: None).
    - max_count (int, optional): The maximum number of search results to return (default: None).
    - max_pdf_downloads (int, optional): The maximum number of PDF files to download per journal/search (default: 50).
    - working_papers_only (bool, optional): Whether to only search for working papers (default: False).


    Returns:
        pd.DataFrame: A DataFrame where each row represents a search result with the following columns:
              - 'Index': Index of the search result (int)
              - 'Formatted Author(s) and Year': Formatted string of authors and publication year (str)
              - 'Publication Year': Year of publication (int)
              - 'Citation Count': Number of citations (int)
              - 'Journal Name': Name of the journal (str)
              - 'Article Title': Title of the article (str)
              - 'Additional Data': Placeholder for additional data (str)
              - 'Full Citation': Full citation of the article (str)
    """
    assert isinstance(idx, int) and (idx >= 0), "The index must be a positive integer."

    # Combine the journal name and query if provided
    if journal_name:
        query = f'source:" {journal_name}" {query}'

    # Search Google Scholar
    logger.debug(f"Searching Google Scholar for: {query}")
    search_results = scholarly.search_pubs(query, year_low=year_from, year_high=year_to)
    logger.info(f"Found {search_results.total_results} results")

    if working_papers_only:
        logger.debug("Subsetting the results to working papers only.")
        search_results = subset_search_results_to_wps(
            search_results=search_results, max_results=500
        )
        logger.info(f"Found {len(search_results)} working papers")

    results = []
    pdf_count = 0
    total_count = 0

    if save_results_to_pdf:
        assert isinstance(
            output_path, str
        ), "The output path must be provided if you wish to save PDF files."
        # Create the output directory if it does not exist
        output_dir = os.path.join(output_path, PATHS.PDF_DOWNLOADS_FOLDER)
        if journal_name:
            output_dir = os.path.join(output_dir, journal_name.replace(" ", "_"))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    for index, result in enumerate(search_results):
        # Extract the necessary details
        title = result["bib"]["title"]
        authors = result["bib"]["author"]
        year = result["bib"]["pub_year"]
        journal = result["bib"]["venue"]
        citation = result["num_citations"]
        source = result["bib"]["venue"]

        # Use the input journal name by default
        journal_name = journal_name or journal or ""

        logger.info(f"Processing result: {title}")

        # cite = result["bib"]["url_scholarbib"]
        # scholar_citation = requests.get(
        #     "https://scholar.google.com" + cite, timeout=10
        # ).text
        # fetch_publication_citation()

        # Format authors for the table format
        author_list = authors.split(", ") if isinstance(authors, str) else authors
        main_author = author_list[0]
        # additional_authors = ", ".join(author_list[1:]) if len(author_list) > 1 else ""
        formatted_authors = (
            f"{main_author} et al." if len(author_list) > 1 else main_author
        )

        # Create a full citation
        citation_full = f"{', '.join(author_list)} ({year}). {title}. {source}."

        # Check for a PDF link
        pdf_link = result.get("eprint_url", None)
        pdf_filename = f"{output_dir}/{index+1+idx}_{year}_{main_author}.pdf".replace(
            " ", "_"
        )

        # Attempt to download the PDF if the option is enabled and the PDF link exists
        if (
            save_results_to_pdf
            and pdf_link
            and pdf_count < max_pdf_downloads
            and not os.path.exists(pdf_filename)
        ):
            try:
                save_pdf_file(pdf_url=pdf_link, save_path=pdf_filename)
                pdf_count += 1
            except Exception as e:
                logger.error(f"Failed to download PDF from {pdf_link}: {e}")

        # Prepare the formatted row
        row = [
            index + 1 + idx,
            f"{formatted_authors} ({year})",
            year,
            citation,
            journal_name,
            title,
            "",
            citation_full,
        ]
        assert len(row) == len(STATIC.STUDY_DF_COLUMNS), "The row length is incorrect."

        # Append to results
        results.append(row)

        total_count += 1
        if total_count >= max_count:
            break

    # Convert the list of results into a DataFrame
    df = pd.DataFrame(results, columns=STATIC.STUDY_DF_COLUMNS)

    return df
