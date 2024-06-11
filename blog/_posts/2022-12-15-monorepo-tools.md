---
title: "Monorepo Build Tools"
categories:
  - build
author: Adam
sidebar:
  nav: monorepos
internal-links:
 - monorepo tools
 - monorepo
topic: monorepo
funnel: 2
excerpt: |
    Learn about the different monorepo build tools available, including Bazel, Pants, Nx, and Earthly. Discover their features, programming language support, learning curves, remote caching and execution capabilities, build introspection abilities, and versatility. Find the right tool for your organization's monorepo needs.
last_modified_at: 2023-07-14
---
**The article examines monorepo build tools, highlighting Pants for Python. Earthly supports multiple languages, potentially simplifying your build process. [Check it out](https://cloud.earthly.dev/login).**

<!-- markdownlint-disable-file MD001 -->
<!-- markdownlint-disable MD045 -->
<!-- vale HouseStyle.OxfordComma = NO -->

In the software development world, there is a growing trend of using monorepos to manage codebases. A monorepo is a single repository that contains the code of many interrelated but distinct projects. While monorepos have their benefits, they also come with their own set of challenges. And guess what? The challenges are primarily around tooling. In this article, I'll compare some of the most popular monorepo build tools on the market and see how they stack up against each other.

## What Are the Problems Presented by Monorepos?

Here is the situation. Building things is relatively simple if you have one build artifact per source repository: you have a build process, you rebuild when code changes, and you get a new artifact. Of course, this codebase can grow, and perhaps as it grows, caching steps will need to be introduced, but generally, every change will lead to one new build artifact.

Things get more complex when code repositories contain multiple partially-independent pieces of software. For example, if a repo has tens or hundreds of services, many services likely depend on each other. Still, changes to one do not necessarily mean all others need to be retested, rebuilt, or redeployed. This is why monorepos build tools, to do a good job, need to track project dependencies.

## Not Just for Monorepos

The opposite of a monorepo is a collection of source code repositories, where each build artifact has its own repository. But this distinction can be a bit meaningless. Many monorepo shops have multiple monorepos, and many places with a polyrepo structure have repositories that produce multiple artifacts. So the code organization solution space is a gradient from maximally conjoined to maximally separated. However, large repos have pushed legacy build tools to a breaking point, and new tools and techniques are now needed. All the tools I'm covering today tightly track dependencies and aggressively cache build steps, but these tools shouldn't just be limited to just maximally homogeneous source code layouts. Caching and tracking dependencies benefits lots of build use cases.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5040.png --alt {{ Monorepo Build Tool Features }} %}

## Features

When choosing a monorepo build tool, there are a few different features that you should keep in mind. These include:

- **Programming Language Support**: Make sure that the build tool you choose supports the programming languages you want to use now and in the future. Some build tools only support specific languages and that is fine as long as your monorepo will only ever have those languages in it.
- **Learning Curve**: The learning difficulty of each tool varies. Some of them require a deep understanding of the underlying technologies and processes, making it difficult to get up and running quickly. Others are more user-friendly, with intuitive interfaces that allow users to quickly understand how to use the tool. Each tool's complexity should be considered when deciding which one best suits your needs.
- **Caching**: An ideal build tool should never run the same build twice. To be more specific, with local caching, a machine should never run the same build step with the same inputs a second time, and with a remote cache, this should be true across an organization or build cluster. Make sure that the build tool you choose has a good caching solution.
- **Remote Execution:** Remote execution can improve build times by allowing you to build the codebase on a remote server. And distributed execution is a further improvement where the build scheduler can distribute build steps across more than one machine. Make sure that the build tool you choose supports remote execution.
- **Build Introspection**: Build introspection refers to the ability of a build tool to provide insight into the processes and dependencies involved in building software. This allows engineers to view and query the build graph and ask questions like what part of the build is slowest or what projects depend upon this change.
- **Versatility**: Build scripts are often used for things besides just purely producing artifacts. Most large organizations have at least one build pipeline with requirements that fall outside of the standard build and test stages. How are dependencies installed? How are integration tests run? Is there a staging database to restore or a production deploy to trigger? Make sure you consider how you will solve problems beyond producing an artifact from some source code.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5120.png --alt {{ The Monorepo Tools }} %}

