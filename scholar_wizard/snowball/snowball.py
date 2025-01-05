from scholar_wizard import STATIC


def snowball(
    output_path: str,
    journals: list[str] = None,
    use_proxy: bool = True,
    date_format: str = STATIC.DATE_FORMAT,
):
    assert isinstance(output_path, str), "The output path must be a string."
    assert isinstance(
        journals, (list, type(None))
    ), "The journals must be a list of strings or None."
    assert isinstance(use_proxy, bool), "The use_proxy flag must be a boolean."
    assert isinstance(date_format, str), "The date_format must be a string."

    print("Snowballing not implemented yet")


def add_arguments(parser):
    """
    Adds command-line arguments for the snowball functionality.

    Args:
    - parser (argparse.ArgumentParser): The parser to add arguments to.
    """
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="The path to save the snowballing results.",
    )
    parser.add_argument(
        "--journals",
        type=str,
        nargs="*",
        default=None,
        help="List of journals to limit the snowballing process. If omitted, all journals are considered.",
    )
    parser.add_argument(
        "--no-proxy",
        action="store_false",
        dest="use_proxy",
        default=True,
        help="Flag to use a proxy server (default: True).",
    )
    parser.add_argument(
        "--date-format",
        type=str,
        default=STATIC.DATE_FORMAT,
        help=f"The date format to use for the output files (default: {STATIC.DATE_FORMAT}).",
    )


def run(args):
    """
    Executes the snowball functionality using parsed command-line arguments.

    Args:
    - args (argparse.Namespace): Parsed command-line arguments.
    """
    # Convert journals to list if it's not None
    journals = args.journals if args.journals else None

    # Call the snowball function with the parsed arguments
    snowball(
        output_path=args.output_path,
        journals=journals,
        use_proxy=args.use_proxy,
        date_format=args.date_format,
    )
