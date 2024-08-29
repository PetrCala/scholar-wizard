import os
import time
import requests
from loguru import logger
import pandas as pd
from scholarly import scholarly
from search import PATHS


def search_google_scholar(
    journal_name: str,
    query: str,
    idx: int = 0,
    save_results_to_pdf: bool = False,
    output_dir: str = PATHS.PDF_DOWNLOADS_DIR,
) -> pd.DataFrame:
    """
    Searches Google Scholar for articles from a specified journal matching the provided query.

    Args:
        journal_name (str): The name of the journal to search within.
        query (str): The search query string, usually including keywords and logical operators.
        idx (int, optional): The index of the first search result to return.
        save_results_to_pdf (bool, optional): Whether to download available PDFs (default: False).
        output_dir (str, optional): Directory where PDFs should be saved (default: 'pdf_downloads').


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

    # Combine the journal name and query
    search_query = f'source:" {journal_name}" {query}'

    # Search Google Scholar
    search_results = scholarly.search_pubs(search_query)
    logger.info(f"Found {search_results.total_results} results")

    results = []
    pdf_count = 0

    # Create the output directory if it does not exist
    journal_output_dir = os.path.join(output_dir, journal_name.replace(" ", "_"))
    if save_results_to_pdf and not os.path.exists(journal_output_dir):
        os.makedirs(journal_output_dir)

    for index, result in enumerate(search_results):
        # related_articles = scholarly.get_related_articles(result)
        # for related in related_articles:
        #     pass
        # Extract the necessary details
        title = result["bib"]["title"]
        authors = result["bib"]["author"]
        year = result["bib"]["pub_year"]
        citation = result["num_citations"]
        source = result["bib"]["venue"]

        # Format authors for the table format
        author_list = authors.split(", ") if isinstance(authors, str) else authors
        main_author = author_list[0]
        additional_authors = ", ".join(author_list[1:]) if len(author_list) > 1 else ""
        formatted_authors = (
            f"{main_author} et al." if len(author_list) > 1 else main_author
        )

        # Create a full citation
        citation_full = f"{', '.join(author_list)} ({year}). {title}. {source}."

        # Check for a PDF link
        pdf_link = result.get("eprint_url", None)
        pdf_filename = (
            f"{journal_output_dir}/{index+1+idx}_{year}_{main_author}.pdf".replace(
                " ", "_"
            )
        )

        # Attempt to download the PDF if the option is enabled and the PDF link exists
        if (
            save_results_to_pdf
            and pdf_link
            and pdf_count < 50
            and not os.path.exists(pdf_filename)
        ):
            logger.debug(f"Downloading PDF for {title}")
            try:
                response = requests.get(pdf_link)
                if response.status_code == 200:
                    with open(pdf_filename, "wb") as pdf_file:
                        pdf_file.write(response.content)
                    pdf_count += 1
                else:
                    pdf_link = None  # Invalidate the link if the download failed
                time.sleep(0.2)
            except Exception as e:
                print(f"Failed to download PDF for {title}: {e}")
                pdf_link = None

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

        # Append to results
        results.append(row)

    # Convert the list of results into a DataFrame
    df = pd.DataFrame(
        results,
        columns=[
            "Index",
            "Formatted Author(s) and Year",
            "Publication Year",
            "Citation Count",
            "Journal Name",
            "Article Title",
            "Additional Data",
            "Full Citation",
        ],
    )

    return df
