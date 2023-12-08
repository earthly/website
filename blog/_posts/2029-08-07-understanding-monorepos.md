---
title: "Understanding Monorepos and High-Performance Build Systems"
categories:
  - Tutorials
toc: true
author: Siddhant Varma

internal-links:
 - high-performance build systems
 - build systems
 - understanding monorepos
 - monorepos and build systems
excerpt: |
    This article explores the benefits of monorepos and discusses high-performance build systems like Nx and Turborepo that can help improve the scalability and efficiency of monorepos. These build systems create a dependency tree, utilize caching, and enable parallel job execution to optimize the build process and reduce build times.
last_modified_at: 2023-08-28
---
**This article identifies top tools for optimizing monorepos. Earthly simplifies and standardizes developer builds. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Monorepo is more than just a trendy buzzword today, thanks to its increasing popularity and game-changing advantages. But if you think they've only been around for a few years, think again. Big tech companies like Google have been using Monorepos since time immemorial. Google maintains more than 2 billion lines of code with more than hundreds of terabytes of data. They store all their code in a single monolithic repository and surprisingly they've been doing it since their inception.

For most companies, the engineering overhead and extraordinary effort it takes to set up and maintain a monorepo system are not justified. Moreover, as they scale in size and complexity, their monorepos tend to become slow and increasingly difficult to work with. This is why it's imperative to understand monorepos and how you can leverage them to have a high-performance build system that is easy to scale.

So in this blog post, we'll explore the benefits of monorepos and discuss high-performance build systems like NX and Turborepo that can help you operate at the speed of Google.

Benefits of Monorepos

- Single source of truth
- Easier dependency management
- Consistency in sharing tools and libraries
- Streamlined continuous integration and automation

## Understanding Monorepos and High-Performance Build Systems

