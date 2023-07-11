---
title: "Don't Configure Control Flow"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - YAML
excerpt: Learn why using YAML for control flow configuration can lead to complex and hard-to-understand code, and why it's better to use existing programming languages or write a parser instead. Discover the pitfalls of using YAML as a programming language and explore alternative tools like Makefile or Earthfile.
---

When I first worked with YAML config, it was a breath of fresh air. No more XML! No angle brackets. It was so plain and clear.

But now, too often, when I see YAML, it's a complex mess of nested lists hundreds of lines long. So where did things go wrong?

To find out, let's take a small problem, use YAML to make it more declarative, step by step, and see where the wheels fall off. In doing this, I think I can draw a clear line for when something should be config and when it shouldn't.

## Demonstration

So I have this little build script I run as part of the build process for my podcast website.

It's a pretty old-fashioned Bash script that checks some conditions and runs some stuff. The end result is some files end up where Netlify needs them, so they show up on the website.

It's something like this:

~~~{.bash caption="build.sh"}
#!/bin/bash

if [ -n "$(echo 'First Condition')" ]; then
    # First step goes here
    echo "Hello, World!" &
fi

if [ -n "$(echo 'Second Condition')" ]; then
      # Second step goes here
     ls &
fi

# Third thing goes here
wait
echo "Third thing:"
~~~

So what it does is run two tasks in the background, if they need to be run, based on the if condition, and then wait on them to run the final third command.

The real version is messier than this, but I thought it'd be interesting to code to a declarative and configurable version of this. Can I make it easier to understand, or will it just get worse?

## YAML

The first step is to pull some of the commands out of Bash and use YAML instead.

Let's refactor to `commands.yaml`:

~~~{.yaml caption="commands.yaml"}
commands:
  - echo "Hello, World!"
  - ls
  - echo "Third thing:"

~~~

Then I need a CI runner to actually do my CI process. Let's use Python to whip one up:

~~~{.python caption="job_runner.py"}
import yaml
import subprocess

with open("commands.yaml", "r") as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

commands = yaml_data["commands"]

for command in commands:
    subprocess.run(command, shell=True, check=True)

~~~

## Conditionals

This works great, except the conditionals for the first two steps are missing.

I could just inline the ifs into the YAML fields, but that seems a little hacky.

So no problem, I can add conditions:

~~~{.yaml caption="commands.yaml"}
commands:
  - command: echo "Hello, World!"
    if: '[ -n "$(echo 'First Condition')" ]'
  - command: ls
   if: '[ -n "$(echo 'Second Condition')" ]'
  - command: echo "No if condition"
~~~

## Execution Order

Now the thing we are missing is running the first two jobs in parallel and then waiting on them for the last.

So we change things to this:

~~~{.yaml caption="commands.yaml"}
commands:
  - command: one 
    run: echo "Hello, World!"
    if: '[ -n "$(echo 'First Condition')" ]'
  - command: two
   run: ls
   if: '[ -n "$(echo 'Second Condition')" ]'
  - command: three
    depends-on[one,two]
    run: echo "Third thing"
~~~

That is strictly more generic than the `WAIT` version written in Bash because you can have dependencies of dependencies, but it does match how GitHub Actions structures things.

Here is the same idea in GitHub Actions:

~~~{.yaml caption="sample_GHA.yaml"}
name: GitHub Actions Demo
jobs:
  one: 
    name: One
    runs-on: ubuntu-latest
    steps:
      -  run: |-
              echo "Hello, World!"
         if: '[ -n "$(echo 'First Condition')" ]'
  two: 
    name: Two
    runs-on: ubuntu-latest
    steps:
      -  run: |-
              echo "Hello, World!"
         if: '[ -n "$(echo 'Second Condition')" ]'
  three: 
    name: three
    runs-on: ubuntu-latest
   needs: [one,two]
    steps:
      -  run: |-
              echo "Third thing"
~~~

I've excluded a few details to save space, but you can see that this whole thing is starting to get verbose. There is the specific YAML layout to understand, but also the semantics of how this is all executed. Just like a real programming language, I need to understand how things are written down, but also, once written down, what they cause to happen.

Travis CI has a slightly different approach to programming parallelism in YAML:

~~~{.yaml caption="sample_Travis.yaml"}
language: minimal

jobs:
  include:
    - stage: parallel tasks
      name: "First Condition"
      script: echo "Hello, World!"
      if: env(FIRST_CONDITION) = "true"
    - stage: parallel tasks
      name: "Second Condition"
      script: ls
      if: env(SECOND_CONDITION) = "true"
    - stage: sequential task
      name: "Third thing"
      script: echo "Third thing:"

~~~

