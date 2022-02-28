---
title: "Building a Monorepo in Golang"
categories:
- Tutorials
  toc: true
  author: Brandon

internal-links:
- just an example
---

A monorepo is a single repository that contains multiple projects, whereas a polyrepo splits projects into separate 
repositories.

In Go, a monorepo may contain multiple "modules" (i.e. multiple `go.mod` files). Each module may be defined in a 
separate directory, and each with their own separate dependencies.

While this may sound simple on paper, there are actually a few tricks required to get a monorepo working smoothly in 
Go.

In this article, I'll demonstrate some strategies I've learned over the years to get a multi-module monorepo working 
in Go, where each module independently (and efficiently!) manages its own build, test, and release cycles.

## Why Build in a Monorepo?

Whether to build your Go projects in a monorepo or polyrepo may depend on your organization and personal preferences. 

I find a monorepo especially appealing when working with a small team, where a few developers collectively maintain 
multiple software projects. In large organization, however, where many teams independently maintain their own projects, 
I might argue that a polyrepo setup could be more comfortable and empower teams to work more autonomously.  
This isn't always the case, however, as large organizations like Google, Facebook and Twitter 
[have been known](https://en.wikipedia.org/wiki/Monorepo) to employ very large monorepos successfully.

[Love them](https://medium.com/@adamhjk/monorepo-please-do-3657e08a4b70) 
or [hate them](https://medium.com/@mattklein123/monorepos-please-dont-e9a279be011b),
there are can be some benefits to using a monorepo to develop your projects. 

Based on my own experiences, some pros and cons you may want to consider with using a monorepo are: 

*Pros:*
* Much easier to make changes across multiple projects at once in a monorepo
* Code reviews are in one place, and the scope of code the team owns is easy to comprehend
* Easy to share knowledge, code (e.g. libraries), and keep a consistent style across projects  

*Cons:*
* Build tooling can be more complicated in a monorepo
* It can be easy to accidentally tightly-couple components that should be decoupled
* Components may be less autonomous, and developers may have less freedom to do things "their own way"
 
## Monorepo Layout in Go

So you have decided that 

## Importing Local Go Modules in a Monorepo

## Build Tooling for a Monorepo in Go
