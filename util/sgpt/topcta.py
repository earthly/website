import os
import argparse

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
            # Remove the first paragraph (up to the first double line break)
            rest_of_article = parts[2].split("\n\n", 1)[1]
            parts[2] = '\n' + replace + '\n\n' + rest_of_article
            new_content = '---'.join(parts)
            with open(filename, 'w') as file:
                file.write(new_content)
        elif 'earthly' not in first_paragraph and 'Earthly' not in first_paragraph:
            # 'sgpt' not found, add a new paragraph with 'sgpt'
            new_content = parts[0] + '---' + parts[1] + '---\n' + replace + '\n' + parts[2]
            with open(filename, 'w') as file:
                file.write(new_content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The name of the markdown file")
    args = parser.parse_args()
    add_paragraph_if_word_missing(args.filename)

if __name__ == "__main__":
    main()
