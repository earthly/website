import argparse
import concurrent.futures
import os
import pickle
import re
from datetime import date, datetime
from textwrap import dedent
from typing import Tuple

import guidance
import portalocker
from guidance import assistant, gen, system, user

gpt4 = guidance.models.OpenAI("gpt-4-1106-preview")
gpt35turbo = guidance.models.OpenAI("gpt-3.5-turbo-16k")

rerun = False
debug = False

cache = True
GLOBAL_CACHE = {}
CACHE_FILE = 'get_new_cta.pkl'

def load_cache() -> None:
    global GLOBAL_CACHE
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as file:
            GLOBAL_CACHE = pickle.load(file)
    else:
        GLOBAL_CACHE = {}

def write_cache() -> None:
    global GLOBAL_CACHE
    with open(CACHE_FILE, 'wb') as file:
        # Lock the file before writing
        portalocker.lock(file, portalocker.LOCK_EX)
        pickle.dump(GLOBAL_CACHE, file)

def log(s : str) -> None:
    if debug:
        print(s)

def add_top_cta_if_conditions(filename : str, dryrun : bool) -> None:
    def find_nth(haystack : str, needle : str, n : int) -> int:
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start

    def split_article(content : str) -> Tuple[str,str]:
        # Identify the frontmatter by finding the end index of the second '---'
        frontmatter_end = find_nth(content, '---', 2)

        # If frontmatter end exists
        if frontmatter_end != -1:
            frontmatter = content[:frontmatter_end + len('---')]  # Include '---' in frontmatter
            rest_of_file = content[frontmatter_end + len('---'):]  # rest_of_file starts after '---'
        else:
            frontmatter = ''
            rest_of_file = content
        return frontmatter,rest_of_file

    def first_paragraph(content : str) -> str:
        paragraphs = content.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip():
                first_paragraph = paragraph.strip()
                break
        return first_paragraph

    def is_cta(text : str) -> bool:
        pattern1 = r"\*\*(.*?)\*\*"
        pattern2 = r"<!--sgpt-->\*\*(.*?)\*\*"

        if re.search(pattern1, text) or re.search(pattern2, text):
            return True
        else:
            return False

    # Read the file
    with open(filename, 'r') as file:
        content = file.read()

    frontmatter,rest_of_file = split_article(content)

    if " Write Outline" in rest_of_file or "topcta: false" in frontmatter:
        if not dryrun:
            print(f"{filename}:Is Earthly focused, skipping.")
        return
    else:
        first_paragraph1 = first_paragraph(rest_of_file)

        if is_cta(first_paragraph1) and rerun:
            print(f"Updating CTA:\t {filename}")
            if not dryrun:
                # Drop old leading paragraph
                rest_of_file = rest_of_file.lstrip().split("\n\n", 1)[1].strip()
                add_new_cta(filename,frontmatter,rest_of_file)
        elif not is_cta(first_paragraph1):
            print(f"Adding CTA:\t {filename}")
            if not dryrun:
                add_new_cta(filename,frontmatter,rest_of_file)
        else:
            if not dryrun:
                print(f"Not Adding CTA:\t {filename}")

def add_new_cta(filename : str, frontmatter : str, rest_of_file : str) -> None:
    replace = get_new_cta_with_cache(filename,rest_of_file)
    new_content = frontmatter + '\n' + replace + '\n\n' + rest_of_file
    with open(filename, 'w') as file:
        file.write(new_content)
    print(f"Wrote:\t{filename}")

def get_new_cta_with_cache(filename : str, rest_of_file : str) -> str:
    global GLOBAL_CACHE
    # Check if result is in cache
    if filename in GLOBAL_CACHE and cache:
        print("Cache hit")
        return GLOBAL_CACHE[filename]

    # Call the original function and store the result in cache
    result = get_new_cta(filename, rest_of_file)
    GLOBAL_CACHE[filename] = result

    # Write the updated cache to the file
    write_cache()

    return result

def get_new_cta(filename : str, rest_of_file : str) -> str:
    replace = build_cta(rest_of_file)
    replace = make_shorter(replace)
    replace = "**"+make_cleaner(replace)+"**"
    return replace

