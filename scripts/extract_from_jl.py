import argparse
import json
import pathlib


def extract_functions_data(json_obj):
    # TODO: implement
    return json_obj


def extract_defines_data(json_obj):
    # TODO: implement
    return json_obj


def extract_typedefs_data(json_obj):
    # TODO: implement
    return json_obj


def extract_enumerations_data(json_obj):
    # TODO: implement
    return json_obj


def extract_enum_members_data(json_obj):
    # TODO: implement
    return json_obj


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

    # Extract data from source json lines file
    functions_json = []
    defines_json = []
    typedefs_json = []
    enumerations_json = []
    enum_members_json = []
    with open(args.source) as source_file:
        for line in source_file:
            json_obj = json.loads(line)
            if json_obj["kind"] == "function":
                functions_json.append(extract_functions_data(json_obj))
            elif json_obj["kind"] == "define":
                defines_json.append(extract_defines_data(json_obj))
            elif json_obj["kind"] == "typedef":
                typedefs_json.append(extract_typedefs_data(json_obj))
            elif json_obj["kind"] == "enum":
                enumerations_json.append(extract_enumerations_data(json_obj))
            elif json_obj["kind"] == "enum-member":
                enum_members_json.append(extract_enum_members_data(json_obj))

    # Write extracted data to output files
    with open(f"{args.target_directory}/functions.json", "w") as functions_file:
        json.dump(functions_json, functions_file, indent=4)
    with open(f"{args.target_directory}/defines.json", "w") as defines_file:
        json.dump(defines_json, defines_file, indent=4)
    with open(f"{args.target_directory}/typedefs.json", "w") as typedefs_file:
        json.dump(typedefs_json, typedefs_file, indent=4)
    with open(f"{args.target_directory}/enumerations.json", "w") as enumerations_file:
        json.dump(enumerations_json, enumerations_file, indent=4)
    with open(f"{args.target_directory}/enum_members.json", "w") as enum_members_file:
        json.dump(enum_members_json, enum_members_file, indent=4)


if __name__ == "__main__":
    main()
