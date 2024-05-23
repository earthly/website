import argparse
from pathlib import Path

import yaml


def remove_existing_categories(lines):
    """Remove existing categories from the front matter."""
    in_front_matter = False
    new_lines = []
    skip_lines = False

    for line in lines:
        if line.strip() == "---":
            if in_front_matter:
                in_front_matter = False
            else:
                in_front_matter = True
            new_lines.append(line)
            continue

        if in_front_matter and line.strip().startswith("categories:"):
            skip_lines = True
            continue

        if skip_lines and line.strip().startswith("-"):
            continue
        else:
            skip_lines = False

        new_lines.append(line)

    return new_lines

def add_new_category(lines, new_category):
    """Add a new category to the front matter."""
    in_front_matter = False
    new_lines = []
    category_inserted = False

    for line in lines:
        new_lines.append(line)
        if line.strip() == "---" and not in_front_matter:
            in_front_matter = True
            continue
        if in_front_matter and line.strip() == "---" and not category_inserted:
            new_lines.insert(-1, f"categories:\n  - {new_category}\n")
            category_inserted = True
            in_front_matter = False

    return new_lines

def update_category_in_md_file(filename: str, new_category: str, dryrun: bool) -> None:
    with open(filename, 'r') as f:
        lines = f.readlines()

    lines = remove_existing_categories(lines)
    lines = add_new_category(lines, new_category)

    if not dryrun:
        with open(filename, 'w') as f:
            f.writelines(lines)
    else:
        print(f"Dry run: would update categories in {filename} to [{new_category}]")

def process_files_in_directory(directory: str, category: str, slugs: list, dryrun: bool) -> None:
    for slug in slugs:
        matching_files = list(Path(directory).rglob(f"*{slug}.md"))
        for file in matching_files:
            update_category_in_md_file(file, category, dryrun)

def main() -> None:
    parser = argparse.ArgumentParser(description='Set a new category in markdown files based on slugs.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')
    parser.add_argument('--category', help='The new category to set.', required=True)
    parser.add_argument('--dryrun', help='Dry run it.', action='store_true')

    args = parser.parse_args()

    if args.dryrun:
        print("Dry run mode activated. No changes will be made.")

    config_file = "blog/_data/categories1.yml"  # Path to the YAML configuration file

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    slugs = config.get(args.category, [])

    if not slugs:
        print(f"No slugs found for category '{args.category}' in the configuration file.")
        exit(1)

    if args.dir:
        process_files_in_directory(args.dir, args.category, slugs, args.dryrun)
    elif args.file:
        update_category_in_md_file(args.file, args.category, args.dryrun)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == '__main__':
    main()
