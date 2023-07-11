import argparse
import subprocess
import os

def add_excerpt_to_md_file(filename):
    # Construct the shell command
    command = f'cat "{filename}" | sgpt --role excerpt --model gpt-3.5-turbo-16k "This is a post in markdown. I need a two sentence  summary that will make people want to read it that is casual in tone."'

    # Call the shell command to generate the excerpt
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    excerpt = result.stdout.strip()

    with open(filename, 'r') as f:
        lines = f.readlines()

     # Assert the first line is ---
    assert lines[0].strip() == "---", "The file does not start with '---'."

    # Flag to check if excerpt already exists
    excerpt_exists = False

    # Start from the second line
    for i, line in enumerate(lines[1:], start=1):
        if line.strip().startswith('excerpt:'):
            # Replace the existing excerpt
            lines[i] = f"excerpt: {excerpt}\n"
            excerpt_exists = True
            break
        if not excerpt_exists and line.strip() == "---":
            # Add the excerpt before the second ---
            lines.insert(i, f"excerpt: {excerpt}\n")
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
