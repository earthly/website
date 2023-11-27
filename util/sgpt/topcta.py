import os
import argparse
import subprocess
from textwrap import dedent

from typing import List, Optional
import guidance
from typing import List, Dict, Tuple
# import contextlib
import os
from pathlib import Path
from textwrap import dedent
import guidance
import pprint

# gpt-4-1106-preview is cheaper and with more context
# But doesn't work with guidance's latest, so must revert back in CI
# Hand patched on Adam's machine
gpt4 = guidance.llms.OpenAI("gpt-4-1106-preview")

gpt35turbo = guidance.llms.OpenAI("gpt-3.5-turbo-16k")

rerun = True
debug = True

def log(s : str):
    if debug:
        print(s)

def build_paragraph(content):
    score = guidance(dedent("""
    {{#system~}}
    You summarize markdown blog posts.
    {{~/system}}
    {{#user~}}
   

    Post:
    ---
    {{content}} 
    ---
    Can you summarize this blog post in a three word sentence of the form 'This article is about ....'? Do no put the summary in quotes.
    Examples:
    - This article is about gmail API changes.
    - This article is about Python CLIs. 
    - This article is about OpenCore company's using MITMproxy. 
                            
    Can you summarize this blog post in a short sentence of the form 'This article is about ....'? 
    {{~/user}}
    {{#assistant~}}
    {{gen 'summary' max_tokens=100 temperature=0}}
    {{~/assistant}}
    """),llm=gpt4, silent=False)
    out = score(content=content)
    article_sentence = out["summary"].strip()
    log(f"Summary:\n"+ article_sentence)

    score = guidance(dedent("""
    {{#system~}}
    You summarize markdown blog posts.
    {{~/system}}
    {{#user~}}
   

    Post:
    ---
    {{content}} 
    ---
    Can you provide a short sentence explaining why Earthly would be interested to readers of this article? Earthly is an open source build tool for CI. The sentence should be of the form 'Earthly is popular with users of bash.' 
    {{~/user}}
    {{#assistant~}}
    {{gen 'summary' max_tokens=100 temperature=0}}
    {{~/assistant}}
    """),llm=gpt4, silent=False)
    out = score(content=content)
    tie_in_sentence = out["summary"].strip().split(".",1)[0]
    log(f"Earthly Tie in:\n"+ tie_in_sentence)

    template = dedent(f"""
        **{article_sentence} {tie_in_sentence}. [Check us out](/).**
                """).strip()
    return template

def add_paragraph_if_word_missing(filename, dryrun):
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

    if "News" in frontmatter or " Write Outline" in rest_of_file or "topcta: false" in frontmatter:
        print(f"{filename}:Is Earthly focused, skipping.")
        return
    # elif "iframe" in rest_of_file:
    #     print(f"{filename}:Youtube CTA, skipping.")
    #     return
    else:
        first_paragraph_found = False
        paragraphs = rest_of_file.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                first_paragraph = paragraph.strip()
                first_paragraph_found = True
                break

        if first_paragraph_found and 'sgpt' in first_paragraph and rerun:
            print(f"Updating CTA:\t {filename}")
            if not dryrun:
                # print("shell gpt paragraph found. updating it.")
                # Remove the first paragraph (up to the first double line break)
                file_content = Path(filename).read_text()
                replace = build_paragraph(file_content) 
                replace = shorter(replace)
                replace = "<!--sgpt-->**"+clearer(replace)+"**"
                # replace = "<!--sgpt-->" + replace
                rest_of_article = rest_of_file.lstrip().split("\n\n", 1)[1]
                new_content = frontmatter + '\n' + replace + '\n\n' + rest_of_article
                with open(filename, 'w') as file:
                    file.write(new_content)
        elif 'https://earthly.dev/' not in first_paragraph and 'earthly.dev' not in first_paragraph:
            print(f"Adding CTA:\t {filename}")
            if not dryrun:
                replace = build_paragraph(filename) 
                # replace = "<!--sgpt-->"+shorter(replace)
                replace = "<!--sgpt-->" + replace
                new_content = frontmatter + '\n' + replace + '\n\n' + rest_of_file.strip()
                with open(filename, 'w') as file:
                    file.write(new_content)
        else:
            print(f"Not Adding CTA:\t {filename}") 

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

shorter_examples = [
    {'input': dedent("""
    This article is a celebration of Scala's Birthday and shares some favorite Scala blogs. Earthly is a powerful build tool that can be used in conjunction with Scala projects, making it a valuable tool for developers interested in building and managing their Scala code efficiently. [Check us out](/).
    """),
    'output': """
    Join us in celebrating Scala's Birthday with our top picks of Scala blogs. We're Earthly: A powerful build tool that can be used with Scala projects. [Check us out](/).
    """},

    {'input': dedent("""
    This article is about installing `matplotlib` in a Docker container. Earthly is a powerful build tool that can greatly simplify the process of building and managing Docker containers, making it an ideal tool for readers interested in installing `matplotlib` in a Docker container. [Learn More](/).
    """),
    'output': """
    This article is about installing `matplotlib` in a Docker container. Earthly is a powerful build tool that can greatly simplify the process of building and managing Docker containers. [Check it out](/).
    """},
    {'input': dedent("""
    This article is about monorepo versus polyrepo strategies. Earthly is favored by developers navigating the complexities of monorepo and polyrepo build strategies. [Check it out](/).
    """),
    'output': """
    In this article, you'll delve into the intricacies of monorepo versus polyrepo strategies. If you're grappling with these build architectures, Earthly can streamline your workflow, no matter which path you choose. [Learn more about Earthly](/).
    """},
]

