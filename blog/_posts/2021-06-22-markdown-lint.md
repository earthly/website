---
title: "Linting Markdown And Documentation"
categories:
  + Tutorials
toc: true
author: Adam
internal-links:
 - just an example
---

### Writing Article Checklist

* [x] Write Outline
* [ ] Write Draft
* [ ] Fix Grammarly Errors
* [ ] Read Outloud
* [ ] Write 5 or more titles and pick the best on
* [ ] Create header image in canva
* [ ] Optional: Find ways to break up content with quotes or images
* [ ] Verify look of article locally
* [ ] Run mark down linter (`earthly +blog-lint-apply`)
* [ ] Add keywords for internal links to frontmatter
* [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
* [ ] Raise PR

## Outline

## Intro

Many linting, code formating and static analysis tools exist for code. You can use eslint, gofmt or many other static analysis tools to ensure you code stays in good shape.  Combine this with a great continous integration process and you can ensure that code stays in good shape.  But what about markdown files and documenation? How do you ensure you aren't committing spelling and grammar mistakes? How do you ensure your files are valid markdown and that the language you are using is clear and correct? You use a documentation linter.

Many tools exist for checking text files. This list is a place to start to find the best tool for your markdown and prose linting needs.

## Criteria 

For Ease of skimming I'll rate each tool based on this criteria.

 * Formating: The quality of finding errors in the formating of markdown files
 * Spelling: The quality of the spelling checking
 * Grammar: The quality of the ability to find errors
 * Writing Tips: The ability to suggest changes that can improve writing clarity.
 * Remediation: The ability to fix errors without manual intervention
 * Customization: How well the tool can be customized to fit your use case.  If you can't exclude a rule or disable a warning CI usage may be hard. The strongest tool support custom rules and documentation style guides.
 * IDE support: Ability to use in common code editors
 * CI / CLI Usage: Ability to be used command line and in a continous integration environemtn

## [Markdown Lint](https://github.com/DavidAnson/markdownlint)

Markdownlint is a node.js markdown linter which is easy to install and easy to customize. It is based on an early tool called [markdownlint](https://github.com/markdownlint/markdownlint). Both are great, but the nodejs tool is easy to install and easy to customize.  

You can disable specific rules inline ( `<!-- markdownlint-disable-file MD001 -->` ) and also setup a per project config in an `.markdownlintrc` file.  It also supports writing custom rules in javascript and is able to remediate many problems itself with the `fix` option:

```
markdownlint --fix "./_posts/*.md"
```

It doesn't handle spelling or grammar or sentence structure but for dealing with markdown structure it can't be beat.

## Coverage

* Formating: 5
* Spelling: 0
* Grammar: 0
* Clarity: 0

## Features

* Ease of Use: 5
* Remediation: 5
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## [mdspell](https://www.npmjs.com/package/markdown-spellcheck)

Mdspell is a tool specifically for spelling checking markdown documents. It can be installed like this:

```
npm i markdown-spellcheck -g    
```

It can be run on markdown files in an interactive mode that builds up a custom dictionary of exceptions that can then be used in CI.

```
mdspell -n -a --en-us  ./blog/_posts/2021-02-11-mitmproxy.md
```

The downsides are the dictionary will likely trigger on lots of words that are quite common but not found it its default dictionary and it make take some time to build up a list of exceptions. As a shortcut you might be able to find some larger `.spelling` files on github.

## Coverage

* Formating: 0
* Spelling: 5
* Grammar: 0
* Clarity: 0

## Features

* Ease of Use: 5
* Remediation: 5
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## [alexjs](https://alexjs.com/) 

alex does one thing: catches insensitive, inconsider writing.  It supports markdown files and works via command-line, CI or various IDEs. The specificity of alex is its strength and it serves an important goal.  For my rubric I am scoring it under clarity as catching insentisive writing certainly improves clarity.

## Coverage

* Formating: 0
* Spelling: 0
* Grammar: 0
* Clarity: 3

## Features

* Ease of Use: 5
* Remediation: 5
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## [Write-Good](https://github.com/btford/write-good)

write good is "developers who can't write good and wanna learn to do other stuff good too." The tools focus is on improving the clarity of writing. 

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
-------------
e-ca-certificates` is an excellent proof of concept, but if you want to run a do
                         ^^^^^^^^^
"excellent" is a weasel word on line 367 at column 84
```

write-good finds all kinds of interesting suggestions. It will highlight passive voice, cliches, weak adverbs and much more. Unfortunately it's not easy to exclude items or configure rules.  It might be useful as a writing suggestion tool but this lack of configurability means it likely can't be used in a continous intergation process.

## Coverage

* Formating: 0
* Spelling: 0
* Grammar: 0
* Clarity: 2

## Features

* Ease of Use: 5
* Remediation: 0
* Customization: 1
* IDE support: 2
* CI / CLI Support: 2

## [textlint](https://textlint.github.io/)

textlint is a pluggable linting tool that supports markdown, plaintext and some other formats.  The pluggin architecture means that it can offer the features of other tools by wrapping them. It has a [pluggin](https://github.com/textlint/textlint/wiki/Collection-of-textlint-rule#rules-english) for alex, write-good, and for many spell checkers and grammar checkers. The downside of this flexibility is that it is a bit harder to setup and configure.

Install

```
$ npm install textlint --global
# install each plugin
$ npm install --global textlint-rule-no-todo
....

```

Run:

```
textlint "docs/**"
```

textlint is configurable via an rc file ( `textlintrc` ) and has inline exclude rules( `<!-- textlint-disable ruleA,ruleB -->` ) -- which may make it a interesting way to use `write-good` or other tools that lack this functionality.

## Coverage

* Formating: 0
* Spelling: 3
* Grammar: 3
* Clarity: 4

## Features

* Ease of Use: 1
* Remediation: 3
* Customization: 4
* IDE support: 5
* CI / CLI Support: 2

## [proselint](http://proselint.com/)

proselint goes deep on writing clarity improvements in the same way the alex goes deep on inclusive writing:

> `proselint` places the world’s greatest writers and editors by your side, where they whisper suggestions on how to improve your prose. You’ll be guided by advice inspired by Bryan Garner, David Foster Wallace, Chuck Palahniuk, Steve Pinker, Mary Norris, Mark Twain, Elmore Leonard, George Orwell, Matthew Butterick, William Strunk, E. B. White, Philip Corbett, Ernest Gowers, and the editorial staff of the world’s finest literary magazines and newspapers, among others. Our goal is to aggregate knowledge about best practices in writing and to make that knowledge immediately accessible to all authors in the form of a linter for prose.

Some of the writing advice is really good though:

```
echo "The very first thing you'll see at the top of every (well-written) bash script " | proselint
<stdin>:1:5: weasel_words.very Substitute 'damn' every time you're inclined to write 'very'; your editor will delete it and the writing will be just as it should be.
```

```
echo "Thankfully, not all the advice I received was bad. " | proselint
<stdin>:1:2: skunked_terms.misc 'Thankfully,' is a bit of a skunked term — impossible to use without issue. Find some other way to say it.
```

```
echo "it is worth noting that both for CI and CD, the operating principles and coding philosophy are equally as important as the technical aspect of the implementation." | proselint
<stdin>:1:96: after_the_deadline.redundancy Redundancy. Use 'as' instead of 'equally as'.
```

This one is awesome:

```
echo "thought leaders" | proselint
<stdin>:1:2: cliches.garner 'thought leaders' is cliché.
```

```
 echo "One elephant in the room with ngrok is" | proselint
<stdin>:1:5: corporate_speak.misc Minimize your use of corporate catchphrases like this one.
```

Learning from all the best writers is a very lofty goal and proselint has several interesting sources of rules but I think they fall sort of the goal of collecting the worlds writing advice is a parsable form. Ignoring and excluding rules also seems cumbersome and not fully supported.

## Coverage

* Formating: 0
* Spelling: 0
* Grammar: 0
* Clarity: 5

## Features

* Ease of Use: 5
* Remediation: 0
* Customization: 0
* IDE support: 5
* CI / CLI Support: 2

## [Vale](https://github.com/errata-ai/vale)

Vale is the the creation of one person, Joseph Kato but it is feature rich. It supports spelling, grammar and clarity checks. It is extensible using a yaml rule format and is designed around the idea of a style guide, that is a specific house style that you put together and vale enforces.  It has an implementation of most `proselint` as a style guide, most of `write-good` as well as an implemenation of the [Microsoft Writing Style Guide](https://docs.microsoft.com/en-us/style-guide/welcome/) and the google 
[developer documentation style guide](https://developers.google.com/style/). My impression is that vale targets enterprize documentation teams who take the writing style of documents very serious.

Vale is fast and configurable but not necessarily easy to get started with. Intially, I couldn't get it to find any problems until I releazide it needs a config file to run:



```
MinAlertLevel = suggestion

[*]
BasedOnStyles = Vale
```
<figcaption>.vale.ini</figcaption>

Additionally to use it effectively you will need to copy an existing styleguide into your repository and customize it to your needs. Seperating the styles completely from the tool is the strength of this tool. It's also its weakness as the rules you build up are specific to your repo. It takes active effort to share these rules online. Besides the official vale styleguides [Buildkite](https://buildkite.com/blog/linting-the-buildkite-docs), [Linode](https://github.com/linode/docs/tree/develop/ci/vale/styles), and [Write The Docs](https://github.com/testthedocs/vale-styles) have rules online that you can copy into your repo or use as inspiration for your own rules. 

If you are taking linting documentation whether it be written in markdown, AsciiDoc or plaintext seriously and can take the time to setup a style that works for you then Vale is the way to go.  The rules of most other tools are likely to implementable in vale using a custom rule.

## Coverage

* Formating: 2
* Spelling: 5
* Grammar: 5
* Clarity: 5

## Features

* Ease of Use: 1
* Remediation: 0
* Customization: 5
* IDE support: 5
* CI / CLI Support: 5

## List of Styles
 * https://github.com/search?q=topic%3Avale-linter-style+org%3Atestthedocs+fork%3Atrue
 * 

## Summary

Whether its a simple readme, or complex technical documentaion, a myriad of tools exist for testing and linting english prose.  Vale is the clear leader and combined with  Markdownlint and run in a continous intergration system should ensure that documents are spelling correctly, grammatically correct and writen in a properly formatted and exclusive way. 