## Monorepo Tools To Compare

Many build tools can be used with monorepos, but I can't cover them all[^1]. Instead, I'll focus on these four:

- **Bazel**: Bazel is a monorepo build tool from Google. It is designed to be fast and scalable, with support for multiple programming languages. Bazel ( and Google internal version Blaze ) have inspired many of the build tools covered here. Bazel has a steep learning curve, but it's a powerful tool.
- **Pants**: Pants is another monorepo build tool. It's popular with large organizations whose development workflow varies in ways that make Bazel a struggle. Pants uses code introspection to reduce the level of effort involved in its adoption.
- **NX**: NX is a monorepo build tool from NRWL. Targeted initially at building monorepos of Angular applications in a safe and performant way, NX has expanded with plugins to cover not just Angular, and not just JavaScript, but also backend languages like Go and Rust.
- **Earthly**: Earthly is a popular open-source build tool for monorepos. Earthly uses BuildKit to perform builds in isolated sandboxed environments, and its Dockerfile-like syntax means it's a small lift to move from a language's native build tools to building with Earthly.

   ( I also work for Earthly and am a big believer in it, but I try to be impartial about when it's a good fit and when it's not. )

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/0890.png --alt {{ Bazel Build Tool }} %}

## Bazel

#### Programming Language Support

Bazel natively supports C++, Python, Java, and popular plugins and extends support to many other languages, such as JavaScript, Go, Rust, Scala, and Kotlin. With Bazel, each language's adoption of Bazel can go a bit differently, and our previous Bazel article has case studies on language-specific adoption.

#### Learning Curve

Bazel's learning curve is known to be a challenging one. Bazel is prescriptive about structuring code, and to migrate to Bazel you will need to write a BUILD file for each Bazel package. Bazel's Google roots, and its current use primarily among hyperscaling large tech companies, means it works best where an experienced build engineering or platform team can dedicate significant time to a Bazel migration.

#### Caching

The original goal of Bazel was to speed up large builds, and this is accomplished by only building what is absolutely necessary and ruthlessly caching everything else. Because of this, Bazel supports very granular caching at the software package level. Remote caching is also supported via a Google Cloud bucket.

#### Remote Execution

Bazel can execute builds and tests on your local machine or across multiple machines using remote execution. Remote execution is not quite a native feature of Bazel, but it's supported through open-source extensions like Buildbarn. Commercial services are also available with remote execution services.

#### Build Introspection

Bazel has extensive build introspection abilities. `bazel query` provides information about the dependency graph with a small query language for structuring results. `bazel cquery` and `bazel aquery` extend this with additional information such as artifacts produced and commands run.

#### Versatility

Bazel has three verbs: build, test, and run. Build and test must be pure steps without side effects on the outside world, in order for Bazel's caching to be effective. The run verb is never cached and so may have side effects. Therefore, integration tests, or anything that touches the outside world, must be done in Bazel using the run step or must be done outside of Bazel entirely. Bazel considers anything else outside of the scope of a build tool. This can be a limitation, especially if steps that interact with the outside world need to happen before ( like environment setup ) or along with specific build steps. This means that Bazel is often wrapped by another tool (Bash or CI scripts).

Build environment setup (which GCC version is installed and so on) is also considered out of scope by Bazel.

### Overall

Bazel is an excellent choice if you have several million lines of code in multiple languages that have dependencies between them. Adoption will be challenging, but at that code size, you can likely dedicate an experienced team to the migration efforts at that size. If your CI process needs to do things outside of building and testing sources, you likely need to wrap Bazel in another tool. You can find several [Bazel adoption case studies](/blog/bazel-build/#bazel-case-studies) in [my previous Bazel article](/blog/bazel-build/).

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1000.png --alt {{ Pants Build Tool }} %}

## Pants

#### Programming Language Support

