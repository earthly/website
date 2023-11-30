---
title: "Building Your JavaScript Monorepo"
categories:
  - Tutorials
toc: true
author: Paul Ibeabuchi
sidebar:
  nav: monorepos

internal-links:
 - CI/CD
 - Monorepo
 - Ecosystem
 - Pipelines 
excerpt: |
    Learn about the different monorepo tools available for building JavaScript projects, including Bazel, Gradle, Lage, Lerna, and Rush. Discover their features, benefits, and drawbacks to determine which one is the best fit for your needs.
last_modified_at: 2023-07-11
---
**This article compares tools for managing monorepos. Earthly ensures build consistency with a containerized approach that is simpler than Bazel's. [Check it out](https://cloud.earthly.dev/login).**

Many engineers and organizations are beginning to adopt a monorepo architecture for their JavaScript projects, where a single repository contains multiple projects. However, ensuring that your pipelines run efficiently and that your builds are occurring in the right order are just a couple of the complexities that a monorepo introduces for your engineering team.

A large JavaScript application has [multiple modules](/blog/go-workspaces) and dependencies; a monorepo tool can manage these dependencies and improve scalability. Fortunately, using a dedicated tool for your monorepo system means you're not spending valuable time away from your core competencies to implement this system yourself.

To help you determine what tool would work best for your project, let's compare five monorepo tools, Bazel, Gradle, Lage, Lerna, and Rush, according to their features, benefits, and drawbacks. We'll analyze factors like:

* Speed
* Learning curve
* Ease of adoption
* Build caching
* How well they detect the scope of changes
* Dependency graph visualization
* Ability to constrain dependency relationships within the repository

Let's dive in.

## Bazel

<div class="wide">
![Bazel Homepage]({{site.images}}{{page.slug}}/t7KgZrS.png)
</div>