earthly_facts = dedent("""
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

                Earthly uses containeriation to build, but has nothing to do with running containers in production.
                Earthly has lots to do with building containers, and CI things before production. It's often used to speed up building build artifacts.
                You might not use Earhtly to build your database, but if you use a database, you might use earthly to build your applciations.

                Earthly is primarily a build automation tool designed to simplify and standardize the process of building software across various environments.
                While Earthly can be a part of a broader DevOps toolkit that includes these Kubernetes tools, it doesn't directly streamline or interact with the functionalities of Kubernetes or kubernetes tools. Each of these tools serves a different aspect of the containerized application lifecycle.
                Earthly is used during the build and CI stages. Kubernetes is part of the runtime.

                Overall, Earthly is a developer-focused build tool that leverages containers to provide reproducible, portable and parallel builds for modern applications. Its declarative Earthfile syntax and built-in caching help optimize build performance.
                Earthly helps with continuous development but not with continuous deployment and works with any programming language.
                Earthly helps with build software on linux, using containers. It doesn't help with every SDLC process, but it improves build times which can help other steps indirectly.
""")

def build_cta(content : str) -> str:
    def get_summary(content: str) -> str:
        lm = gpt35turbo
        with system():
            lm += "You generate one paragraph, three sentence summaries from markdown content."

        with user():
            lm += dedent(f"""
                <content>
                {content}
                </content>
                You generate two sentence summaries from markdown content.
                Can you summarize this entire article into one descriptive paragraph?
                """)

        with assistant():
            lm += gen('summary', max_tokens=100, temperature=0)

        return lm['summary'].strip()

    def this_article_sentence(content: str) -> str:
        lm = gpt4
        with system():
            lm += "You summarize markdown blog posts."

        with user():
            lm += dedent(f"""
                Post:
                ---
                {content}
                ---
                Can you summarize this blog post in a three word sentence of the form 'This article is about ....'? Do not put the summary in quotes.
                Examples:
                - This article is about gmail API changes.
                - This blog post is about Python CLIs.
                - This article is about OpenCore company's using MITMproxy.

                Can you summarize this blog post in a short sentence of the form 'This article is about ....'?
                """)

        with assistant():
            lm += gen('summary', max_tokens=100, temperature=0)

        article_sentence = lm['summary'].strip()
        log("Summary:\n" + article_sentence)
        return article_sentence

    def earthly_statement(content: str) -> str:
        lm = gpt4  # Assuming gpt4 is defined elsewhere in your code
        with system():
            lm += dedent(f"""
                You: You are an expert on Earthly and use your background knowledge to assist with Earthly questions.
                <background>
                {earthly_facts}
                </background>

                Task: Can you provide a short sentence explaining why Earthly would be interested to readers of this article? Earthly is an open source build tool for CI. The sentence should be of the form 'Earthly is popular with users of bash.' The sentence should be a statement.

                Examples:
                - If you're a Jenkins fan, Earthly could give your build a boost.
                - Earthly works well with Go Builds.
                - If you're into Azure Functions, you'll love how Earthly optimizes your CI build tools.
                - If you're into command line tools, then Earthly is worth a look.

                Please provide a list of potential options.
                """)

        with user():
            lm += content

        with assistant():
            lm += gen('options', max_tokens=1500, temperature=0)

        with user():
            lm += "Can you please comment on the pros and cons of each of these. Sparking curiosity in the reader is a goal. Not misleading about what Earthly is is another goal. Being concise is a goal."

        with assistant():
            lm += gen('thinking', temperature=0, max_tokens=2000)

        with user():
            lm += "Please return the text of the best option, based on the above thinking."

        with assistant():
            lm += gen('answer', temperature=0, max_tokens=500)

        tie_in_sentence = lm['answer'].strip().split(".", 1)[0]
        log(lm.__str__())
        log("Earthly Tie in:\n" + tie_in_sentence)
        return tie_in_sentence

    summary = get_summary(content)
    article_sentence = this_article_sentence(summary)
    tie_in_sentence = earthly_statement(summary)
    template = dedent(f"""
        **{article_sentence} {tie_in_sentence}. [Check it out](https://cloud.earthly.dev/login).**
                """).strip()
    return template