Pants is a build tool that supports multiple languages, including Go, Python, Shell, Java, and Scala. It currently does not support Javascript or Rust, but there may be plans to add support. Pants is written in Python, and its rich support of Python is a differentiator from Bazel, where Python support has sometimes been criticized as partially abandoned.

#### Learning Curve

Pants v1 was created at Twitter as an in-house implementation of Blaze, the build tool that would be open-sourced as Bazel. Pants v2 is an implementation of Pants specifically targeted at alleviating many of the challenges of adopting Bazel or Pants v1. Specifically, Pants relies on static analysis of code to establish dependencies between modules, and in this way, it removes some of the pains of monorepo tool adoption.

#### Caching

Pants, being born at Twitter and then spreading to Foursquare and other large tech companies, also strongly focuses on speeding the builds of very large monorepos via fine-grained caching. Remote caching is available as a commercial solution and as an open-source offering.

#### Remote Execution

Remote execution support in Pants is experimental and limited to Linux builds.

#### Build Introspection

Pants has a command called 'pants dependencies` that returns for any file the project dependencies and third-party dependencies. This can also be done at the target level, and the dependees query shows the reverse results, which depends upon this file. Because of the static analysis of Pants 2.0 this can all be done, in the supported languages, without writing boilerplate package definitions in BUILD files.

#### Versatility

Much like Bazel, pants limits its scope to the build and test steps of working with a mono repo. Build-environment setup, ad hoc general build automation, and integration tests that are stateful or depend upon the outside world would be considered out of scope for pants.

### Overall

Pants is a first-class alternative to Bazel if the migration efforts behind writing BUILD files for each package are too costly or if the workflows and concepts imposed by Bazel are an awkward fit for your organization. The current niche Pants is seeing the most adoption in is large Python monorepos. Its lack of support for languages like JavaScript and Rust may limit its adoption in other niches for now.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1240.png --alt {{ NX Build Tool }} %}

## Nx

#### Programming Language Support

Nx's original focus was on Angular, but it has expanded support for other frameworks such as React, Vite, and backends written using various frameworks in Javascript, and Typescript. iOS and Android Executors are also available, and plugins for languages like Go and Rust also exist. Unfortunately, Java and C++ appear not to be supported.

Nx has made several efforts to use Bazel internally as an NX backend. And although they no longer recommend this approach, it would allow for using NX for Angular projects and Bazel for backend services.

#### Learning Curve

By focusing primarily on JavaScript and TypeScript monorepos, NX can offer a tool that feels natural to frontend developers in a way that Bazel and Pants may not.

#### Caching

NX has fine-grained caching of dependencies. Remote caching can be achieved via Nx Cloud, a commercial offering with a free tier.

#### Remote Execution

NX supports Distributed Task Execution via the NX Cloud, a commercial offering with a free tier.

#### Build Introspection

NX has an `nx graph` command that returns graph of project dependencies as an html webpage. Additionally, the `nx affected` has some ability to return data about the effects of a change. It may be possible to add other introspection capabilities using NX plugins but generally, build introspection capabilities are more limited than Bazel.

#### Versatility

NX builds are built up of tasks. Whether the items should be cached or always rerun is controlled via a `cacheableOperation` option. This, combined with its ability to execute npm scripts, makes it more versatile at handling ad-hoc build tasks than pants or Bazel. That said it is not intended as a general purpose build automation tool.

### Overall

NX is a great choice for frontend monorepos, and large Javascript or Typescript monorepos in general. NX cloud's remote execution and caching capabilities look promising for those uses cases.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1350.png --alt {{ Earthly Build Tool }} %}

## Earthly

#### Programming Language Support

Earthly's approach to programming language support (and monorepo builds in general, is a bit different. Described by its users as "Docker for builds," Earthly uses runc containers for build isolation, meaning that you can use your existing programming language tool inside an Earthly build. This includes standard languages such as Javascript, Python, Java, C++, Go, and Rust, but also any build tool that can be run on Linux can be run in Earthly.

This containerized approach also means Earthly can handle builds that depend on system-level dependencies like libc as well as efficiently producing containers as part of the build process. A downside of this approach is that, at present, Earthly builds can only target Linux environments. Therefore, it's not a good choice for those building iOS apps or Windows binaries.

