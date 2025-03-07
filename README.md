# Scholar wizard

Welcome to **Scholar Wizard**! This guide will help you understand how to invoke the various functionalities of the Scholar Wizard package via the command-line interface (CLI). Whether you're performing literature searches or engaging in snowballing processes, this guide provides clear instructions and examples to get you started.

## Table of Contents

- [Scholar wizard](#scholar-wizard)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Scholar Wizard](#running-scholar-wizard)
    - [General Command Structure](#general-command-structure)
    - [Available Commands](#available-commands)
      - [1. Search](#1-search)
      - [2. Snowball](#2-snowball)
  - [Help and Documentation](#help-and-documentation)
    - [General Help](#general-help)
    - [Command-Specific Help](#command-specific-help)
  - [Examples](#examples)
    - [Example 1: Performing a Literature Search](#example-1-performing-a-literature-search)

## Prerequisites

Before using Scholar Wizard, ensure you have the following:

- **Python 3.7 or higher** installed on your system.
- **pip** (Python package installer) available.
- Necessary dependencies installed (see [Installation](#installation)).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/scholar_wizard.git
   cd scholar_wizard
   ```

2. **Install Dependencies**

   It's recommended to use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

   Install the pacakge:

   ```bash
   pip install -e .
   ```

## Running Scholar Wizard

Scholar Wizard provides a flexible CLI that allows you to invoke different functionalities seamlessly. The general command structure is as follows:

```bash
python -m scholar_wizard <command> [options]
```

### General Command Structure

- **`python -m scholar_wizard`**: Invokes the Scholar Wizard package.
- **`<command>`**: Specifies the functionality you want to execute (e.g., `search`, `snowball`).
- **`[options]`**: Additional arguments and flags tailored to the chosen command.

### Available Commands

Currently, Scholar Wizard supports the following commands:

#### 1. Search

**Description:**  
Search Google Scholar for articles based on a query and various optional parameters.

**Usage:**

```bash
python -m scholar_wizard search [options]
```

**Options:**

- `--query` (str, **required**): The search query string, including keywords and logical operators.
- `--output-path` (str, **required**): The directory path where results will be saved.
- `--journals` (str, optional): List of journals to limit the search to. Provide multiple journals separated by spaces.
- `--year-from` (int, optional): The starting year to search from.
- `--year-to` (int, optional): The ending year to search to.
- `--save-output-to-df` / `--no-save-output-to-df` (bool, optional): Flag to save the search results to a DataFrame. Defaults to `True`.
- `--save-output-metadata` / `--no-save-output-metadata` (bool, optional): Flag to save the metadata of the search results. Defaults to `True`.
- `--save-results-to-pdf` / `--no-save-results-to-pdf` (bool, optional): Flag to download available PDFs. Defaults to `True`.
- `--no-proxy` (bool, optional): Flag to disable using a proxy server. If not provided, a proxy server will be used by default.
- `--working-papers-only` (bool, optional): If set to True, the search will be subsetted to only working papers.
- `--max-pdf-downloads` (int, optional): Maximum number of PDF files to download per journal/search. Defaults to `50`.
- `--date-format` (str, optional): The date format to use for the output files. Defaults to `YYYY-MM-DD`.

#### 2. Snowball

**Description:**  
Perform a snowballing process to find related articles based on existing references.

**Details:**
For each passed input reference, the package searches for related Google Scholar articles. It saves metadata about each of the related articles, and finally groups these metadata to identify the most relevant articles.

**Usage:**

```bash
python -m scholar_wizard snowball [options]
```

**Options:**

- `--output-path` (str, **required**): The directory path where snowballing results will be saved.
- `--journals` (str, optional): List of journals to limit the snowballing process. Provide multiple journals separated by spaces.
- `--no-proxy` (bool, optional): Flag to disable using a proxy server. If not provided, a proxy server will be used by default.
- `--date-format` (str, optional): The date format to use for the output files. Defaults to `YYYY-MM-DD`.

## Help and Documentation

For detailed information about each command and its options, you can use the `--help` flag with any command.

### General Help

```bash
python -m scholar_wizard --help
```

### Command-Specific Help

Replace `<command>` with the desired command (e.g., `search`, `snowball`).

```bash
python -m scholar_wizard <command> --help
```

**Examples:**

- **Search Help:**

  ```bash
  python -m scholar_wizard search --help
  ```

- **Snowball Help:**

  ```bash
  python -m scholar_wizard snowball --help
  ```

## Examples

### Example 1: Performing a Literature Search

**Scenario:**  
You want to search for articles related to "machine learning" in the "Journal of AI" and "Journal of ML". Save the results to the `./results` directory, download PDFs, and disable the use of a proxy server.

**Command:**

```bash
python -m scholar_wizard search \
  --query "machine learning" \
  --output_path "./results" \
  --journals "Journal of AI" "Journal of ML" \
  --max_pdf_downloads 100 \
  --no-use_proxy
```

**Explanation:**

- **`--query "machine learning"`**: Searches for articles containing "machine learning".
- **`--output_path "./results"`**: Saves the search results in the `./results` directory.
- **`--journals "Journal of AI" "Journal of ML"`**: Limits the search to these two journals.
- **`--max_pdf_downloads 100`**: Sets the maximum number of PDF downloads per journal/search to 100.
- **`--no-proxy`**: Disables the use of a proxy server.

---

By following this guide, you should be able to effectively utilize the Scholar Wizard CLI to perform literature searches and snowballing processes. For further assistance, refer to the project's [GitHub repository](https://github.com/yourusername/scholar_wizard) or contact the maintainer.