def shorter(input: str) -> str:
    score = guidance(dedent('''
    {{#system~}}
    <background> 
    Here are some key things to know about Earthly and why it is used in tech:

    Earthly is an open source build automation tool released in 2020. It allows you to define builds using a domain-specific language called Earthfile.

    Key features of Earthly include:
    Reproducible builds - Earthly containers isolate dependencies and build steps so you get consistent, repeatable builds regardless of the environment.
    Portable builds - Earthfiles define each step so you can build on any platform that supports containers like Docker.
    Declarative syntax - Earthfiles use a simple, declarative syntax to define steps, reducing boilerplate.
    Built-in caching - Earthly caches steps and layers to optimize incremental builds.
    Parallel builds - Earthly can distribute work across containers to build parts of a project in parallel.

    Reasons developers use Earthly:
    Simpler configuration than bash scripts or Makefiles.
    Avoid dependency conflicts by isolating dependencies in containers.
    Consistent builds across different environments (local dev, CI, production).
    Efficient caching for faster build times.
    Can build and integrate with any language or framework that runs in containers.
    Integrates with CI systems like GitHub Actions.
    Enables building complex multi-language, multi-component projects.
    Earthly is commonly used for building, testing and shipping applications, especially those with components in different languages. It simplifies build automation for monorepos and complex projects.

    Overall, Earthly is a developer-focused build tool that leverages containers to provide reproducible, portable and parallel builds for modern applications. Its declarative Earthfile syntax and built-in caching help optimize build performance.
    Earthly helps with continuous development but not with continuous deployment and works with any programming language.  
    Earthly helps with build software on linux, using containers. It doesn't help with every SDLC process, but it improves build times which can help other steps indirectly.
    </background> 

    Task:
    Revise this call to action to make it more engaging and informative for the Earthly blog readers. The call to action should clearly introduce the specific topic of the article and emphasize the unique insights or benefits offered by Earthly. Aim for a concise, casual tone, while ensuring clarity and directness in language.
    
    Guidelines:

    1. Explicit Topic Reference: Start with a clear statement about the article's topic. For example, "In this detailed article, you will learn about [specific topic]..."
    2. Highlight Earthly's Unique Perspective: Emphasize what makes Earthly's connection to the topic special or beneficial. For instance, "If you're grappling with [specific topic] vs [specific topic], Earthly can streamline your build, no matter which path you choose."
    3. Sign Post: It's important that the text signpost the article by saying something like "This article is about [topic]" or "In this article you will learn". "Discover C#!" is less good than "In this article you'll discover C#" because it lacks explicit reference to the article.
    4. Casual and Direct: Shorter and casual phrasing is preferred. William Zinsser's advice for writing clearly, actively and directly should be followed.
    5. Curosity By Connection: A great call to action generates curiosity or interest in Earthly by connecting to the topic of the article. But if the connection is not clear, a straight-forward request to look at Earthly is second best option.

    When in doubt, stay close to:
    {{input}} 
    Do not sure the word Dive.
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
    {{gen 'options' n=7 temperature=0.5 max_tokens=500}}
    {{~/assistant}}
    {{#user~}}
    Can you please comment on the pros and cons of each of these replacements?

    This text will be a very brief advertisement at the top of a blog post on the Earthly blog.

    Shorter is better. More connected to the topic at hand is better. Natural sounding, like a casual recommendation is better.
    
    It's important that the text signpost the article by saying something like "This article is about X" or "In this article you'll learn X". For this reason, "Discover X!" is worse than "In this article you'll discover X" because it lacks explicit reference to the article.

    Overstating things, with many adjectives, is worse. Implying Earthly does something it does not is worse. 

    ---{{#each options}}
    Option {{@index}}: {{this}}{{/each}}
    ---
    {{~/user}}
    {{#assistant~}}
    {{gen 'thinking' temperature=0 max_tokens=2000}}
    {{~/assistant}}
    {{#user~}} 
    Please return the text of the best option, based on above thinking.
    {{~/user}}
    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}
    '''), llm=gpt4, silent=False, logging=True)
    out = score(examples=shorter_examples,input=input) 
    log(out.__str__())
    return out["answer"].strip()

def clearer(input: str) -> str:
    score = guidance(dedent('''
    {{#system~}}
    You are William Zinsser. You improve writing by making it simpler and more active. You are given a short paragraph of text and return an improved version. If it can't be improved, you return it verbatim.
    {{~/system}}
    {{#user~}} 
    {{input}}
    {{~/user}}
    {{#assistant~}}
    {{gen 'answer' temperature=0.0 max_tokens=1500}}
    {{~/assistant}}
    '''), llm=gpt4, silent=False, logging=True)
    out = score(examples=shorter_examples,input=input) 
    log(out.__str__())
    return out["answer"].strip()

def main():
    parser = argparse.ArgumentParser(description='Add an excerpt to a markdown file.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')
    parser.add_argument('--dryrun', help='Dry run mode', action='store_true')

    args = parser.parse_args()

    if args.dryrun:
        print("Dryrun mode activated. No changes will be made.")

    if args.dir:
        for root, dirs, files in os.walk(args.dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    add_paragraph_if_word_missing(os.path.join(root, file), args.dryrun)
    elif args.file:
        add_paragraph_if_word_missing(args.file, args.dryrun)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == "__main__":
    main()