Google built [Bazel](https://bazel.build/) to automate software builds and tests, with an aim to make builds reproducible and portable. In other words, for every set of inputs, the same outputs are always produced, regardless of the device on which the build is run.

Some notable features and benefits of Bazel include:

* **It's fast.** It's able to rebuild only necessary file changes by comparing them to previously cached build results. Bazel runs build operations locally by default but you can connect it to a cluster, which makes it even faster.
* **It supports local caching of build results.** However, it also supports [remote caching](https://bazel.build/docs/remote-caching).
* **It supports multiple [languages](https://bazel.build/rules).** Bazel also supports multiple platforms such as Linux, macOS, and Windows, for desktop, server, and mobile.
* **It can handle large projects.** [Bazel](/blog/bazel-build) is reliable when it comes to scaling applications. According to its documentation, it can comfortably handle builds with thousands of source files.
* **It can execute a command on multiple devices while developing locally.** This is unlike other monorepo tools listed in this article.
* **It supports visualization of dependencies between projects and tasks.**

Some drawbacks of Bazel include:

* **It doesn't have native support for code generation.** Therefore, Bazel requires an external tool for generating code.
* **It requires developers to author BUILD files.** This is unlike other tools in this article, which can generate build scripts (e.g., Lage and Lerna can analyze package.json files to achieve this).
* **It takes time to adopt.** Adopting Bazel is a gradual process due to its complexity and requires effort, but it does have exhaustive documentation to guide you through its implementation.

## Gradle

<div class="wide">
![Gradle Homepage]({{site.images}}{{page.slug}}/VgjyI1e.png)
</div>

Gradle is an open-source build automation tool. It uses three build phases, known as its [Build Lifecycle](https://docs.gradle.org/current/userguide/build_lifecycle.html#build_lifecycle):

* **The Initialization Phase.** The environment for the build is set up.
* **The Configuration Phase.** Task configurations are made, i.e, what tasks run first and in what order.
* **The Execution Phase.** The determined tasks run according to the order in the configuration phase.

In a monorepo, Gradle is used to create a **Gradle build file**, which adds dependencies, configurations, and tasks for modules of the repository. You can either create a build file for each module of the repository or a unified build file for the entire repository. The build then runs based on added dependencies.

> Tasks in Gradle are logical instructions to be run and can include actions (e.g., copy files or compile), inputs (values, files), and outputs (files as well).

Some benefits and features of Gradle include:

* **It runs on JVM (Java Virtual Machine).** This makes Gradle friendly for most Java users since build logic can use standard Java APIs.
* **It includes [Build Scan](https://scans.gradle.com/?_ga=2.140991354.933214367.1669595063-1927410915.1669595063).** This is a good tool for insight into your application's performance. You can review performance and find out why or when issues occur.
* **It's fast.** Gradle reuses previous output to determine what inputs need to be executed. It also allows parallel execution of tasks, like running multiple tasks simultaneously, which makes it even faster.
* **It can reuse previous output.** Gradle uses [Build Caches](https://docs.gradle.org/current/userguide/build_cache.html#sec:task_output_caching), allowing it to behave similarly to Bazel.
* **It supports major IDEs.** Examples include VSCode, Eclipse, Android Studio, IntelliJ IDEA, and NetBeans.
* **It supports [dependency management](https://gradle.org/features/#:~:text=be%20Gradle%20builds.-,Dependency%20Management,-Transitive%20Dependencies)**.
* **It can detect changes in projects and packages.** This helps it determine what build or test to run.

Some of the drawbacks of Gradle are:

* **It doesn't provide support for running a command across multiple machines while developing locally.** This is unlike Bazel.
* **Javascript documentation and examples are limited** This may make it difficult to adopt by early programmers.

## Lage

<div class="wide">
![Lage Homepage]({{site.images}}{{page.slug}}/DHJM2gv.png)
</div>

[Lage](https://microsoft.github.io/lage/) (which means "make" in Norwegian) is a build tool that was built by Microsoft, with the aim of improving speed and performance in build processes.

While Lerna and Rush (which are also monorepo tools we'll cover in a bit) make it possible for you to run your npm scripts one at a time in a topological order (that is, build scripts run first and test scripts run only after they're completed), Lage tries to minimize the CPU cycles that could be wasted between those two processes. It uses *terse pipelining syntax* to optimize your build processes, which allocates tasks to available CPU cores rather than waiting and focusing on the order in which the tasks should be run.

Some of the features and benefits of Lage are:

* **It's easy to adopt and get started with.** Lage provides you with documentation that's simpler than Bazel's or Gradle's.
* **It supports both [remote](https://microsoft.github.io/lage/docs/Tutorial/remote-cache) and [local](https://microsoft.github.io/lage/docs/Tutorial/cache) build caching.** Therefore Lage doesn't run a task twice, which makes it fast.
* **It can detect scope changes by examining a [target graph](https://microsoft.github.io/lage/docs/Introduction#how-does-lage-schedule-tasks) to know what targets are not affected by new changes.** This is similar to Gradle.
* **It allows you to [prioritize](https://microsoft.github.io/lage/docs/Tutorial/priority) tasks.** You can schedule tasks in the order with the most optimal run time.
* **It comes with a built-in profiler.** This lets you visualize your build graphs.

Some of the drawbacks of Lage are:

* **It doesn't provide support for running a command across multiple machines.** This is similar to Gradle.
* **It only works with npm.** Lage can only run npm scripts.

## Lerna

<div class="wide">
![Lerna Homepage]({{site.images}}{{page.slug}}/AIbm4aX.png)
</div>

[Lerna](https://lerna.js.org/) is a monorepo tool for TypeScript/JavaScript. It allows you to create multiple packages in a single repository. Lerna v5+ [can use Nx (an open source build system) to run tasks](https://twitter.com/i/status/1529493314621145090), which is super fast. Like Lage, Lerna runs npm scripts and uses JavaScript. Some Lerna users include top libraries and frameworks such react-router, Jest, and Babel.

Some of the features and benefits of Lerna are:

* **It's easy to get started with and adopt.** Lerna requires minimal configuration and uses JavaScript, which is common to most web developers.
* **It provides you with detailed documentation for getting started.**
* **It's free.**
* **It provides graph visualization.**
* **It caches results locally.** This is similar to most other tools. It's also able to run only tasks that have been affected by code changes.
* **It makes it possible to share computation caches between developers or CI/CD machines.**
* **It allows you to run a command across multiple machines.** This is unlike Lage.
* **It lets you specify the relationship between npm scripts (or targets).**

Some of the drawbacks of Lerna are:

* **It's [not actively maintained](https://github.com/lerna/lerna/issues/2703).** This is despite its popularity.
* **It only works with npm.** That is, Lerna doesn't integrate well with programming languages, tools or platforms. This is unlike Bazel.

## Rush

<div class="wide">
![Rush Homepage]({{site.images}}{{page.slug}}/p3OTmeg.png)
</div>

[Rush](https://rushjs.io/) is another build tool made by Microsoft. It's a scalable monorepo manager designed for large teams to handle large repositories. Rush is used by organizations like OneDrive, Windows Store, and Wix.

Microsoft also created Rush Stack which contains components that can be used with Rush, such as:

* [API Extractor](https://api-extractor.com/), which coordinates API reviews.
* API Documenter, which helps to generate your [API documentation](https://api-extractor.com/pages/setup/generating_docs).
* [Rundown](https://www.npmjs.com/package/@rushstack/rundown), which helps to optimize Node.js process startup times.

Some of the features and benefits of Rush are:

* **It's able to detect changes in dependency in order to run build.** This is similar to most other tools.
* **It's free and open source.** This is similar to Lerna.
* **It supports [build caching](https://rushjs.io/pages/maintainer/build_cache/).** However, this is currently an experimental feature, as stated in Rush's documentation.
* **It can automatically generate a Changelog.**
* **It's commonly used around the web.** Rush also uses JavaScript.

Some of the drawbacks of Rush are:

* **It doesn't support graph visualization.**
* **It doesn't support multiple languages or multiple platforms.** This is unlike Bazel.

## Conclusion

These five common monorepo tools — Bazel, Gradle, Lage, Lerna, and Rush — all have their own features, benefits, and drawbacks for building JavaScript and TypeScript [monorepos](/blog/go-workspaces). The good news is that regardless of which one works best for your situation, you can still use [Earthly](https://cloud.earthly.dev/login) with all of them.

As an open source [CI/CD](/blog/ci-vs-cd) framework, Earthly allows you to develop locally and run anywhere. Builds are containerized and language agnostic, and tasks are executed in parallel, which makes it fast. Check out Earthly's detailed [documentation](https://docs.earthly.dev/) to see how you can get started with it easily.

{% include_html cta/bottom-cta.html %}
