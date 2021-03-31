import argparse
import pathlib


def main():
    # Define cmd arguments and parse them
    parser = argparse.ArgumentParser(
        description="""Extracts detailed data from specified json lines source
        file containing output of the cuda_docs_spider.
        Writes output to several json files in the specified target directory:
        functions.json,
        defines.json,
        typedefs.json,
        enumerations.json,
        enum_members.json.
        """
    )
    parser.add_argument(
        "source",
        metavar="SOURCE",
        help="input file to be processed in json lines format",
    )
    parser.add_argument(
        "-t",
        "--target-directory",
        default=".",
        metavar="DIRECTORY",
        help="generate output files in DIRECTORY, defaults to '.'",
    )
    args = parser.parse_args()

    # Validate arguments
    if not pathlib.Path(args.source).is_file():
        parser.error(f"Invalid SOURCE argument, not a valid file: {args.source}")
    if not pathlib.Path(args.target_directory).is_dir():
        parser.error(
            f"Invalid DIRECTORY argument, not a valid directory: {args.target_directory}"
        )

    # TODO: implement


if __name__ == "__main__":
    main()