#### Caching

Caching in Earthly is layer based and similar to caching found in container images. The granularity of caching is determined by the inputs to the specific build step. This means, by default, the caching is less granular than found in Bazel but often works very well by simply bringing your existing programming language tools into an Earthfile.

Mount-based caching and a CACHE keyword, along with inline and explicit caching, mean that the cache hit rate can be further improved from there.

Additionally, two types of Remote caching are supported and can be backed by a Docker Registry.

#### Learning Curve

Earthly's syntax is inspired by the Dockerfile format, where each build step is a series of RUN commands. Because of this, writing your Earthfile involves using the same tools you'd use to build outside of an Earthly. The way you build something using Earthly is the way you'd build it on Linux. This means writing an Earthfile has a shallow barrier to entry.

#### Remote Execution

Earthly supports two methods of remote execution. One uses remote BuildKit workers you set yourself up, and the other uses commercially hosted Earthly Satellites.

Remote execution with ample remote local cache is a unique solution to build times Earthly Satellites uses to save cache network round trips and speed builds.

#### Build Introspection

Earthly's introspection abilities are limited. Earthly can list targets in the current Earthfile and provide some information about build performance, but not in a machine-readable format. It cannot provide information about the dependencies or dependees of a file or build target.

#### Versatility

Earthly elevates versatility as a core value, bringing the reproducibility, dependency tracking, and caching from tools like Bazel not just to build and test steps but to everything that would traditionally be done in a bash script, Makefile or ./configure script.

### Overall

Earthly is a tool that is well-suited for multi-language monorepos, especially for teams that are familiar with Dockerfiles and containerization. It is especially helpful for teams with builds that require additional setup or are more complex in nature. Teams building cloud microservice backends may find Earthly a good fit.

Earthly is the only tool in this list that does not replace your previous language-specific build tool but instead wraps it. This has pros and cons. As a pro, it is easy to adopt Earthly as it acts more like a glue layer rather than a rewrite of the build scripts. As a con, being a glue layer, it is often less fine-grained at caching, which can affect its performance.

## Overview

<style>
      .prose table,
      .prose td {
        vertical-align: middle !important;
      }
    </style>

Another way to compare these tools is look at each feature one by one.

### Programming Language Support

It's important to choose the tool that can support the programming languages you have in your monorepo.

| Tool |          |    Programming Language Support |
| ----- | ----------- | --------------------------------------------- |
| <img src="{{site.images}}{{page.slug}}/4.png" width="50" height="50" /> | Bazel             |Java, C++, Python and more.|
| <img src="{{site.images}}{{page.slug}}/3.png" width="50" height="50" /> | Pants             |Go, Python, Java and more (no JavaScript)
| <img src="{{site.images}}{{page.slug}}/5.png" width="50" height="50" /> | Nx             |Javascript, Go, Rust. Also iOS and Android executors.
| <img src="{{site.images}}{{page.slug}}/6.png" width="50" height="50" /> | Earthly             |Anything that runs on Linux. |

### Learning Curve

Adopting a monorepo build tool has a cost. That cost varies based on the learning curve and ease of adoption.

| Tool |          |    Learning Curve |
| ----- | ----------- | --------------------------------------------- |
| <img src="{{site.images}}{{page.slug}}/4.png" width="50" height="50" /> | Bazel             |Challenging to adopt.|
| <img src="{{site.images}}{{page.slug}}/3.png" width="50" height="50" /> | Pants             |Uses static introspection to improve on the usability of Bazel.|
| <img src="{{site.images}}{{page.slug}}/5.png" width="50" height="50" /> | Nx             |Small learning curve for JavaScript Developers.|
| <img src="{{site.images}}{{page.slug}}/6.png" width="50" height="50" /> | Earthly             |Build software same way you would on Linux, but inside Earthly. |

### Remote Caching and Execution

Remote caching and execution is important for scaling builds.

