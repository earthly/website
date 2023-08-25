---
title: "Earthly CI: Launching a new era for CI"
categories:
  - News
toc: true
author: Vlad
topic: earthly
funnel: 3
excerpt: |
    
---

**Update: This is a historical announcement. The problems highlighted in this article are now solved by [Earthly Cloud](/). Earthly CI has been deprecated.**

*Hello world! We have partnered up with some [cool people in Silicon Valley](/blog/new-fundings-at-earthly/) [^1] to fix the world of software builds. So today we are launching [Earthly CI](https://earthly.dev/signup/earthly-ci), the world's first CI/CD solution that merges together a CI and a build system. A more fine-grained understanding of the build allows Earthly CI to run faster than a CI ever could before. And it's not an incremental improvement. It's a dramatic improvement. We're talking 100% to 2,000% faster. Here's how we did it.*

## But Why??

The challenges facing modern software teams are vast and varied. We live in a world of containers, diverse programming languages, diverse tech stacks, diverse code layouts, and very… very complex build scripts. Just imagine trying to explain your CI/CD stack to your mom. As our scripts have become denser and our integration tests have become more complex, our build times have spiraled out of control. It's not uncommon for CI build times to take more than 40 minutes, and if you're doing that ten times a day, you're left with very little time to actually get any work done.

And it's not just build times that are a problem. Managing your CI/CD pipelines can be a nightmare, especially as your team grows and the number of moving parts increases. It's all too common to find yourself in a situation where your builds take forever and there are no more low-hanging fruits left to improve performance. You're stuck.

This is an increasingly familiar story. The point when you lose control is the point when you have to rethink your CI/CD story from the ground-up. You need a way to make your CI pipelines faster, without throwing more humans at the problem, but rather by throwing more efficiency at the problem.

That's why today, we are announcing the general availability of Earthly CI. It's a fast, repeatable CI/CD platform that is super simple to use.

After digging deeper and swapping notes with software engineers daily for the last 3 years, here's what we believe are the stickiest CI/CD situations developers face daily.

## Problem #1: Slow Builds

A great innovation of the CI industry has been the introduction of sandboxed CI environments. They're great because a fresh new environment on every run means that you get more consistency in the way builds are executed. There's no leftover state to mess that up. They also improve security because less things are shared between runs and between pipelines.

That's extremely useful, but it comes at a very significant cost: build performance. Every CI run needs to start from a blank slate every single time. You need to download and install dependencies every time, you need to recompile everything from scratch, and you need to pull and rebuild Docker images from the ground up. That's messed up! No wonder builds take so long in this day and age.

The remote caching strategies that most CI's implement today are crude. They allow you to upload a set of directories at the end of the build, and then they allow you to download them at the beginning of the next one. But this strategy is very limited because more often than not, it ends up being slower with the cache than without it due to the upload/download times. It only works in very few circumstances, like when you're caching heavy computation, not downloaded dependencies. Otherwise, you're just swindling yourself one download for an upload and a download.

## Problem #2: Misaligned Incentives

> The slower your build, the more the vendor profits

As an industry, we have gotten used to consuming CI/CD by-the-minute. This worked fine for the previous era when CI/CD was merely a glorified bash script runner.

Nowadays, however, paying by compute time means that the slower your build, the more the vendor profits. This isn't right, because it creates a perverse incentive for the CI/CD vendor to never innovate in providing ways to speed things up. If a CI/CD tool is meant to deliver productivity gains, then correlating the value to how much less productive you are is the wrong way to go.

## Problem #3: CI/CD Pipelines Are a Nightmare to Maintain

Making the smallest changes to CI requires you to carve out hours of your day to implement them. The reason being that ***there is no way to run CI locally***. So this means that you have to test pipelines live by doing `git commit -m "try again"` over and over until you get it right. Trying out a CI/CD pipeline only in the cloud is like only ever testing apps in production. We don't do that with the rest of the software development. Why do we do it for CI/CD pipelines?

In addition, there is usually no easy way to reuse CI/CD pipeline logic. Either because the language is too difficult to use (Bash, Groovy) or because it just simply doesn't have the capability to do so (YAML).

Finally, gaining more speed in CI oftentimes means creating more parallelization by breaking up bigger pipelines into smaller ones and running them in parallel. What if the CI pipelines could be made out of smaller targets that could be automatically parallelized by the scheduler to begin with? Why does achieving parallelization mean a CI script rearchitecture every time?

These issues combined together make CI/CD pipelines a nightmare to maintain. Harder to maintain pipelines result in a worse overall CI/CD experience for the entire team, because trying to improve them is such a hassle.

## Problem #4: The CI of the past Was Not Designed for Monorepos

Currently, traditional CI/CD platforms handle monorepos by using a list of directories to watch for changes, in order to trigger pipelines. This is very limited, for multiple reasons. Firstly, not all changes to files in a sub-project should trigger a rebuild, and conversely, files outside the sub-project might change in a way that does require a rebuild. So the over-simplification that a directory is a sub-project doesn't really work in practice. Additionally, the list of directories is yet another dependency list that you have to maintain. This list is difficult to test to ensure that it is correct (partly because of all the problems mentioned before). So you could end up in situations where you thought your changes passed integration testing and were shipped to production, only to find out your integration tests never ran. Or the opposite may be true, where you're running too many tests in an abundance of caution, thus making builds impossibly slow for everybody.

No traditional CI has been designed to handle monorepos -- for good reasons: they were designed before monorepos were mainstream. And so, they have been retrofitted to work with them to the extent possible. The right approach would be for the CI to have an intimate knowledge of the dependency graph and for it to cache portions of the graph that have not changed from one run to another. No solution on the market today was able to do this.

## The Solution

Based on what we've been hearing from the industry, we thought about what the CI of the future should be.

We knew that it needed to be fast. It had to have really solid caching. Builds should not be repeated for the parts that have not changed.

We knew that the pricing model needed to be such that the vendor does not profit from ever slower builds.

We knew that it needed to be super simple to use. We knew that it had to have a strong understanding of code interdependence, such that parallelization can be fully automated. We knew that users had to be able to not only develop and update pipelines from the command-line, but also to run them, test them, iterate on them in a tight feedback loop, like we do for any other piece of software that we develop.

And finally, we knew that it had to be versatile enough for the modern demands of software development, including monorepos and polyrepos.

So we designed a new CI/CD platform from the ground-up. It's been three years in the making, and it is now seeing the light of day. We're calling it Earthly CI.

(Unfortunately, you still can't explain it to your mom though…)

## Introducing Earthly CI

Earthly CI is built on the [open-source project Earthly](https://github.com/earthly/earthly). It allows you to write CI/CD pipelines using a simple, familiar syntax, and leverages containers for isolation.

~~~{.Dockerfile caption=""}
build-pipeline:
    PIPELINE
    TRIGGER pr main
    BUILD +my-service

my-service:
    BUILD +image
    BUILD +unit-test
    BUILD +integration-test

image:
    FROM alpine:3.17
    COPY +src/my-service /bin
    ENTRYPOINT ["/bin/my-service"]
    ARG VERSION=latest
    SAVE IMAGE --push acmecorp/my-service:$VERSION

unit-test:
    FROM +src
    COPY main_test.go ./
    RUN go test ./...

integration-test:
    FROM +src
    COPY main_integration_test.go .
    COPY docker-compose.yml ./
    WITH DOCKER --compose docker-compose.yml
        RUN go test --tags=integration ./...
    END

src:
    COPY go.mod go.sum ./
    RUN go mod download
    COPY main.go ./
    RUN go build -o my-service main.go
    SAVE ARTIFACT my-service AS LOCAL my-service
~~~

Earthly allows you to execute CI/CD pipelines on your computer, thus allowing you to iterate fast when developing or maintaining them. Earthly CI was designed with the explicit goal of simplifying the dev-test cycle of CI/CD pipelines. (Our open-source users are particularly excited about this)

In Earthly CI, every step involved in the build is cached automatically, and the cache is available instantly. No upload or download necessary. The cache always makes the build faster, there's no guesswork needed, and for that reason the cache is always on for every step of every pipeline.

The syntax also allows the declaration of interdependencies. The interdependencies allow the system to build a directed acyclic graph (DAG) on the fly, and execute it with high parallelism. [^2]

In most cases this results in at least 2X speed-up compared to a traditional CI. Some teams we've been testing the technology with reported 20X improvements in extreme cases. Even the more modest improvements add up to dramatic productivity gains when taking into account the fact that developers perform builds many times every single day.

It's not just the raw time saved - that alone can pay for itself many times over. It's also the reduction in context switching. Beyond a certain threshold, longer builds mean you have to switch to doing something else in parallel to remain productive during the day. Shorter builds thus mean less context-switching, more sustained focus, more productivity, providing fast feedback while the context is still fresh in your mind.

In addition, Earthly CI's pricing includes ***zero-margin compute*** -- we make zero profit on compute. This means that if your builds are slow, we don't get rich from it. Our profit only comes from the number of active users on the platform. Plus, we only count people who perform at least three builds in a month as active users -- so if your colleague is on vacation, or if another team contributes only occasionally to your repository, we don't bill those. Conversely, if your organization uses Earthly regularly and widely, then it means it's delivering value, and that's the only situation when we actually make money. We think that this aligns our interests with those of our users better than previous models used in the industry.

And finally, Earthly CI was designed to work with any code layout. And more specifically, it was designed and tested with both monorepos and polyrepos in mind. For monorepos, Earthly understands the interdependence of build targets, and the specific source files that contribute to those targets, allowing it to cache and parallelize builds accordingly. If you're iterating on an integration test and you only change 1 out of 7 microservices, Earthly only rebuilds that 1 microservice before re-running the integration test. Similarly, Earthly has a strong understanding of setups where the build is split across many repositories. It is Git-hash-aware, and will only rebuild what has actually changed.

## Get Started With Earthly CI

Earthly CI is being made available today. As the platform is new, we are letting new users in gradually, to ensure overall platform stability.

If this is interesting to you, [get started with Earthly CI](https://earthly.dev/signup/earthly-ci)! Let's build the next generation of software together!

{% include_html cta/bottom-cta.html %}

[^1]:
    Innovation Endeavors led our [$6.5M Seed+ round](/blog/new-fundings-at-earthly/), and were joined by 468 Capital and Uncorrelated Ventures. A number of founders of companies such as Cockroach Labs, DigitalOcean, Mesosphere, DataDog, Sentry, and Instana, plus a number of creators and maintainers of notable developer platforms, such as Docker, Elixir, VS Code, GitHub Copilot, Hashicorp, Envoy proxy, Cypress, Mesos and many others, have also previously invested in Earthly.

[^2]:
    And because everything runs in containers, it is possible in the future to also distribute a single build across a compute cluster for maximum parallelization. Today, Earthly CI only runs on one machine at a time, however.
