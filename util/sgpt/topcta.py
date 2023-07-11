import os
import argparse
import subprocess
from textwrap import dedent

def build_paragraph(filename):
    command1 = dedent(f"""
            cat "{filename}" | sgpt --model gpt-3.5-turbo-16k "This is a post in markdown. I need a three word summary of the article in sentence form of 'This article is about ....' .  For example: 'This article is about large scale builds.' or 'This article is about python list comprehensions.'. It should be just the topic in that form of sentence and should make sense." 
            """).strip() 
    result = subprocess.run(command1, capture_output=True, text=True, shell=True)
    article_sentence = result.stdout.strip()

    command2 = dedent(f"""
             cat "{filename}" | sgpt --model gpt-3.5-turbo-16k "This is a post in markdown. I need a very short sentence explaining why Earthly would be interested to readers of this article. So summarize the article and then return a small bridging sentence. Earthly is an open source build tool for CI. The sentence should be of the form 'Earthly is popular with users of bash.' Example: 'Earthly is great in combination with Dockerfiles.', 'Earthly is particularly useful if you are working with Monorepos', 'If you are looking for a way to build your Ruby code then Earthly is a great option.' It should be a sentence that bridges between the topic and Earthly.
             
             This is a post in markdown. I need a very short sentence explaining why Earthly would be interested to readers of this article."
                      """)
    result = subprocess.run(command2, capture_output=True, text=True, shell=True)
    tie_in_sentence = result.stdout.strip().split(".",1)[0] # Earthly is particularly useful if you're working with a Monorepo.
    print(f"tie in: {tie_in_sentence}")

    template = dedent(f"""
        <!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. {article_sentence} {tie_in_sentence}. [Check us out](/).**
                """).strip()
    return template

def add_paragraph_if_word_missing(filename):
    # Read the file
    with open(filename, 'r') as file:
        content = file.read()

    # Split the markdown file by the '---' delimiter to isolate the frontmatter
    parts = content.split('---')

    if "funnel:" in content:
        print("Is Earthly focused, skipping.")
        return
    # Ensure we have more than the frontmatter
    if len(parts) > 2:
        first_paragraph_found = False
        paragraphs = parts[2].split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                first_paragraph = paragraph.strip()
                first_paragraph_found = True
                break
        
        replace = build_paragraph(filename) #"<!--sgpt-->This is the Earthly nonsense paragraph."
        # Check if 'sgpt' is in the first paragraph
        if first_paragraph_found and 'sgpt' in first_paragraph:
            print("shell gpt paragraph found. updating it.")
            # Remove the first paragraph (up to the first double line break)
            rest_of_article = parts[2].lstrip().split("\n\n", 1)[1]
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
