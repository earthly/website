import argparse
import os
from pathlib import Path
from textwrap import dedent

import guidance
from guidance import assistant, gen, system, user

gpt35turbo = guidance.models.OpenAI("gpt-3.5-turbo-16k")

def get_excerpt(content : str) -> str:
  lm = gpt35turbo
  with system():
    lm += "You generate two sentence summaries from markdown content."
  with user():
    lm += dedent(f"""
            Can you summarize this in two sentences?
            ---
            {content}
            ---
            """)
  with assistant():
    lm += gen('summary', max_tokens=100)
  return lm['summary'].strip()

def add_excerpt_to_md_file(filename : str, dryrun : bool) -> None:

    with open(filename, 'r') as f:
        lines = f.readlines()

    excerpt_exists = False

    for i, line in enumerate(lines[1:], start=1):
        if line.strip().startswith('excerpt:'):
            excerpt_exists = True
        elif not excerpt_exists and line.strip() == "---":
            break

    if not excerpt_exists:
        print(f"Starting: {filename}")
        if not dryrun:
            # Generate the excerpt
            file_content = Path(filename).read_text()
            excerpt = get_excerpt(file_content)

            # Insert the excerpt
            lines.insert(i, f"excerpt: |\n    {excerpt}\n")

    with open(filename, 'w') as f:
        f.writelines(lines)

def main() -> None:
    parser = argparse.ArgumentParser(description='Add an excerpt to a markdown file.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')
    parser.add_argument('--dryrun', help='Dry run it.', action='store_true')

    args = parser.parse_args()

    if args.dryrun:
        print("Dryrun mode activated. No changes will be made.")

    if args.dir:
        # Process each markdown file in the directory
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith('.md') and not file.startswith('2029'):
                    path = os.path.join(root, file)
                    add_excerpt_to_md_file(path, args.dryrun)
    elif args.file:
        add_excerpt_to_md_file(args.file, args.dryrun)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == '__main__':
    main()
