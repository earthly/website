---
title: 'Introducing Earthly: build automation for the container era'
featured: true
author: Vlad
categories:
  - news
toc: false
internal-links:
   - build automation
topic: earthly
funnel: 3
topcta: false
excerpt: |
    Introducing Earthly, a build automation tool for the container era. Learn how Earthly brings modern capabilities like reproducibility, determinism, and parallelization to your builds without the need for a complete rewrite.
last_modified_at: 2023-07-11
---

We live in an era of continuous delivery, containers, automation, rich set of programming languages, varying code structures (mono/poly-repos) and open-source. And yet, our most popular CI/CD platform was started 15 years ago when the industry looked very different. CI systems have not changed much since — they are still largely glorified bash scripts, and the limitations are starting to show their age. For context, Docker's first release was 7 years ago and Kubernetes is only 5 years old. There is no way Jenkins ("Hudson" back then) could have been built with containers in mind, as Docker didn't even exist at the time.

{% include imgf src="adoption.png" alt="graph of CI usage" caption="Source [Lawrence Hecht](https://medium.com/u/d3b222569e15?source=post_page-----55619c63c3e----------------------), Source [CNCF 2019 Survey](https://www.cncf.io/wp-content/uploads/2020/03/CNCF_Survey_Report.pdf)" %}

During this time, tech giants have innovated in parallel and have open-sourced tools like [Bazel](https://bazel.build/) and [Pants](https://www.pantsbuild.org/). They bring modern features, like reproducibility, determinism, the ability to scale in a monorepo and the ability to use cloud-based cache and parallelization.

Although these systems are probably some of the most advanced build automation tools the world has seen, they come at a significant cost: the build config is not compatible with any of the popular open-source tooling that the language communities have gotten so used to. It's like they come from a parallel universe. For most teams, adopting these tools means completely rewriting all the build configs from scratch and giving up on an entire ecosystem of tooling that they have become so dependent on. As advanced as they are, these solutions have not seen significant adoption beyond tech giants.

## Introducing Earthly

![Earthly Logo]({{site.images}}{{page.slug}}/logo.png)\

With the purpose of bringing these modern capabilities to people out in the real world, today we are announcing the release of [Earthly: a build automation tool for the container era](https://cloud.earthly.dev/login).

**Earthly is not meant to replace your existing open-source tooling, but rather to leverage and augment it**. It does not replace your Gradle, your Maven, your npm, your webpack — you don't need to rewrite your build. Instead, it leverages these popular technologies and builds on top of them, acting more like the glue.

**Earthly runs all build targets containerized: they get container isolation and layer caching**. Nothing is shared between build targets, other than clearly defined, immutable build artifacts and Docker images.

**No sharing means that you get parallelization for free**. You don't need to do anything to get it and you never have to debug race conditions. It just works.

**But most importantly, all builds are completely reproducible**. You get a guarantee that the build succeeds on its own and not because of your local dependencies or some environmental config that you're not aware of. Thus, it becomes an order of magnitude easier to iterate on and debug broken CI builds.

![Screenshot of commits for a failing build]({{site.images}}{{page.slug}}/commits.png)\

**A familiar Dockerfile-like syntax is used** , to help new users get up-to-speed quickly. It's like Dockerfile and Makefile had a baby. However, in contrast to Dockerfiles, you can also output regular artifacts (jars, packages, binaries, arbitrary files), in addition to Docker images.

~~~{.dockerfile caption=""}
FROM golang:1.13-alpine3.11
WORKDIR /go-example

build:
  COPY main.go .
  RUN go build -o build/go-example main.go
  SAVE ARTIFACT build/go-example AS LOCAL build/go-example

docker:
  COPY +build/go-example .
  ENTRYPOINT ["/go-example/go-example"]
  SAVE IMAGE go-example:latest
~~~

Earthly in the future will be about much more: for example, cloud-based build parallelization that has never been possible before. For now, you can run it on top of your existing CI, and you can run it locally for development. You still get the other benefits mentioned above.

There are many other goodies that Earthly provides. For more information and also installation instructions, visit [Earthly's sign up](https://cloud.earthly.dev/login/).

This is the first release of Earthly. We will continue to iterate, make improvements and, most importantly, incorporate user feedback. We can't wait to see what you build with it!

{% include_html cta/bottom-cta.html %}

<script id="asciicast-314104" src="https://asciinema.org/a/314104.js" async></script>