| Tool |          |    Remote Caching and Execution |
| ----- | ----------- | --------------------------------------------- |
| <img src="{{site.images}}{{page.slug}}/4.png" width="50" height="50" /> | Bazel |Remote caching and distributed execution available open-source or commercially.|
| <img src="{{site.images}}{{page.slug}}/3.png" width="50" height="50" /> | Pants |Remote caching and distributed execution available open-source or commercially.|
| <img src="{{site.images}}{{page.slug}}/5.png" width="50" height="50" /> | Nx    |Remote caching and remote execution available commercially.|
| <img src="{{site.images}}{{page.slug}}/6.png" width="50" height="50" /> | Earthly|Remote caching and remote execution available open-source or commercially. Open source via self-host BuildKit runners and commercially via Earthly Satellites. |

### Build Introspection

Build introspection refers to the ability of a build tool to provide insight into the processes and dependencies involved in building software.

| Tool |          |    Build Introspection |
| ----- | ----------- | --------------------------------------------- |
| <img src="{{site.images}}{{page.slug}}/4.png" width="50" height="50" /> | Bazel |`bazel query` and related commands offer great introspection support.|
| <img src="{{site.images}}{{page.slug}}/3.png" width="50" height="50" /> | Pants |`pants dependencies` command offers good introspection.|
| <img src="{{site.images}}{{page.slug}}/5.png" width="50" height="50" /> | Nx    |Nx affected offers some introspection capabilities.|
| <img src="{{site.images}}{{page.slug}}/6.png" width="50" height="50" /> | Earthly|Earthly has limited introspection capabilities.|

### Versatility

Most large organizations have at least one build pipeline with requirements that fall outside of the standard build and test stages. Some tools consider this out of scope while others offer support for tackling the automation work at the heart of building software.

| Tool |          |    Build Introspection |
| ----- | ----------- | --------------------------------------------- |
| <img src="{{site.images}}{{page.slug}}/4.png" width="50" height="50" /> | Bazel |Limited support. `run` stage can be used for integration testing. Environment setup and build automation mainly considered out of scope.|
| <img src="{{site.images}}{{page.slug}}/3.png" width="50" height="50" /> | Pants |Limited support. Environment setup and build automation mainly considered out of scope.|
| <img src="{{site.images}}{{page.slug}}/5.png" width="50" height="50" /> | Nx    |Support for non-cacheable steps and ad-hoc build tasks via npm scripts.|
| <img src="{{site.images}}{{page.slug}}/6.png" width="50" height="50" /> | Earthly|Aims to encompass all environment setup and build automation by wrapping existing tools.|

## Conclusion

If your organization is Google-like – in terms of language use, workflow, and code base size – then Bazel is probably a good fit. If you find the cost of migrating to Bazel prohibitive or if you are frustrated by Bazel's Python support and BUILD boilerplate, then Pants is worth investigating.

If your monorepo is a frontend web dev monorepo, mainly full of JavaScript and Typescript, then Bazel is often a significant change, and Pants isn't ready for you. For those reasons and because of its popularity among front-end devs, NX is a great choice.

If you are working with containerized microservices, or if your software has system-level dependencies, or if you'd like to use your language's existing build tools or need to do something a bit non-standard, then [Earthly](https://cloud.earthly.dev/login), with its containerized glue layer approach, can be a great choice to build in an efficient and reproducible way.

(Also, you can combine many of these tools together. Earlier I mentioned NX backed by Bazel, but Bazel inside of Earthly and Pants inside of Earthly has also been done. The only real way to find out what tool will work best for your specific use case is to give it a try with a small proof of concept.)

{% include_html cta/bottom-cta.html %}

[^1]:
   There are so many tools that can help build a monorepo. There are other Bazel-inspired tools like Amazon's Brazil and Facebook's Buck and Buck2. There are JS-only build tools like Lerna, Rush, Turborepo, Lage. There are traditional build tools like Gradle, CMake, ninja, and shake. And even package management languages like Nix, when you throw in its build system Hydra, could be considered for building a monorepo. So, I've only picked a few representative builds. If there are others you'd like to see covered, please let me know.
