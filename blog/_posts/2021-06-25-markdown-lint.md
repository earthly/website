---
title: "Linting Markdown And Documentation"
categories:
  - Tutorials
author: Adam
internal-links:
 - vale
 - markdown lint
 - markdown
 - spell
 - spelling
excerpt: |
    Learn how to ensure the quality of your markdown files and documentation with linting tools. Discover various tools like markdownlint, mdspell, alex, write-good, textlint, proselint, and Vale that can help you catch formatting errors, spelling mistakes, grammar errors, and improve writing clarity. Find the right tool for your needs and automate their usage to maintain high-quality documentation.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

Many linting, code formatting, and static analysis tools exist for code. You can use `eslint`, `gofmt`, or many other static analysis tools, combined with a great continuous integration process, and ensure that your code stays in good shape. But what about markdown files and documentation? How do you ensure you aren't committing spelling and grammar mistakes? How do you ensure your files are valid markdown and that the language you are using is clear and correct? You can do this and more with a documentation linter.

Many tools exist for finding problems in text files. You can use this list as a starting point for finding the markdown and prose linting tools that best fit your needs.

<div class="notice--success notice--big">

## Docs as Code

The movement behind testing and linting prose is known as [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/), and the [Writing The Docs](https://www.writethedocs.org/) website is a great place to learn more.

</div>

## Criteria

For Ease of skimming, I'll rate each tool based on this criteria:

* **Formatting:** The ability to find errors in the formatting of text files (markdown, txt, asciidoc).
* **Spelling:** The ability to find spelling mistakes.
* **Grammar:** The ability to detect grammar errors.
* **Clarity:** The ability to suggest changes that can improve writing clarity.

Additionally, I will rate tools based on their feature set:

* **Remediation:** The ability to fix errors without manual intervention.
* **Customization:** How well the tool can be customized to fit your use case. If you can't exclude a rule or disable a warning, CI usage may be challenging. The most robust tools support custom rules and documentation style guides.
* **Integrated Developer Environment (IDE) support:** Ability to use in common code editors
* **Continuous Integration (CI) / Command Line Interface (CLI) Usage:** Ability to be used at the command line and in a continuous integration environment.

## [Markdown Lint](https://github.com/DavidAnson/markdownlint)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/markdownlint4.png --picture --img width="1200px" --alt {{ markdown lint GitHub Readme }} %}
 </div>

`markdownlint` is a node.js markdown linter that is easy to install and easy to customize. It is based on an earlier Ruby tool, also called [markdownlint](https://github.com/markdownlint/markdownlint). Both are great, but the Node.js tool is easy to install and easy to customize.  

You can disable specific rules inline ( `<!-- markdownlint-disable-file MD001 -->` ) and set up a per-project config in a `.markdownlintrc` file. It also supports writing custom rules in JavaScript and can remediate many problems itself with the `fix` option:

```
markdownlint --fix "./_posts/*.md"
```

It doesn't handle spelling, grammar, or sentence structure, but it can't be beaten for dealing with markdown structure and it has a great online [demo site](https://dlaa.me/markdownlint/).

### Coverage

* Formatting: 5
* Spelling: 0
* Grammar: 0
* Clarity: 0

### Features

* Ease of Use: 5
* Remediation: 5
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## [mdspell](https://www.npmjs.com/package/markdown-spellcheck)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/mdspell1.png --picture --img width="1200px" --alt {{ mdspell readme }} %}
 </div>

`mdspell` is a tool specifically for spelling checking markdown documents. Install it like this:

```
npm i markdown-spellcheck -g    
```

You can run it on markdown files in an interactive mode that builds up a custom dictionary of exceptions. You can then use that list later in a continuous integration process.

```
mdspell -n -a --en-us  ./blog/_posts/2021-02-11-mitmproxy.md
```

The downsides of `mdspell` are that the dictionary will likely complain about lots of words that are quite common. It may take some time to build up a list of exceptions. As a shortcut, you might be able to find some more `.spelling` files on GitHub.

### Coverage

* Formatting: 0
* Spelling: 5
* Grammar: 0
* Clarity: 0

### Features

* Ease of Use: 5
* Remediation: 5
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## [alex](https://alexjs.com/)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/alex.png --picture --img width="1200px" --alt {{ alex.js readme }} %}
</div>

`alex` does one thing: catches insensitive and inconsiderate writing. It supports markdown files, and works via command-line, and has various IDE integrations. The specificity of `alex` is its strength. For my rubric, I am scoring it under clarity as catching insensitive writing certainly improves clarity.

### Coverage

* Formatting: 0
* Spelling: 0
* Grammar: 0
* Clarity: 3

### Features

* Ease of Use: 5
* Remediation: 5
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## [`write-good`](https://github.com/btford/write-good)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/write-good.png --picture --img width="1200px" --alt {{ write-good on GitHub }} %}
 </div>

`write-good` is designed for "developers who can't write good and wanna learn to do other stuff good too." The tool's focus is on improving the clarity of writing (and helping developers write well).

Install:

```
npm install -g write-good
```

Run:

```
$ write-good ./blog/_posts/2021-02-11-mitmproxy.md
here are several ways to accomplish this.
                         ^^^^^^^^^^
"accomplish" is wordy or unneeded on line 305 at column 26