import argparse
import subprocess
import os

def add_excerpt_to_md_file(filename):
    command = f'cat "{filename}" | sgpt --role excerpt --model gpt-3.5-turbo-16k "This is a post in markdown. I need a two sentence  summary that will make people want to read it that is casual in tone."'

    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    excerpt = result.stdout.strip()

    with open(filename, 'r') as f:
        lines = f.readlines()

    assert lines[0].strip() == "---", "The file does not start with '---'."

    excerpt_exists = False
    excerpt_start = 0


    for i, line in enumerate(lines[1:], start=1):
        if line.strip().startswith('excerpt:'):
            # Start replacing the existing excerpt
            excerpt_start = i
            excerpt_exists = True
        elif excerpt_exists:
            # If the line is indented, it's part of the existing excerpt and should be removed
            if line.startswith('    '):
                lines[i] = ''
            else:
                # We've reached the end of the existing excerpt
                lines[excerpt_start] = f"excerpt: |\n    {excerpt}\n"
                break
        elif not excerpt_exists and line.strip() == "---":
            # Add the excerpt before the second ---
            lines.insert(i, f"excerpt: |\n    {excerpt}\n")
            break

    with open(filename, 'w') as f:
        f.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description='Add an excerpt to a markdown file.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')

    args = parser.parse_args()

    if args.dir:
        # Process each markdown file in the directory
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    print(f"Starting: {path}")
                    add_excerpt_to_md_file(os.path.join(root, file))
                    print(f"Finishing: {path}")
    elif args.file:
        add_excerpt_to_md_file(args.file)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == '__main__':
    main()
