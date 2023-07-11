import os
import argparse
from textwrap import dedent

process = dedent(f"""
            cat "$(post)" | sgpt --model gpt-3.5-turbo-16k "This is a post in markdown. I need a three word summary of the article in sentence form of 'This article is about ....' .  For example: 'This article is about large scale builds.' or 'This article is about python list comprehensions.'. It should be just the topic in that form of sentence and should make sense." 
            """) 

def add_paragraph_if_word_missing(filename):
    # Read the file
    with open(filename, 'r') as file:
        content = file.read()

    # Split the markdown file by the '---' delimiter to isolate the frontmatter
    parts = content.split('---')

    # Ensure we have more than the frontmatter
    if len(parts) > 2:
        first_paragraph_found = False
        paragraphs = parts[2].split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                first_paragraph = paragraph.strip()
                first_paragraph_found = True
                break
        
        replace = "<!--sgpt-->This is the Earthly nonsense paragraph."
        # Check if 'sgpt' is in the first paragraph
        if first_paragraph_found and 'sgpt' in first_paragraph:
            print("shell gpt paragraph found. updating it.")
            # Remove the first paragraph (up to the first double line break)
            rest_of_article = parts[2].split("\n\n", 1)[1]
            parts[2] = '\n' + replace + '\n\n' + rest_of_article
            new_content = '---'.join(parts)
            with open(filename, 'w') as file:
                file.write(new_content)
        elif 'https://earthly.dev/' not in first_paragraph and 'earthly.dev' not in first_paragraph:
            print("CTA not found. Adding shell-gpt one.")
            new_content = parts[0] + '---' + parts[1] + '---\n' + replace + '\n\n' + parts[2].strip()
            with open(filename, 'w') as file:
                file.write(new_content)
        else:
            print(f"Starting: {filename}")
            print("Existing hand written CTA found. Doing nothing")

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
                    add_paragraph_if_word_missing(os.path.join(root, file))
                    print(f"Finishing: {path}")
    elif args.file:
        add_paragraph_if_word_missing(args.file)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == "__main__":
    main()
