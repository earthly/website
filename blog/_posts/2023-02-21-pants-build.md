---
title: "Creating Pants"
categories:
  - Tutorials
toc: true
author: Adam
internal-links:
 - pants
 - pants build
---

## Intro
Pants, the build system has a complex and interesting history. It all started when Benjy worked at various C++ places. Back then builds were just slow.

> and there was just a perception that this was almost part of the mystique of software engineering. Like things are supposed to be hard and slow and flaky and broken and require huge amounts of memory. And that's just how it is. And you accept that and you don't really think anything of it. 

Compiling then was something that you did and then went and grabbed a coffee. But then Benjy moved to Google.

## Off-The-Rack: MakeFiles at Google

Google at that time, in the early 2000s, had a lot of C++ code in a large perforce repository. And you would compile locally by running the large makefile that built the entire solution. 

> You start, you'd fire it up and it would pass the make file, and then it would have to stat many, many, many thousands of files on your, at the time spinning disc. And so, it, it was just very, very slow to even start up, to get to the point where it could figure out what work needed, what compilation work needed to be done, let alone doing that compilation work or running tests or whatever.

Google handled this differently though.

> The attitude was not, this is the fact that this is slow and broken and hard and messy is part of the mystique. The attitude there was no, we should fix. This should be fast and easy and fun. And software engineering is a discipline, and we have it within our power to improve our own discipline. We can come up with good practices and we can build tools that not just support those practices, but enforce them.

Sometimes as software engineers we are too busy, or forget, that we have the power to build our own tools.

> Oh, actually, unlike I think pretty much all other professionals that don't have it within their power to create their own tools – if you work in sales and you want better sales tools, you have to find a software engineer to do it for you – but we are software engineers and the tools that we use are themselves made outta software. So we have it in our power to fix them.

Other large tech organizations solve this problem with a polyrepo setup. If each product or service or library lives in its own repository then builds may be faster ( though other problems can come up.) For google splitting, that solution was worst than the problem and so ways to build faster had to be found.

### Hemming Make

The first step in speeding things was constraining the problem. If getting the status of everyfile in the monorepo so that make knows what to do is the bottleneck then perhaps for each directory or file you could explicilty list out the full transitive dependencies of it.

> Every time you want to do some operation. We should only be looking at the relevant parts. And so instead of statting, you know, 50,000 files, maybe you only have to stat 500.

In fact, if you knew the full set up files you needed, perhaps you could just check out those.

> Perforce unlike git allows you to check out only parts of the code base [you need]. So it's a very, very different model than what maybe many people are familiar with with Git.

And then if then dependencies you weren't changing could be references a different way.

> They had they developed something called SourceFS. It was just essentially a file system overlay that let you see reference any version of any source file as a file. And eventually, ObjectFS, which allowed you access to the object files that were stored on some network file system.

## Tailored for Google: Blaze

These improvements to the build system sped things up.

> I very much remember it getting a lot better very quickly every time some new thing was launched.

But they were fighting a growing google, where everyday people were adding new code and also the company was growing.

> All those gains were the added drag of just more and more and more code, and more complexity and more dependencies.

So this system, internally called Blaze, kept improving and kept growing. And then Benjy left for Twitter.

## Bespoke for Twitter: Pants V0

At twitter, Scala and a polyrepo approach to code was the common pattern. They had around 200 engineers but many more code repositories than people.

> But many, many more repos than there were engineers on the team. 
> Every little library, every little project was its own repo. And there was just a lot of difficulty in sharing code.







## Tailoring Builds for FourSquare: Pants V1

## ToolChain - Behind the Seams

## Custom-tailored for Python: Pants V2

## The Future is Ready-to-Wear




### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

## Outside Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
