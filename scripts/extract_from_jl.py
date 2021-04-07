import argparse
import json
import pathlib
import re


def extract_params(function_signature_str):
    match = re.match(r".*\(([^\)]*)\)", function_signature_str)
    if match:
        params_str = match.group(1)
        params = re.split(r", ", params_str) if params_str != "void" else []
        return params
    return []


def extract_functions_data(json_obj):
    descr = re.split(r"Parameters|Returns\n", json_obj["descr"].strip())
    documentation = f"{descr[0].strip()}\n"
    if len(descr) == 3:
        params_descr = re.sub(" +", " ", descr[1].strip())
        params_descr = re.sub(r"(\w+)\n", r"\1", params_descr)
        params_descr = re.sub(r" \n ", r"\n", params_descr)
        params_descr = f"\n{params_descr}"
        params_descr = re.sub(r"\n(\w+) -", r"\n- \1 -", params_descr)
        returns_descr = descr[2].strip()
        documentation = f"{documentation}\nParameters\n{params_descr}\n\nReturns\n\n{returns_descr}\n"
    return {
        "label": json_obj["name"],
        "detail": json_obj["value"],
        "documentation": documentation,
        "parameters": extract_params(json_obj["value"]),
    }


def extract_defines_data(json_obj):
    return {
        "label": json_obj["name"],
        "detail": f'#define {json_obj["name"]} {json_obj["value"]}',
        "documentation": json_obj["descr"].strip(),
    }


def extract_typedefs_data(json_obj):
    return {
        "label": json_obj["name"],
        "detail": json_obj["value"],
        "documentation": json_obj["descr"].strip(),
    }


def extract_enumerations_data(json_obj):
    return {
        "label": json_obj["name"],
        "detail": f'enum {json_obj["name"]}',
        "documentation": json_obj["descr"].strip(),
    }


def extract_enum_members_data(json_obj):
    return {
        "label": json_obj["name"],
        "detail": json_obj["value"],
        "documentation": json_obj["descr"].strip(),
    }


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