shorter_examples = [
    {'input': dedent("""
    This article is a celebration of Scala's Birthday and shares some favorite Scala blogs. Earthly is a powerful build tool that can be used in conjunction with Scala projects, making it a valuable tool for developers interested in building and managing their Scala code efficiently. [Check us out](https://cloud.earthly.dev/login/).
    """),
    'output': """
    Join us in celebrating Scala's Birthday with our top picks of Scala blogs. We're Earthly: A powerful build tool that can be used with Scala projects. [Check us out](https://cloud.earthly.dev/login/).
    """},

    {'input': dedent("""
    This article is about installing `matplotlib` in a Docker container. Earthly is a powerful build tool that can greatly simplify the process of building and managing Docker containers, making it an ideal tool for readers interested in installing `matplotlib` in a Docker container. [Learn More](https://cloud.earthly.dev/login/).
    """),
    'output': """
    This article is about installing `matplotlib` in a Docker container. Earthly is a powerful build tool that can greatly simplify the process of building and managing Docker containers. [Check it out](https://cloud.earthly.dev/login/).
    """},
    {'input': dedent("""
    This article is about monorepo versus polyrepo strategies. Earthly is favored by developers navigating the complexities of monorepo and polyrepo build strategies. [Check it out](https://cloud.earthly.dev/login/).
    """),
    'output': """
    In this article, you'll delve into the intricacies of monorepo versus polyrepo strategies. If you're grappling with these build architectures, Earthly can streamline your workflow, no matter which path you choose. [Learn more about Earthly](https://cloud.earthly.dev/login/).
    """},
]

def make_shorter(input: str) -> str:
    lm = gpt4  # Assuming gpt4 is defined elsewhere in your code
    with system():
        lm += dedent(f"""
            <background>
            {earthly_facts}
            </background>

            Task:
            Revise this call to action to make it more engaging and informative for the Earthly blog readers. The call to action should clearly introduce the specific topic of the article and emphasize the unique insights or benefits offered by Earthly. Aim for a concise, casual tone, while ensuring clarity and directness in language.

            When in doubt, stay close to:
            {input}
            Do not use the word Dive. Only return the revised call to action.

            Revised should be made of these parts:
            Summary: Each should start with a sentence summarizing the article.
            Statement: Each should then have a statement about Earthly.
            Link: Each should then end with a link.

            Earthly statement should be a direct statement of something about Earthly. It should not be an invitation.
            It should be direct, assertive statements rather than those that invite the reader to discover or explore further.
            The statement should contain clear, unambiguous statements that directly convey information.
            """)

    # Process each example using a for loop
    for example in shorter_examples:
        with user():
            lm += example['input']

        with assistant():
            lm += example['output']

    with user():
        lm += input

    lm2 = gpt4
    with assistant():
        for i in range(1,7):
            r = lm + gen('options', temperature=0.1, max_tokens=500)
            lm2 += dedent(f"""
                          ---
                          Option {i}:
                          {r["options"]}
                        """)

    with user():
        lm2 += dedent(f"""
            ---
            Can you please comment on the pros and cons of each of these replacements and which should be rejected?

            Rejection Criteria:
            Summary: Each should start with a sentence summarizing the article.
            Statement: Each should then have a statement about Earthly.
            Link: Each should then end with a link.

            Reject An Option If:
            1. Summary: Reject if summary does not mention the article directly. Or mentions the article, or content last.
            "In this article, we'll dive into the latest DevOps practices." - Good.
            "We'll dive into the latest DevOps practices, in this article." - Bad

            2. Statement: Reject statement if not a statement. Earthly statement should be a direct statement of something about Earthly. It should not be an invitation.
            "If you're a DevOps enthusiast, Earthly can streamline your CI workflows with containerized build automation." - Good.
            "If you're a DevOps enthusiast, discover how Earthly can streamline your CI workflows with containerized build automation." - Bad - Use of discover

            3. Link: The link should be a short invitation to learn more about earthly. It should be a link.
            Do not reject based on the link, unless the link is missing.
            "[Check it out](https://cloud.earthly.dev/login)" - Good
            "[Learn more about Earthly](https://cloud.earthly.dev/login)" - Good

            After rejecting options, please go through remaining options and state pros and cons based on Other criteria.

            Other criteria:
            Shorter is better. More connected to the topic at hand is better. Natural sounding and casual is better.

            It's important that the first sentence signpost the article by saying something like "This article is about X" or "In this article you'll learn X". For this reason, "Discover X!" is worse than "In this article you'll discover X" because it lacks explicit reference to the article.

            It's important that, following the sign posting, the next part is a statement about Earthly. This statement should connect the topic to Earthly without overstating Earthly's benefits. The statement can be direct or implied second person or direct second person. Like "If leveraging zsh for command-line speed, Earthly can streamline your build processes."

            Overstating things, with many adjectives, is worse. Implying Earthly does something it does not is worse.

            If options all rejected, choose the default:

            ---
            Default: {input}
            ---""")

    with assistant():
        lm2 += gen('thinking', temperature=0, max_tokens=2000)

    with user():
        lm2 += "Please return the text of the best option, based on the above thinking."

    with assistant():
        lm2 += gen('answer', temperature=0, max_tokens=500)

    log(str(lm2))
    return lm2["answer"].strip()