Stages are executed in order, each waiting on the next but items that share a stage are executed in parallel. This is less verbose, but again you are programming the Travis CI runtime using YAML. You need to understand Travis's approach to parallelism to understand how it works.

## Understanding Required

![Understanding]({{site.images}}{{page.slug}}/understanding.png)\

Here's a question: What does this Travis CI build output?

~~~{.yaml caption="commands.yaml"}
language: minimal

jobs:
  include:
    - stage: parallel tasks
      name: "First"
      script: echo "1"
    - name: "Second"
      script: echo "2"
    - name: "Third"
      script: echo "3"

~~~

Answer: It's indeterminate because the default stage is the last used stage, and so all three tasks run in parallel. It's an implicit parallelism approach but embedded in YAML.

That's kind of neat!

But when you specify parallelism in YAML, it *doesn't* save you from understanding the semantics and the runtime execution that they influence and control. The valid syntax is a subset of YAML, but the semantics can be *anything*.

So the details that are present in this:

~~~{.bash caption="build.sh"}
#!/bin/bash

if [ -n "$(echo 'First Condition')" ]; then
    # First step goes here
    echo "Hello, World!" &
fi

if [ -n "$(echo 'Second Condition')" ]; then
      # Second step goes here &
     ls
fi

# Third thing goes here
wait
echo "Third thing:"
~~~

Are sort of obscured in

~~~{.yaml caption="sample_GHA.yaml"}
name: GitHub Actions Demo
jobs:
  one: 
    name: One
    runs-on: ubuntu-latest
    steps:
      -  run: |-
              echo "Hello, World!"
         if: '[ -n "$(echo 'First Condition')" ]'
  two: 
    name: Two
    runs-on: ubuntu-latest
    steps:
      -  run: |-
              echo "Hello, World!"
         if: '[ -n "$(echo 'Second Condition')" ]'
  three: 
    name: three
    runs-on: ubuntu-latest
   needs: [one,two]
    steps:
      -  run: |-
              echo "Third thing"
~~~

So, YAML is fine and all for config, but it's less fine when it's used as the way to write the AST for an unspecified programming language. Instead, maybe you just should use the bash script or – in the context of a larger runtime – take instructions in Lua or Python or whatever makes sense for your program.

Or if you want the constraints that configuration offers, then it's also super easy to write your own parser for the little language you've built.

Here is one way to do this for my blog build script example:

~~~{.bash caption="test1.job"}
job first PARALLEL {
   echo "Hello, World!"
} when {
   echo 'First Condition' 
}

job second PARALLEL {
   ls
} when {
   echo 'Second Condition'
}

wait

job third  {
   echo "Third thing" 
}
~~~

I wrote a Python implementation for this little job runner using a [PEG parser](https://github.com/erikrose/parsimonious) and [futures](https://docs.python.org/3/library/concurrent.futures.html) ([GitHub](https://github.com/adamgordonbell/job-runner)), and it's like 100 lines of Python, and it works. You put whatever bash code within the `job` and `when` blocks, which works as expected. I will try it for a bit and probably end up back at Bash, but it's certainly better than the YAML-embedded solution.

### Declaring Code as Data

**So does that mean that YAML is always a bad idea?** Not at all, there are reasons to dislike YAML, but that's not my point here.

YAML (or JSON or TOML) works fine when declaring something. `Name=Adam`, `ID=7`, or even `UseParallelGC=True`, but the more you need to know about what is done with those values, the less declarative your config is and the further you are drifting from configuration data to configuration code.

**In my opinion, once you have to branch or have conditionals in your config, you are coding and should put the config file down and grab a better tool.**

### How Did We Get Here?

If YAML shouldn't be used to 'declare' a program that later runs, then why is this pattern so prevalent in modern DevOps tooling? One reason is that there was a sense at some point that configuring something was less complicated than programming it. Hopefully, I've shown why that might not be true: You still need to understand the semantics of the 'code' even if you're embedding it in YAML. A second reason is that sometimes it's an excuse to save [the effort of writing a parser](https://buttondown.email/hillelwayne/archive/code-is-data-is-yaml/).

## Conclusion

![conclusion]({{site.images}}{{page.slug}}/conclusion.png)\
So here is my conclusion.

**Tool authors**: If you are trying to 'configure' the evaluation or control flow of something, use an existing programming language or write a parser. A packrat or PEG parser is not that much code. Try to avoid building ill-defined little languages whose AST is hand-written in YAML.

**And tool users**: Don't assume that because something only requires configuration, you won't need to learn a partially-defined embedded-in-config programming language. You might be better off choosing a tool like a Makefile, an Earthfile, or even Gradle than one of the 100s of things that are 'configured' in YAML (Ansible, GHA, Azure Pipelines, and so on).

{% include_html cta/bottom-cta.html %}
