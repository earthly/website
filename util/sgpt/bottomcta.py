import argparse
import subprocess
import os
from typing import Optional
from textwrap import dedent
import contextlib
import yaml
import guidance

gpt4 = guidance.llms.OpenAI("gpt-4")

# should_cache = True
should_cache = False

def get_summary(lines: str) -> str:
    score = guidance(dedent('''
    {{#system~}}
    You summarize markdown blog posts.
    {{~/system}}
    {{#user~}}
   

    Post:
    ---
    {{lines}} 
    ---
    Can you summarize this blog post?
    {{~/user}}
    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}
    '''), llm=gpt4, caching=should_cache)
    out = run_llm_program(score, lines=lines)
    return out["answer"].strip() 

def add_tie_in(summary: str, conclusion : str) -> str:    
    tie_in = generate_tie_in(summary, conclusion)
    combined = merge_tie_in(conclusion, summary, tie_in)
    return combined

def merge_tie_in(summary: str, conclusion : str, tie_in : str) -> str:
    examples = [
        {
        'conclusion': dedent("""
        Awk has more to it than this. There are more built-in variables and built-in functions. It has range patterns and substitution rules, and you can easily use it to modify content, not just add things up.

        If you want to learn more about Awk, [The Awk Programming Language](https://www.amazon.ca/AWK-Programming-Language-Alfred-Aho/dp/020107981X/) is the definitive book. It covers the language in depth. It also covers how to build a small programming language in Awk, how to build a database in Awk, and some other fun projects.
        """),
        'tie_in' : "Also, if you're the type of person who's not afraid to do things on the command line then you might like [Earthly](/)",
        'result' :  dedent("""
        Awk has more to it than this. There are more built-in variables and built-in functions. It has range patterns and substitution rules, and you can easily use it to modify content, not just add things up.

        If you want to learn more about Awk, [The Awk Programming Language](https://www.amazon.ca/AWK-Programming-Language-Alfred-Aho/dp/020107981X/) is the definitive book. It covers the language in depth. It also covers how to build a small programming language in Awk, how to build a database in Awk, and some other fun projects. Also, if you're the type of person who's not afraid to do things on the command line then you might like [Earthly](/)
        """)
        },
         {
        'conclusion': dedent("""
        Awk has more to it than this. There are more built-in variables and built-in functions. It has range patterns and substitution rules, and you can easily use it to modify content, not just add things up.

        If you want to learn more about Awk, [The Awk Programming Language](https://www.amazon.ca/AWK-Programming-Language-Alfred-Aho/dp/020107981X/) is the definitive book. It covers the language in depth. It also covers how to build a small programming language in Awk, how to build a database in Awk, and some other fun projects.
        """),
        'tie_in' : "Also, if you're the type of person who's not afraid to do things on the command line then you might like [Earthly](/)",
        'result' :  dedent("""
        Awk has more to it than this. There are more built-in variables and built-in functions. It has range patterns and substitution rules, and you can easily use it to modify content, not just add things up.

        If you want to learn more about Awk, [The Awk Programming Language](https://www.amazon.ca/AWK-Programming-Language-Alfred-Aho/dp/020107981X/) is the definitive book. It covers the language in depth. It also covers how to build a small programming language in Awk, how to build a database in Awk, and some other fun projects. 
                           
        (Also, if you're the type of person who's not afraid to do things on the command line then you might like [Earthly](/))
        """)
        },
    ]
    score = guidance(dedent('''
        {{#system~}}
        Background:
        ---
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
        {{~/system}}
        {{~#each examples}}
        {{#user~}}
        Tie-in:
        {{this.tie_in}}

        Post Conclusion:
        {{this.conclusion}} 
        ---
        Can you add the tie in to the conclusion in a way that makes sense and blends in? Rewrite it if needed. 
        {{~/user}}
        {{#assistant~}}
        {{this.result}}
        {{~/assistant}}    
        {{~/each}}
        {{#user~}}
        Tie-in:
        {{tie_in}}

        Post Conclusion:
        {{conclusion}} 
        ---
        Can you add the tie in to the conclusion in a way that makes sense and blends in? Rewrite it if needed. 
        {{~/user}}
        {{#assistant~}}
        {{gen 'answer' temperature=0 max_tokens=2000}}
        {{~/assistant}}
    '''), llm=gpt4, caching=should_cache)
    out = run_llm_program(score, conclusion=conclusion, tie_in=tie_in, examples=examples, summary=summary)
    return out["answer"].strip()