def make_cleaner(input: str) -> str:
    def clean_string(s : str) -> str:
        return s.strip('"*')

    lm = gpt4  # Assuming gpt4 is defined elsewhere in your code
    with system():
        lm += dedent("""
            You are William Zinsser. You improve writing by making it simpler and more active. You are given a short paragraph of text and return an improved version. If it can't be improved, you return it verbatim.

            Your general editing rules:
            Clarity: Ensure your writing is clear and easy to understand. Every sentence should convey its meaning without ambiguity.
            Simplicity: Use simple words and sentences. Avoid complex vocabulary where a simpler word would work just as well.
            Strong Verbs: Use strong, specific verbs to convey action. They often eliminate the need for adverbs and make the writing more vivid and precise.
            Avoiding Clichés and Redundancies: Steer clear of clichés and redundant phrases.

            Specific editing rules:
            The resulting paragraph should be made of these parts:
            Summary: Each should start with a sentence summarizing the article.
            Statement: Each should then have a statement about Earthly.
            Link: Each should then end with a link.

            Earthly statement should be a direct statement of something about Earthly. It should not be an invitation.
            It should be direct, assertive statements rather than those that invite the reader to discover or explore further.
            The statement should contain clear, unambiguous statements that directly convey information.

            Specific editing rules take precedence over your general editing rules.
            You are given a short paragraph of text and return an improved version. If it can't be improved, you return it verbatim.

            Important: Do Not change the meaning.
            Important: Do Not Remove the markdown link.

            First discuss what improvements could be made. Discuss some options.
            """)

    with user():
        lm += input

    with assistant():
        lm += gen('options', max_tokens=1500, temperature=0)

    with user():
        lm += "Can you please comment on the pros and cons of each of these changes."

    with assistant():
        lm += gen('thinking', temperature=0, max_tokens=2000)

    with user():
        lm += "Identify the best option based on the previous analysis and return only the text of that option, without any additional context, explanation, or analysis. Please provide only the selected text."

    with assistant():
        lm += gen('answer', temperature=0, max_tokens=500)

    # Execute LLM with the accumulated instructions
    log(str(lm))
    return clean_string(lm["answer"].strip())

def parse_date(date_str : str) -> date:
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def is_file_newer_than(file_path : str, filter_date : date) -> bool:
    # Extract the date from the filename
    date_str = file_path.split('/')[-1].split('-')[:3]
    file_date = datetime.strptime('-'.join(date_str), '%Y-%m-%d').date()
    return file_date > filter_date

def main() -> None:
    load_cache()
    parser = argparse.ArgumentParser(description='Add an excerpt to a markdown file.')
    parser.add_argument('--dir', help='The directory containing the markdown files.')
    parser.add_argument('--file', help='The path to a single markdown file.')
    parser.add_argument('--dryrun', help='Dry run mode', action='store_true',default=False)
    parser.add_argument('--after-date', help='Filter files modified after this date (format: YYYY-MM-DD)', type=str, default=None)

    args = parser.parse_args()

    if args.dryrun:
        print("Dryrun mode activated. No changes will be made.")

    if args.after_date:
        filter_date = parse_date(args.after_date)
    else:
        filter_date = None

    markdown_files = []

    if args.dir:
        # Accumulate Markdown file paths
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    if not filter_date or is_file_newer_than(path, filter_date):
                        markdown_files.append(path)

        markdown_files.sort()
        # markdown_files = markdown_files[:100]

        # Dispatch the tasks using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futures = [executor.submit(add_top_cta_if_conditions, file_path, args.dryrun) for file_path in markdown_files]
            print("Waiting...")
            concurrent.futures.wait(futures)  # Wait for all futures to complete
        write_cache()
    elif args.file:
        add_top_cta_if_conditions(args.file, args.dryrun)
    else:
        print("Please provide either --dir or --file.")
        exit(1)

if __name__ == "__main__":
    main()
