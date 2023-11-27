---
title: "To Understand Pants, Understand Bazel's History"
categories:
  - Tutorials
toc: true
sidebar:
  nav: "bazel"
author: Adam
internal-links:
 - pants
 - pants build
excerpt: |
    This article explores the history of the build system Pants, from its early days at Google to its current version, Pants V2. It delves into the challenges faced by large tech organizations in managing builds and how Pants provides solutions for Python monorepos. If you're interested in understanding the background and development of build systems, this article is a must-read.
last_modified_at: 2023-07-11
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article discusses some of the benefits of using a Monorepo. Earthly is particularly useful if you're working with a Monorepo. [Check us out](/).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/mEx8NWm4830" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

[Pants](https://www.pantsbuild.org/), the build system has a complex and multifaceted history. I reached out to Benjy Weinberger to get the whole story.

_The full interview is embedded above, but here is an article summarizing the talk for those in a rush:_

## Intro

Without C++ there would be no Pants. Because in Benjy's first couple jobs as a software developer, they worked in C++, and builds were slow.

{% include quotes/bazel/quote.html %}
and there was just a perception that this was almost part of the mystique of software engineering. Like things are supposed to be hard and slow and flaky and broken and require huge amounts of memory. And that's just how it is. And you accept that and you don't really think anything of it.
{% include quotes/end.html %}

Compiling then was something that you did, and then you went and grabbed a coffee. But then Benjy moved to Google.

<!-- vale HouseStyle.H2 = NO -->
## Off-the-Rack: Makefiles At Google

Google at that time, in the early 2000s, had a lot of C++ code in a large perforce repository. And you would compile locally by running the large makefile that built the entire solution.

{% include quotes/bazel/quote.html %}
You start, you'd fire it up and it would pass the make file, and then it would have to stat many, many, many thousands of files on your, at the time spinning disc. And so, it, it was just very, very slow to even start up, to get to the point where it could figure out what work needed, what compilation work needed to be done, let alone doing that compilation work or running tests or whatever.
{% include quotes/end.html %}

Google handled this differently, though.

{% include quotes/bazel/quote_blank.html %}
The attitude was not, this is the fact that this is slow and broken and hard and messy is part of the mystique. The attitude there was no, we should fix. This should be fast and easy and fun. And software engineering is a discipline, and we have it within our power to improve our own discipline. We can come up with good practices and we can build tools that not just support those practices, but enforce them.
{% include quotes/end.html %}

Sometimes – as software engineers – we are too busy and forget about the power we have.

{% include quotes/bazel/quote_blank.html %}
Unlike I think pretty much all other professionals that don't have it within their power to create their own tools – if you work in sales and you want better sales tools, you have to find a software engineer to do it for you – but we are software engineers and the tools that we use are themselves made out of software. So we have it in our power to fix them.
{% include quotes/end.html %}

Other large tech organizations solve this problem with a polyrepo setup. If each product, service, or library lives in its own repository then builds may be faster ( though other problems can arise.) For Google, splitting that solution was worse than the problem, and so ways to build faster were needed.

### Hemming Make

The first step in speeding things up was constraining the problem.

{% include quotes/bazel/quote.html %}
Every time you want to do some operation. We should only be looking at the relevant parts. And so instead of statting, you know, 50,000 files, maybe you only have to stat 500.
{% include quotes/end.html %}

To do that, you could explicitly list the full transitive dependencies of each submodule. Then, if you knew the complete set of files you needed for working in an area, perhaps you could just check out those.

{% include quotes/bazel/quote_blank.html %}
Perforce – unlike git – allows you to check out only parts of the code base [you need]. So it's a very, very different model than what maybe many people are familiar with, with Git.
{% include quotes/end.html %}

And then, what if the dependencies you weren't changing could be referenced differently?

{% include quotes/bazel/quote_blank.html %}
They had developed something called SourceFS. It was just essentially a file system overlay that let you see references to any version of any source file as a file. And eventually, ObjectFS, which allowed you access to the object files that were stored on some network file system.
{% include quotes/end.html %}

## Tailored for Google: Blaze

These improvements to the build system sped things up.

{% include quotes/bazel/quote.html %}
I very much remember it getting a lot better very quickly every time some new [build] thing was launched.
{% include quotes/end.html %}

But they were fighting against a growing Google.

{% include quotes/bazel/quote_blank.html %}
Against all those gains were the added drag of just more and more and more code, and more complexity and more dependencies.
{% include quotes/end.html %}

So this system, internally called Blaze, kept improving and kept growing. And then Benjy left for Twitter.

## Bespoke for Twitter: Pants V0

At Twitter, Scala – and a polyrepo approach to code – was the common pattern.

{% include quotes/bazel/quote.html %}
[There were] many, many more repos than there were engineers on the team.

Every little library, every little project was its own repo. And there was just a lot of difficulty in sharing code.
{% include quotes/end.html %}

Benjy wasn't the only former Google person at Twitter.

{% include quotes/bazel/quote_blank.html %}
So at Twitter, I met John Sirois, who is now my co-founder at Toolchain, and he had the same observation I did about, wow, there's a lot of repos here and the tooling is haphazard and there isn't any uniform way of building anything at all.

And he had already started hacking on that problem using Python to generate ant XML files for Ant. And so that's where the name pants came from. It was a sort of contraction of Python ANTs because he was using Python to generate ANT builds.
{% include quotes/end.html %}

Pants v0 – as this ANT version has come to be known – had some limitations, so Benjy started requesting features, and soon enough, he was contributing to Pants himself.

## Tailoring Builds for FourSquare: Pants V1

Pants was a success, and then eventually, Benjy moved on from Twitter.

{% include quotes/bazel/quote.html %}
[I] went to work at Foursquare, I quickly noticed that Foursquare had the exact same problem.

They had this big Scala code base and it wasn't scaling. The solution at the time – and I am not joking – was to give all of the engineers a stick of ram, a screwdriver, and to say just upgrade your laptops.

And you can do that for a while. Right? But you can't do it forever. And that's when I realized I think I have a solution here.
{% include quotes/end.html %}

One possible solution would be to talk to Google about open-sourcing Blaze. But that had its issues.

{% include quotes/bazel/quote_blank.html %}
It was designed for Google – for a giant C++ code base that had more or less the shape of Google's. You can use it for other things, but it's hard to do. It's hard to adopt. And we didn't feel like that was even possible. The idea that we could get Google to open source it did not seem very likely at the time.
{% include quotes/end.html %}

So Benjy contacted Twitter and asked them to open-source Pants. Both companies had big Scala code-bases, and with a shared solution they could help each other out.

{% include quotes/bazel/quote_blank.html %}
There were only a handful of Scala using companies [in that] early 2010s vintage. That was back when it seemed like Scala would be the next big thing and it didn't quite go in that direction.

But that was what we now call Pants V1 to distinguish it from the current version of the system.
{% include quotes/end.html %}

## ToolChain - Behind the Seams

After leaving FourSquare, Benjy notices another dev community he is part of start to mature:

{% include quotes/bazel/quote.html %}
While everyone was looking at Scala waiting to see if it would take off, Python actually took off.
{% include quotes/end.html %}

Pants v0 and V1 were written in Python, but the build tooling for the build tool itself was lacking.

{% include quotes/bazel/quote_blank.html %}
I love working in Python. Just the Python ecosystem did not have any tooling that was really designed for big, scalable repos. Everything was sort of implicitly and sometimes explicitly assumes that your Python code base is small and produces one thing. I want a monorepo and I want to be able to have tooling to be really effective in that space.
{% include quotes/end.html %}

## Custom-Tailored for Python: Pants V2

So Benjy and John Sirois start trying to take a crack at this problem of Python Monorepos.

{% include quotes/bazel/quote.html %}
We've essentially, in 2018 to 2020, rebuilt pretty much [all of Pants] from scratch and named it Pants V2, because we're pretty bad at naming things.
{% include quotes/end.html %}

So Pants originally was written in Python, but the rewrite used Rust.

{% include quotes/bazel/quote_blank.html %}
And that P in Pants now has come full circle, except now it's not that the implementation is Python. It's that the language we're targeting is Python.

Although I should mention we do now support Java, Scala, Kotlin, Go, and several more languages in the pipeline.
{% include quotes/end.html %}

So, as Python has moved from a scripting tool to something that powers ML pipelines, microservices, and whole companies' code bases, Pants is positioning itself as the tool to help make this transition easier.

{% include quotes/bazel/quote_blank.html %}
And so rather than rely on handwriting those laborious build files Pants relies a lot on static analysis of your files. So we essentially learn the fine grain structure and dependencies of your code base. And that allows us to do things like handle cycles and all the sort of weird unpleasant, real world dependency situations [that come up].

So if you want to adopt pants, you do not need to first refactor your code base or write 10,000 lines of build files. You can just kind of set it up and run with it.
{% include quotes/end.html %}

## The Future Is Ready-To-Wear

I work on Earthly, another open-source build tool tackling similar problems. To Benjy, though, the important thing is not the potential for competition, it's the size of the problem.

{% include quotes/bazel/quote.html %}
I think an example of how much work there is to do in this space is the fact that Earthly and Pants are so different in their approaches, and yet both really fill in these needs.

There's so much open space here to fill with good technology that two systems with radically different architectures and radically different approaches can both be very useful in their own right and also complimentary.

And so it's not like, oh, this is just a little bit of a gap here and it's very obvious what the architecture is that will solve this and so someone should just build that and then we'll be done.

No, this is a big wide open field where Pants and Earthly and others are still path-finding in this space and there's room for a hell of a lot of innovation.
{% include quotes/end.html %}

That was the interview. Thank you so much Benjy Weinberger.

You can find Benjy on the Pants slack at [pantsbuild.org](https://www.pantsbuild.org/) and I'm, of course, very fond of [Earthly](/), which you can find right on this very website.

{% include_html cta/bottom-cta.html %}