def generate_tie_in(summary: str, conclusion : str) -> str:
    examples = [
    {'summary': dedent("""
    Learn the basics of Awk, a powerful text processing tool, in this informative article. 
    """),
    'conclusion': dedent("""
    Awk has more to it than this. There are more built-in variables and built-in functions. It has range patterns and substitution rules, and you can easily use it to modify content, not just add things up.

    If you want to learn more about Awk, [The Awk Programming Language](https://www.amazon.ca/AWK-Programming-Language-Alfred-Aho/dp/020107981X/) is the definitive book. It covers the language in depth. It also covers how to build a small programming language in Awk, how to build a database in Awk, and some other fun projects.
    """),
    'result' : "Also, if you're the type of person who's not afraid to do things on the command line then you might like [Earthly](/)"},
 
]
    score = guidance(dedent('''
        {{#system~}}
        Background:
        ---
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
        {{~/system}}
        {{~#each examples}}
        {{#user~}}
        Summary:
        {{this.summary}}

        Post Conclusion:
        {{this.conclusion}} 
        ---
        Can write a short sentence with a markdown link to Earthly that will explain the reader of this article might be interested in Earthly?
        {{~/user}}
        {{#assistant~}}
        {{this.result}}
        {{~/assistant}}    
        {{~/each}}
        {{#user~}}
        Summary:
        {{summary}}

        Post Conclusion:
        {{conclusion}} 
        ---
        Can write a short sentence with a markdown link to Earthly that will explain the reader of this article might be interested in Earthly?
        {{~/user}}
        {{#assistant~}}
        {{gen 'answer' temperature=0 max_tokens=500}}
        {{~/assistant}}
    '''), llm=gpt4, caching=should_cache)
    out = run_llm_program(score, conclusion=conclusion, examples=examples, summary=summary) 
    return conclusion + out["answer"].strip()

def run_llm_program(program, *args, **kwargs):
    with open("log.txt", "a") as f, contextlib.redirect_stdout(
        f
    ), contextlib.redirect_stderr(f):
        return program(*args, **kwargs)

def add_comment_to_section(text_after_last_heading: str, excerpt : str) -> str:
    comment = '<!--sgpt-->\n'
    if comment in text_after_last_heading:
        text_after_last_heading = add_tie_in(excerpt, text_after_last_heading.replace(comment, ''))
        print('Updating...')
    else:
        print('Adding...')
        text_after_last_heading = add_tie_in(excerpt, text_after_last_heading)
    return text_after_last_heading

def update_text_after_last_heading(filename: str) -> Optional[None]:
    with open(filename, 'r') as f:
        content = f.read()
        
    excerpt = get_summary(content)
    lines = content.split('\n')
    for i in reversed(range(len(lines))):
        # Check if the line starts with a heading
        if lines[i].startswith('#'):
            # Get all lines after the last heading
            text_after_last_heading = '\n'.join(lines[i+1:])
            # If 'Earthly' is in the text, skip the file
            if 'Earthly' in text_after_last_heading:
                return
            # If the line starts with '{%', remove it
            text_after_last_heading = '\n'.join(line for line in text_after_last_heading.split('\n') if not line.strip().startswith('{%'))
            # Add the comment to the beginning of the section
            text_after_last_heading = add_comment_to_section(text_after_last_heading, excerpt)
            lines[i+1:] = text_after_last_heading.split('\n')
            break
            
    updated_content = '\n'.join(lines)

    with open(filename, 'w') as f:
        f.write(updated_content)


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
                    update_text_after_last_heading(os.path.join(root, file))
                    print(f"Finishing: {path}")
    elif args.file:
        update_text_after_last_heading(args.file)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == '__main__':
    main()
