import argparse
import os
from pathlib import Path

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
        if line.strip() == "---":
            if in_front_matter and not category_inserted:
                # Insert category just before closing the front matter
                new_lines.append(f"categories:\n  - {new_category}\n")
                category_inserted = True
            in_front_matter = not in_front_matter

        new_lines.append(line)

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

def main() -> None:
    parser = argparse.ArgumentParser(description='Set a new category in a markdown file.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')
    parser.add_argument('--category', help='The new category to set.', required=True)
    parser.add_argument('--dryrun', help='Dry run it.', action='store_true')

    args = parser.parse_args()

    if args.dryrun:
        print("Dry run mode activated. No changes will be made.")

    if args.dir:
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    update_category_in_md_file(path, args.category, args.dryrun)
    elif args.file:
        update_category_in_md_file(args.file, args.category, args.dryrun)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == '__main__':
    main()
