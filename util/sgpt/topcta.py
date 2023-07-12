import os
import argparse
import subprocess
from textwrap import dedent

from typing import List, Optional
import guidance
from typing import List, Dict, Tuple
import contextlib
import os

gpt4 = guidance.llms.OpenAI("gpt-4")

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

    template = dedent(f"""
        **We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. {article_sentence} {tie_in_sentence}. [Check us out](/).**
                """).strip()
    return template

def add_paragraph_if_word_missing(filename):
    # Read the file
    with open(filename, 'r') as file:
        content = file.read()

    # Identify the frontmatter by finding the end index of the second '---'
    frontmatter_end = find_nth(content, '---', 2)

    # If frontmatter end exists
    if frontmatter_end != -1:
        frontmatter = content[:frontmatter_end + len('---')]  # Include '---' in frontmatter
        rest_of_file = content[frontmatter_end + len('---'):]  # rest_of_file starts after '---'
    else:
        frontmatter = ''
        rest_of_file = content

    if "funnel:" in frontmatter or "News" in frontmatter or " Write Outline" in rest_of_file:
        # print("Is Earthly focused, skipping.")
        return
    # Ensure we have more than the frontmatter
    else:
        first_paragraph_found = False
        paragraphs = rest_of_file.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                first_paragraph = paragraph.strip()
                first_paragraph_found = True
                break

        # Check if 'sgpt' is in the first paragraph
        if first_paragraph_found and 'sgpt' in first_paragraph:
            print(f"Starting: {filename}")
            # print("shell gpt paragraph found. updating it.")
            # Remove the first paragraph (up to the first double line break)
            replace = build_paragraph(filename) 
            replace = "<!--sgpt-->"+shorter(replace)
            rest_of_article = rest_of_file.lstrip().split("\n\n", 1)[1]
            new_content = frontmatter + '\n' + replace + '\n\n' + rest_of_article
            with open(filename, 'w') as file:
                file.write(new_content)
        # elif 'https://earthly.dev/' not in first_paragraph and 'earthly.dev' not in first_paragraph:
        #     # print("CTA not found. Adding shell-gpt one.")
        #     replace = build_paragraph(filename) 
        #     new_content = frontmatter + '\n' + replace + '\n\n' + rest_of_file.strip()
        #     with open(filename, 'w') as file:
        #         file.write(new_content)

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

examples = [
    {'input': dedent("""
    **We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about 5 Blogs for Scala's Birthday. Earthly is a powerful build tool that can be used in conjunction with Scala projects, making it a valuable tool for developers interested in building and managing their Scala code efficiently. [Check us out](/).**
    """),
    'output': """
    **We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. Earthly is a powerful build tool that can be used with Scala projects. [Check it out](/).**
    """},

    {'input': dedent("""
    **We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about installing `matplotlib` in a Docker container. Earthly is a powerful build tool that can greatly simplify the process of building and managing Docker containers, making it an ideal tool for readers interested in installing `matplotlib` in a Docker container. [Check us out](/).**
    """),
    'output': """
    **We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. It's an ideal tool for dealing with your python container builds. [Check it out](/).**
"""},
]

def shorter(input: str) -> str:
    score = guidance(dedent('''
    {{#system~}}
    Write a shortened version of this call to action for getting readers of an article interested in Earthly. 
    {{~/system}}
    {{~#each examples}}
    {{#user~}}
    {{this.input}}
    {{~/user}}
    {{#assistant~}}
    {{this.output}}
    {{~/assistant}}    
    {{~/each}}
    {{#user~}} 
    {{input}}
    {{~/user}}
    {{#assistant~}}
    {{gen "answer"}}
    {{~/assistant}}   
    '''), llm=gpt4, silent=True)
    with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
        out = score(examples=examples,input=input) 
    return out["answer"].strip()


    

def main():
    parser = argparse.ArgumentParser(description='Add an excerpt to a markdown file.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')

    args = parser.parse_args()

    if args.dir:
        # Process each markdown file in the directory
        for root, dirs, files in os.walk(args.dir):
            for file in files[:50]:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    # print(f"Starting: {path}")
                    add_paragraph_if_word_missing(os.path.join(root, file))
                    # print(f"Finishing: {path}")
    elif args.file:
        add_paragraph_if_word_missing(args.file)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == "__main__":
    main()