Thanks to its growing popularity and game-changing nature, Monorepos are more than just a buzzword these days. However, as the codebase grows in size and complexity, it becomes increasingly difficult to scale a monorepo. Big tech companies like [Google have been using Monorepos](https://research.google/pubs/pub45424/) for a long time, but they have their own in-house version control system and a build tool called [Bazel](https://bazel.build/) (internally called Blaze) to help them easily scale their monorepo.

However, building an in-house version control system and build tools is not feasible for teams of all sizes. As their monorepos start to scale in size and complexity, they tend to present many problems. Build times can start to skyrocket and the developer experience can become unwieldy. This is why it's imperative to understand where monorepos are helpful and how you can leverage high-performance build systems and make it easy to scale your monorepo while keeping its performance intact.

So in this blog post, we'll explore the benefits of monorepos and discuss high-performance build systems like Nx and Turborepo.

## Monorepos in a Nutshell

![Nutshell]({{site.images}}{{page.slug}}/nutshell.png)\

First, let's understand what Monorepos are. Monorepo is an architecture that governs how different applications are treated as a single project to streamline the development, testing and deployment of these applications.

Imagine you have a JavaScript web app, a NodeJS server, and a React Native mobile app that share a lot of common code and dependencies. One option is that you can have each of these apps in separate projects inside their own git repositories. That means you write code for these apps separately, test your changes and deploy them independently of each other.

This workflow is great, simple, and normally works well for most small projects. However, as these projects grow in scale, size, and complexity, you'll realize it's inefficient and requires a lot of repetitive work for building, testing, deploying, and maintaining the codebase. This is where monorepos come in. In the above example, we bind all those different JavaScript projects to a single project under a common git repository.

This single git repository is called a monorepo. Now you can streamline and structure your development workflow for 3 different applications using a common approach for building, testing, and deploying them.

## Benefits of Monorepos

Let's look at some real benefits that stand out when using monorepos against traditional multirepo architecture.

### Single Source of Truth

In a Monorepo, all code changes happen inside a single git repository giving you more visibility towards the git diffs of your applications. In a large organization and a growing codebase with different teams of developers working simultaneously, visibility becomes quintessential.

Further, it's also easy to set up for new developers that join your team. There's a single git repository to clone, fork, and push changes to.

### Consistency in Sharing Tools and Libraries

Monorepos make writing code that you can share across different projects easy. You can create shared libraries like [Loadash](https://lodash.com/), utility functions, and tooling like [ESLint](https://eslint.org/) that can be common for all your applications. You can have a single design system component library that you can use in both your client-side JavaScript and native mobile application.

A consistent way of sharing tools and libraries makes the development workflow more efficient and removes redundant work.

### Easier Dependency Management

As projects grow larger in size, it becomes increasingly complex to configure, manage and track dependencies. Using a single `package.json` file can help reduce the headaches associated with dependency management instead of having multiple config files. You can then use a single command to update or remove them for all the applications.

### Streamlined Continuous Integration and Automation

Monorepos allow you to streamline your CI/CD workflows and introduce automation that works the same way for all your applications. Since all your code is in one place, it's easier to test different builds together and deploy them at the same time via a single command.

## Approaches To Monorepos

So let's first look at some of the common and simple approaches to establishing a monorepo architecture for your project. These approaches rely on existing tools that you already use for your projects.

### Using Package Managers Like Yarn Or Npm

The most basic approach is to use package managers like [Npm](https://www.npmjs.com/) or [Yarn](https://yarnpkg.com/) to define workspaces. Anytime you create a new NodeJS project, a React project or a Vue project, you get a `package.json` file by default in the root directory. Inside the root directory, you already have a nested workspace like apps and packages which are linked to your project.

Further, both npm and yarn deduped your node modules so if you already have a node module or dependency installed, Npm will make sure it doesn't install again. You can also orchestrate scripts that define a certain action like building or testing all of your apps at the same time.

### Using Lerna

The Npm approach works great, but it is limited in the case of an open-source project that publishes different packages. In that case, you'll need a tool that can optimize the workflow of a multi-package repo. One such tool is [Lerna](https://lerna.js.org/).

Lerna can manage these packages as a monorepo. It will version your packages so you don't face the problem of incompatible dependencies. You can also use it to link different packages together. This allows you to use code from one package to another without the need to publish and install it separately.

Finally, you can publish all your packages to npm with a single command using Lerna.

## Challenges of Monorepos

![Challenges]({{site.images}}{{page.slug}}/challenges.png)\

We've discussed several advantages of monorepos and some simple approaches you can take to implement it. However, size is a big problem with these approaches and Monorepos, in general.

Therefore, monorepos become slow and difficult to work with as they grow in size leading to inefficiencies and bottlenecks in your development workflow.

Luckily, we have two great tools today dedicated to managing Monorepos.

## High-Performance Build Systems

To address the performance challenge with Monorepos, you need a build tool that's smart to understand what part of your codebase changes. We'll explore two such tools now - [Nx](https://nx.dev/) and [Turborepo](https://turbo.build/).

### Overview of NX and Turborepo

Both Nx and Turborepo create a dependency tree between all of your apps and packages. They use this dependency tree to understand which part of the codebase has changed and what needs to be rebuilt. They also cache any files or artifacts that have already been built and use that to speed up your builds. Further, they can run parallel jobs to execute everything much faster.

### How They Create a Dependency Tree

Nx and Turborepo analyze the codebase inside our monorepo's workspace. Based on the import and export statements present in our files, they generate a dependency graph accordingly. This graph is then used to optimize the build process and ensure that only the necessary parts of the code are rebuilt when we make changes.

Let's understand this further with the help of an example. Let's say in our project, we have our main application module, which depends on two libraries, `Lib 1` and `Lib 2`. Additionally, `Lib 1` also depends on `Lib 3`. Similarly, `Lib 2` depends on `Lib 4` and `Lib 5`.

Using a tool like Nx or Turborepo, we can generate a dependency graph that shows the relationships between these different modules and libraries:

![Monorepo-dependency-graph]({{site.images}}{{page.slug}}/BFzSfSS.png)

With the above, it's much easier to understand that the `App Module` depends on `Lib 1` and `Lib 2`, which in turn depends on other libraries. This can help us identify potential issues such as circular dependencies, which can cause performance issues and make the code harder to maintain. We can also use this graph to optimize our build process and ensure that only the necessary parts of the code are rebuilt when changes are made.

### Caching

As the dependency graph is getting created, these tools compute a hash for each file and dependency. This hash uniquely identifies the contents of that file or dependency. These hash values are then stored inside a cache on a local disk along with any other relevant metadata that needs to be stored for generating a build pertaining to that file or dependency.

So the next time the tool is run, it first checks if any files or dependencies have changed since the last build ran.

If the values haven't changed, the tool reuses the results of previous computations via the hash eliminating the need to rebuild again. This can save a considerable amount of build time, especially for larger files and expensive computations.

### Parallel Job Execution

Both Nx and Turoborepo internally divide your codebase into small units. When they analyze the dependency graph, they understand which jobs are supposed to be run in parallel. Independent jobs are then run in parallel, whereas jobs that depend on each other still run sequentially.

These tools utilize available CPU resources to spin off multiple threads or processes to execute jobs in parallel. As each job completes, they update the current dependency graph to reflect the new state of the system.

## Nx vs Turborepo

Let's now compare Nx and Turborepo to understand which tool might be better for you.

### Community

Nx has been around for a while now. You're more likely to find enough resources, blog posts, and good documentation to understand how to integrate it into your project. TurboRepo, on the other hand, is relatively new and has fewer resources as compared to Nx and a smaller community.

### Features and Ease of Use

Nx provides a lot of features out of the box as compared to Turborepo. For instance, there's a [VS Code plugin](https://marketplace.visualstudio.com/items?itemName=nrwl.angular-console) that you can use to run test and build commands. Its CLI also generates boilerplates automatically for you. It also provides a feature called [Distributed Task Execution to distribute work across multiple CI servers.

Turborepo, on the other hand, is relatively minimal. It doesn't provide all the features that Nx does by default such as IDE integrations and plugins, built-in code generation and scaffolding and distributed task execution. It also integrates very easily with common package managers like Yarn or Npm. Thus with [minimum configurational changes,](https://turbo.build/repo/docs/core-concepts/monorepos/configuring-workspaces) you can create your existing JavaScript project into a blazingly fast monorepo. Tuborepo seems a good choice for smaller projects where you don't require too much configuration, unlike Nx.

### Remote Caching

While both tools implement caching to generate builds faster, TubroRepo additionally has [remote caching](https://turbo.build/repo/docs/core-concepts/remote-caching). This allows local caches to be synced with a remote cache on a Vercel cloud server so that the entire cache can be downloaded remotely if you're on a different machine.

![Source: [Turbo.Build](https://turbo.build)](https://turbo.build/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flocal-caching.d097807f.png&w=3840&q=75)

Let's say developer A in your team builds an application. Then, developer B configures the monorepo in their machine. The entire cache from Developer A's machine will be downloaded on Developer B's machine. This can save a huge amount of time for a large organization. Since now developer B can use the cached artefacts to create builds on the monorepo that other developers (like developer A) have used).

## Conclusion

Monorepos have become an increasingly popular concept in the context of distributed teams. Taking advantage of the enhanced visibility and efficient code sharing they afford, as well as the potential to test and build complex applications easily, more and more development teams are turning to monorepos. The introduction of high-performance build systems such as Nx and Turborepo can take the power of monorepo to a whole new level, equipping them with features like caching, parallel job execution, and more.

If you're currently looking for a build tool that works great with monorepos, consider checking out [Earthly](https://cloud.earthly.dev/login). As an open source [CI/CD](/blog/ci-vs-cd) framework, Earthly allows you to develop locally and run anywhere. Builds are containerized and language agnostic, and tasks are executed in parallel, which makes it fast. Check out Earthly's detailed [documentation](https://docs.earthly.dev/) to see how you can get started with it easily.

{% include_html cta/bottom-cta.html %}
