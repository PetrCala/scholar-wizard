import os
import time
import itertools
import pandas as pd
from loguru import logger
from scholarly import scholarly
from scholar_wizard.libs.utils import save_pdf_file


def get_study_publication(citation: str) -> dict | None:
    """Using a study citation, search for a publication. Return it as a dictionary."""

    logger.info(f"Searching for publication data for citation: {citation}")
    search_results = scholarly.search_pubs(citation)

    try:
        publication = next(search_results, None)

        if publication is None:
            logger.warning(f"Found no results when searching for citation: {citation}.")
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


def snowball_a_study(citation: str, max_results: int = 20) -> pd.DataFrame:
    """Using a study citation, get it's data, find relevant studies, and extract their data into a pandas data frame."""

    time.sleep(0.4)
    publication = scholarly.search_single_pub(pub_title=citation, filled=True)
    time.sleep(0.4)  # To avoid rate limiting
    related_studies = scholarly.get_related_articles(publication)

    results = []

    for index, result in itertools.islice(enumerate(related_studies), max_results):
        time.sleep(0.4)

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


def parse_snowballing_results(relevant_studies_df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse a raw snowballing DataFrame to extract relevant information.

    This function calculates the frequency of citations for each unique study,
    removes the 'Index' and 'Source Study' columns, and orders the result
    first by frequency (descending) and then by citation count (descending).
    """
    # Count the frequency of each unique study based on 'Formatted Author(s) and Year'
    frequency_counts = (
        relevant_studies_df.groupby("Formatted Author(s) and Year")["Source Study"]
        .count()
        .reset_index()
    )
    frequency_counts.rename(columns={"Source Study": "Frequency"}, inplace=True)

    # Merge the frequency counts with the original dataframe, dropping duplicates
    merged_df = relevant_studies_df.drop(
        columns=["Index", "Source Study"]
    ).drop_duplicates()
    result_df = merged_df.merge(frequency_counts, on="Formatted Author(s) and Year")

    # Sort first by Frequency (descending) then by Citation Count (descending)
    result_df = result_df.sort_values(
        by=["Frequency", "Citation Count"], ascending=[False, False]
    )

    # Reset index for clean output
    result_df.reset_index(drop=True, inplace=True)

    return result_df


def download_snowballing_pdfs(
    parsed_df: pd.DataFrame, output_dir: str, max_pdfs: int = 100
) -> None:
    """Using a snowballing output DataFrame, download all studies into an output folder."""

    assert isinstance(
        parsed_df, pd.DataFrame
    ), "The snowballing DataFrame must be a DataFrame."
    assert isinstance(output_dir, str), "The output directory must be a string."

    assert (
        "Frequency" in parsed_df.columns
    ), "The DataFrame must contain a 'Frequency' column."

    os.makedirs(output_dir, exist_ok=True)

    pdfs_to_download = parsed_df[parsed_df["Frequency"] > 1].head(max_pdfs)

    logger.info(
        f"Downloading {pdfs_to_download.shape[0]} snowballing PDFs to: {output_dir}"
    )

    for idx, row in pdfs_to_download.iterrows():
        pdf_url = row["PDF URL"]
        pdf_title = f"{idx}_{row["Formatted Author(s) and Year"]}"
        pdf_path = os.path.join(output_dir, f"{pdf_title}.pdf")

        try:
            save_pdf_file(pdf_url, pdf_path)
        except Exception as e:
            logger.error(f"Failed to download PDF from {pdf_url}: {e}")
