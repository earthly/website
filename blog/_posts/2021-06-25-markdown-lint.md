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
last_modified_at: 2023-07-19
---
**This article introduces prose linting tools. If you value precise software documentation, Earthly can integrate with Vale and markdownlint to automate and improve your CI builds. [Explore more](https://cloud.earthly.dev/login).**

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

~~~
markdownlint --fix "./_posts/*.md"
~~~

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

~~~
npm i markdown-spellcheck -g    
~~~

You can run it on markdown files in an interactive mode that builds up a custom dictionary of exceptions. You can then use that list later in a continuous integration process.

~~~
mdspell -n -a --en-us  ./blog/_posts/2021-02-11-mitmproxy.md
~~~

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

~~~
npm install -g write-good
~~~

Run:

~~~
$ write-good ./blog/_posts/2021-02-11-mitmproxy.md
here are several ways to accomplish this.
                         ^^^^^^^^^^
"accomplish" is wordy or unneeded on line 305 at column 26
-------------
e-ca-certificates` is an excellent proof of concept, but if you want to run a do
                         ^^^^^^^^^
"excellent" is a weasel word on line 367 at column 84
~~~

`write-good` has many exciting suggestions. It will highlight passive voice, cliches, weak adverbs, and much more. Unfortunately, it's not easy to exclude items or configure rules. It might be helpful as a writing suggestion tool, but this lack of configurability means you will have difficulty using it in a continuous integration process.

### Coverage

* Formatting: 0
* Spelling: 0
* Grammar: 0
* Clarity: 2

### Features

* Ease of Use: 5
* Remediation: 0
* Customization: 1
* IDE support: 2
* CI / CLI Support: 2

## [textlint](https://textlint.github.io/)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/textlint.png --picture --img width="1200px" --alt {{ textlint website }} %}
</div>

`textlint` is a pluggable linting tool that supports markdown, plain text, and HTML. The plug-in architecture means that it can offer the features of some of the previous items by wrapping them up as a plug-in. It has a [plug-in](https://github.com/textlint/textlint/wiki/Collection-of-textlint-rule#rules-english) for `alex`, `write-good`, and for many spell checkers and grammar checkers. The downside of this flexibility is that it is a bit harder to set up and configure: you have to install each plug-in separately.

Install:

~~~
$ npm install textlint --global
# install each plugin
$ npm install --global textlint-rule-no-todo
....

~~~

Run:

~~~
textlint "docs/**"
~~~

`textlint` is configurable via an `textlintrc` and has inline exclude rules ( `<!-- textlint-disable ruleA,ruleB -->` ) -- which may make it a possible way to use `write-good` or other tools that lack this functionality.

### Coverage

* Formatting: 0
* Spelling: 3
* Grammar: 3
* Clarity: 4

### Features

* Ease of Use: 1
* Remediation: 3
* Customization: 4
* IDE support: 5
* CI / CLI Support: 2

## [proselint](http://proselint.com/)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/proselint.png --picture --img width="1200px" --alt {{ Prose Lint }} %}
</div>

`proselint` goes deep on writing clarity improvements in the same way the `alex` goes deep on inclusive writing:

> `proselint` places the world's greatest writers and editors by your side, where they whisper suggestions on how to improve your prose. You'll be guided by advice inspired by Bryan Garner, David Foster Wallace, Chuck Palahniuk, Steve Pinker, Mary Norris, Mark Twain, Elmore Leonard, George Orwell, Matthew Butterick, William Strunk, E. B. White, Philip Corbett, Ernest Gowers, and the editorial staff of the world's finest literary magazines and newspapers, among others. Our goal is to aggregate knowledge about best practices in writing and to make that knowledge immediately accessible to all authors in the form of a linter for prose.

Some of the writing advice included is great:

~~~
echo "The very first thing you'll see at the top of every (well-written) bash script " | proselint
<stdin>:1:5: weasel_words.very Substitute 'damn' every time you're inclined to write 'very'; your editor will delete it and the writing will be just as it should be.
~~~

~~~
echo "Thankfully, not all the advice I received was bad. " | proselint
<stdin>:1:2: skunked_terms.misc 'Thankfully,' is a bit of a skunked term — impossible to use without issue. Find some other way to say it.
~~~

~~~
echo "it is worth noting that both for CI and CD, the operating principles and coding philosophy are equally as important as the technical aspect of the implementation." | proselint
<stdin>:1:96: after_the_deadline.redundancy Redundancy. Use 'as' instead of 'equally as'.
~~~

This one is awesome considering the context of the [original article](/blog/thought-leaders/):

~~~
echo "thought leaders" | proselint
<stdin>:1:2: cliches.garner 'thought leaders' is cliché.
~~~

~~~
 echo "One elephant in the room with ngrok is" | proselint
<stdin>:1:5: corporate_speak.misc Minimize your use of corporate catchphrases like this one.
~~~

Learning from all the best writers is a very lofty objective, and `proselint` has accumulated some valuable rules, but it falls short of its goal of collecting all the worlds writing advice in a parsable form. Ignoring and excluding rules are also not fully supported.

### Coverage

* Formatting: 0
* Spelling: 0
* Grammar: 0
* Clarity: 5

### Features

* Ease of Use: 5
* Remediation: 0
* Customization: 0
* IDE support: 5
* CI / CLI Support: 2

## [Vale](https://github.com/errata-ai/vale)

<div class="wide">
 {% picture content2 {{site.pimages}}{{page.slug}}/vale.png --picture --img width="1200px" --alt {{ Vale Website }} %}
 </div>

Vale, created by Joseph Kato, supports spelling, grammar, and clarity checks. It is extendable using a YAML rule format and is designed around the idea of a style guide -- a specific house style that you put together and vale enforces. It has an implementation of most `proselint` as a style guide, most of `write-good`, as well as the [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/welcome/) and the Google
[developer documentation style guide](https://developers.google.com/style/). Vale is targeted directly at the Docs-as-Code community and documentation teams, who take the writing style of documents very seriously.

Vale is fast and configurable but not necessarily easy to get started with. Initially, I couldn't get it to find any problems until I realized that it needs a config file to run:

~~~
MinAlertLevel = suggestion

[*]
BasedOnStyles = Vale
~~~

<figcaption>.vale.ini</figcaption>

Additionally, to use it effectively, you will need to copy an existing style-guide into your repository. Separating the styles from the tool is Vale's biggest strength. It's also could be a weakness as the rules you build up are specific to your repository. It is easy to write and customize rules but hard to share them back as they need to live in your source code repository.

 Besides the official Vale style guides [Buildkite](https://buildkite.com/blog/linting-the-buildkite-docs), [Linode](https://github.com/linode/docs/tree/develop/ci/vale/styles), and [Write The Docs](https://github.com/testthedocs/vale-styles) have rules online that you can copy into your repo or use as inspiration for your own rules.

If you are taking linting documentation seriously and can take the time to set up a style that works for you, then Vale is the way to go. The rules of most other tools can be implemented inside value, and many already are.

### Coverage

* Formatting: 2
* Spelling: 5
* Grammar: 5
* Clarity: 5

### Features

* Ease of Use: 1
* Remediation: 0
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

### Vale Styles

* [Official Styles](https://github.com/topics/vale-linter-style)\
* [Write The Docs Styles](https://github.com/search?q=topic%3Avale-linter-style+org%3Atestthedocs+fork%3Atrue)
* [Grammarly Clone in Vale](https://github.com/testthedocs/Openly)

## Summary

There are several tools available for testing and linting English prose, ranging from simple spell-checks to comprehensive style guides for your software documentation. If you're open to investing time, `Vale` is a top choice due to its flexible rules. Coupling `Vale` with `markdownlint` in a CI build ensures correct spelling, grammar, and appropriate formatting.

And while you're doing prose automation, why not give your build processes an easy upgrade? Check out [Earthly](https://www.earthly.dev/). This blog, for instance, uses `Vale` and `markdownlint` in an [Earthfile](https://earthly.dev/) for every commit to avoid errors. And if you need simpler options, `mdspell` combined with `markdownlint` is a good start. Remember, automation is key to maintaining high-quality software documentation.
