---
title: Frequently Asked Questions
layout: page
---
<!-- vale HouseStyle.H2 = NO -->
<link rel="stylesheet" href="/assets/css/subpage.css">

<h2 class="text-2xl font-semibold mb-5 mt-20" id="existing-ci">Can I use Earthly with my existing continuous integration (CI) system?<span class="hide"><a href="#existing-ci">¶</a></span></h2>

Yes, both Earthly and Earthly Satellite can be used from existing continuous integration (CI) systems. We have documented integrations for some [popular CI systems](https://docs.earthly.dev/docs/ci-integration) but it is likely that you will be able to get earthly working with any other CI System. Hop in our [Slack channel](/slack) and you may find others using your CI system of choice.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="performance">How does Earthly Cloud achieve 2-20X performance gain compared to traditional CIs?<span class="hide"><a href="#performance">¶</a></span></h2>

Earthly was designed from the ground up to be fast and to reuse as much previous work as possible in every run, without compromising usability or versatility. Earthly Cloud achieves 2-20X performance gain via a combination of caching and parallelization.

Earthly's caching is based on the idea of image building layer caching, except that it is extended beyond image building, to also include testing, linting, code generation, producing non-image artifacts (such as binaries), and other use-cases typically involved in the CI/CD process. The layer caching technique allows Earthly to reuse computation from a previous run for the parts of the build where nothing has changed.

A key performance feature of Earthly Cloud is the fact that the cache does not require any uploads or downloads. It is just there, available instantly when the build runs. By contrast, a traditional CI has a caching system with significantly less capabilties, but it also requires uploads and downloads, which can be a significant performance bottleneck. With traditional CIs caching something usually results in slower build times, because of the upload/download overhead.

Earthly's parallelization is based on the fact that every component of the build executes in a container. As the container has clear inputs and outputs and is otherwise isolated from the rest of the process, the system can create a dynamic direct acyclic graph (DAG) and parallelize its operations to the maximum extent possible. Although currently, Earthly executes builds on a single machine, it is designed to be able to scale even further to multiple machines in the future.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="satellites">What are Earthly Satellites?<span class="hide"><a href="#satellites">¶</a></span></h2>

Earthly Satellites are a part of and included with Earthly Cloud. Satellites are single-tenant remote runners managed by the Earthly team. Satellites are frequently used as remote runners in CI or development workflows.

Common use-cases for using Satellites include:

- Using satellites on top of a traditional CI, in order to take advantage of the Earthly caching and parallelization capabilities
- Using satellites in local development workflows in order to share compute and cache with colleagues
- Using satellites in order to execute x86 builds on ARM (or Apple Silicon) machines, or vice-versa

To learn more about our plans, please visit our [pricing page](/pricing).

<h2 class="text-2xl font-semibold mb-5 mt-20" id="monorepo">How does Earthly handle monorepo setups and what makes it special?<span class="hide"><a href="#monorepo">¶</a></span></h2>

Earthly  is designed to perform minimal work when a build is triggered. In a monorepo setup this means only rebuilding the components within the repository that have actually changed. This allows Earthly to scale to large monorepo setups, without sacrificing performance.

Additionally, Earthly's strong reusability constructs allows for parts of the build to be shared between different sub-projects. The interdependencies between the sub-projects are expressed in the Earthfile, and the system will automatically detect when a sub-project has changed and needs to be rebuilt.

In a traditional CI system, the chain between a changed file and the set of deliverables that need to be rexecuted (artifacts to be rebuilt, tests to be rerun, deployments to be refreshed) is not known to the system. The only available setting is often configuring triggers based on changes to subdirectories of a monorepo. However that strategy has significant limitations that don't work well in real-world scenarios. Either the triggers are too aggressive and result in builds that grind the team to a halt, or they are too conservative and result in accidentally shipping changes that do not pass testing. No traditional CI supports monorepos properly.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="polyrepo">How does Earthly handle polyrepo or hybrid setups and what makes it special?<span class="hide"><a href="#polyrepo">¶</a></span></h2>

Earthly has strong reusability constructs that allow for parts of the build to be referenced or imported from other repositories. It is possible to import artifacts, images and recipes from other repositories, such that the build definition is not repeated.

Earthly's caching system is designed to only rebuild referenced deliverables only when they have actually changed. It is git-hash-aware, and even when changes are present, it only rebuilds the parts that are actually impacted by the change.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="nix">How does Earthly compare to Nix?<span class="hide"><a href="#nix">¶</a></span></h2>

Both [Nix](https://nixos.org/) and Earthly are focusing on improving the way that software is built but we believe they have different goals. Nix is focused on providing a declarative way to specify the build environment and dependencies of a project. Earthly is focused on providing a declarative way to specify the build pipeline of a project.

At a technical level, both Nix and Earthly use Linux namespaces to provide file system isolation. Earthly uses namespaces via Runc, using BuildKit whereas Nix uses them directly. At a higher level, though, Earthly is focused on providing an easy-to-write language for declaring all the steps of a complex build pipeline. This often includes things that may not be a good fit for the Nix build model, such as code linting, starting up and tearing down dependent services, making network calls, and running integration tests.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="bazel">How is Earthly different from Bazel?<span class="hide"><a href="#bazel">¶</a></span></h2>

[Bazel](https://bazel.build/) is a build tool developed by Google to optimize the speed, correctness, and reproducibility of their internal monorepo codebase. The main difference between Bazel and Earthly is that Bazel is a **build system**, whereas Earthly is a **general-purpose CI/CD framework**.

Bazel focuses on compiling and unit testing, and it does so in a highly opinionated manner. Bazel is an extremely efficient build system that provides speed, correctness, and reproducibility. But Bazel is difficult to adopt, and you have to implement it correctly to get its benefits. Achieving anything beyond compiling and unit testing is difficult and time-consuming.

Earthly, on the other hand, can be used for general-purpose CI/CD use cases. Earthly can compile and run unit tests like Bazel, but, it goes beyond that, allowing integration testing, deployment to production, executing arbitrary scripts, performing custom packaging, etc.

Bazel does exceptionally well in very specific environments, for very specific use cases, but it is not a general-purpose CI/CD framework.

For these reasons, Bazel is often run in conjunction with Earthly, rather than instead of it. Here is an [example of how to do that in the Earthly repository on GitHub](https://github.com/earthly/earthly/tree/main/examples/bazel). In particular, the combination of Bazel and [Earthly Satellites](https://earthly.dev/pricing) (or self-hosted [Earthly remote runners](https://docs.earthly.dev/ci-integration/remote-buildkit)) allows Bazel’s cache to be saved on the remote runner and instantly available on the next build. This can make Bazel executions in CI very fast.

One of Bazel’s use cases is managing builds for a monorepo setup. For this use case, there is some overlap with what Earthly can do. Here are some key differences between the two:

- Earthly is significantly easier to adopt. Every new programming language that Bazel needs to build requires onboarding, and all build files usually need to be completely rewritten. This can be a significant investment of time and effort from the team adopting it. For large codebases, migration often takes a few years. Earthly, on the other hand, does not replace language-specific tools. This makes migrating to Earthly much faster and easier, only taking a few weeks to a few months.
- The learning curve of Earthly is much lower than Bazel. Learning Earthly is especially easy if you already have experience with Dockerfiles. Bazel, on the other hand, introduces several new concepts and a custom programming language. The difficulty of learning how to use Bazel means fewer engineers across a team will be able to use it. Earthly's simplicity makes it easier to democratize builds across a team than with Bazel.
- Bazel has a purely descriptive specification language. Earthly is a mix of descriptive and imperative language.
- Earthly does not do file-level compilation caching on its own. Bazel does. So incremental compilation of large codebases is faster on Bazel. You can set up Earthly to cache individually compiled files, but that requires more work (we're working to improve this).
- Bazel’s consistency is more correct and more difficult to achieve, while Earthly’s consistency is more practical. Bazel uses tight control of compiler toolchains to achieve true hermetic builds, whereas Earthly uses containers and well-defined inputs. Bazel achieves truly reproducible builds – the output is byte-for-byte consistent across systems – when run in hermetic environments (compiler versions match, dependencies match, etc.). Earthly achieves repeatable builds – consistency is guaranteed by using containers to ensure that the build executes in a similar environment. The build output is usually not byte-for-byte the same except under specific situations (e.g. dependencies are pinned to fixed versions, compilers used in the build don't introduce timestamps, etc.).

For more information about when to use Bazel, check out our blog, where we have written an [extensive article on the topic](https://earthly.dev/blog/bazel-build/).

<h2 class="text-2xl font-semibold mb-5 mt-20" id="dagger">How is Earthly different from Dagger?<span class="hide"><a href="#dagger">¶</a></span></h2>

Both [Dagger](https://dagger.io/) and Earthly are open-source CI/CD frameworks that use BuildKit and containerization to improve the CI workflow. With both tools, you can run the CI or CD process locally, which is a big step forward from the world of needing to work with a centralized build process.

The most fundamental difference between Earthly and Dagger is that through Earthly Cloud, Earthly forms a complete build automation platform optimized for the democratization of builds within the engineering team, and for unlocking team productivity at a level no CI/CD platform can match.

In terms of build specification, Earthly and Dagger differ in the following ways:

- Earthly uses an `Earthfile` to specify a build in a format that takes inspiration from Dockerfiles, shell scripting, and Makefiles. As a result, if you know how to perform a step in your build process at the command line, you know how to do it in Earthly.
- Dagger uses an SDK to configure build steps via general-purpose programming languages, such as Go and Python.

This difference means Earthly is more accessible to both experienced and first-time users. Many users can understand and make simple changes to Earthfiles without reading any documentation, which goes a long way toward democratizing builds within the engineering team. On the other hand, Dagger can require a considerable learning investment. This investment can pay off: there are forms of abstraction available in Dagger, which are harder to encode in Earthly. If you need those features, Dagger might be a great choice.

But overall, we believe Earthly's strong focus on [approachability](https://earthly.dev/blog/platform-values/#approachability) and ease of use is a fantastic match for most organizations.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="dockerfile">How is Earthly different from Dockerfiles?<span class="hide"><a href="#dockerfile">¶</a></span></h2>

[Dockerfiles](https://docs.docker.com/engine/reference/builder/) were designed for specifying the make-up of Docker images and that's where Dockerfiles stop. Earthly takes some key principles of Dockerfiles (like layer caching) but expands on the use cases. For example, Earthly can output regular artifacts, run unit and integration tests, and create several Docker images at a time - all of which are outside the scope of Dockerfiles.

Earthly introduces a richer target, artifact, and image [referencing system](https://docs.earthly.dev/guides/target-ref), allowing for better reuse in complex builds spanning a single large repository or multiple repositories. Because Dockerfiles are only meant to describe one image at a time, such features are outside the scope of applicability of Dockerfiles.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="usedocker">Why not just use Docker and bash/make/python/ruby/etc?<span class="hide"><a href="#usedocker">¶</a></span></h2>

Sure, you can do that. That's how Earthly started.

Earthly grew out of a wrapper around Dockerfiles. As your project grows, your build and testing requirements will grow too. You might end up with multiple Dockerfiles, you might need to support running tests and builds on Linux, MacOS, and Windows, you might run into parallelization issues, and you might need to scale across multiple repositories. After all that hard work, the performance of the build will still be limited, because it would rely on traditional CI technologies, with limited parallelism and caching.

Earthly grew out of all of these requirements and is supported by a growing user base, which (most likely) offers a more battle-tested code base than your custom in-house wrapper.

Still think you should just write your own wrapper? We have some tips on our [blog](https://earthly.dev/blog/repeatable-builds-every-time/).

<h2 class="text-2xl font-semibold mb-5 mt-20" id="multistage">Is Earthly a way to define a Docker multi-stage build?<span class="hide"><a href="#multistage">¶</a></span></h2>

Defining [multi-stage image builds](https://earthly.dev/blog/docker-multistage/) is one possible use case, although Earthly is typically used in much more complex use cases than that. Earthly is not only a tool for producing container images. Earthly is a tool for building cross-platform build specifications. It can produce container images but it can also be used to produce binary artifacts, run tests, lint code, and anything else you would normally do inside of a build pipeline in a CI system.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="pl">Can I use Earthly with my programming language or command line build tools?<span class="hide"><a href="#pl">¶</a></span></h2>

Yes. If it's possible to create a docker image with your programming language, compiler, and tools of choice installed then it's possible to use these with Earthly.

Earthly is especially popular with those who need to work with several languages or tools in a single build pipeline. Earthly can act as a glue layer that holds the various tools together and provides caching and parallelism across them.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="build">Can Earthly build Dockerfiles?<span class="hide"><a href="#build">¶</a></span></h2>

Yes! You can use the command `FROM DOCKERFILE` to inherit the commands in an existing Dockerfile.

<pre class="p-4 mb-6 bg-gray-100">
  <code>
    build:
      FROM DOCKERFILE .
      SAVE IMAGE some-image:latest
  </code>
</pre>

One limitation to using `FROM DOCKERFILE` in Earthly is that you cannot `COPY` artifacts created in a previous Earthly step in the middle of the Dockerfile build. You also cannot use a base image produced by Earthly earlier in the build to be used as part of the Dockerfile build.

As an alternative, you may port your Dockerfiles to Earthly entirely. Translating Dockerfiles to Earthfiles is usually a matter of copy-pasting and making minor adjustments. See the [basics tutorial](https://docs.earthly.dev/basics) for some Earthfile examples.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="host">Where does Earthly host the build runners?<span class="hide"><a href="#host">¶</a></span></h2>

Earthly Cloud is a fully managed SaaS offering that includes Earthly Satellite runners. The servers are hosted in AWS on the West Coast in the USA. The runners are single-tenant. For more information regarding our security measures please see our [security page](/security).

{: .mb-6 .text-lg .font-medium .text-gray-600 .sm:w-full .sm:text-lg .sm:leading-8 .sm:mb-6 }

<!-- vale HouseStyle.H2 = YES -->
<div class="color2">
  <div class="wrapper">
    {% include home/earthlyButton.html padding="pt-8" %}
  </div>
</div>
