---
title: "Incremental Rust builds in CI"
categories:
  - Tutorials
toc: true
author: Nacho

internal-links:
 - just an example
last_modified_at: 2023-09-08
---

In this post, we present [lib/rust](https://github.com/earthly/lib/tree/main/rust), an open-source [Earthly](https://earthly.dev/) library created in collaboration with the [ExpressVPN](https://github.com/expressvpn) core team, that will help you get maximum performance on Rust builds in CI when used in combination with persistent build runners.

lib/rust leverages the same caching features that make your local Rust builds fast. It is also straightforward to use and keeps your build logic (Earthfiles) clean and readable. You just replace `RUN cargo` with `DO rust+CARGO` and get faster builds.

**New to Earthly?** Earthly is like a containerized Make that uses Dockerfile syntax. It lets you express the build logic in a readable and familiar way, runs the builds locally or on remote runners, and can be integrated with your CI provider. See the [Earthly docs](https://docs.earthly.dev/) for more info.

#### Before

~~~{.bash caption=">_"}
lint:
  RUN cargo clippy --all-features --all-targets -- -D warnings
~~~

After:

~~~{.bash caption=">_"}
IMPORT github.com/earthly/lib/rust AS rust

lint:
  DO rust+CARGO --args="clippy --all-features --all-targets -- -D warnings"
~~~

With this change, ExpressVPN saw Cargo build times go from [22.5 minutes](https://github.com/expressvpn/wolfssl-rs/actions/runs/6957128755) to [2.5 minutes](https://github.com/expressvpn/wolfssl-rs/actions/runs/6957805365) (with a warm cache). This level of success was then replicated across a number of other Rust projects of theirs. Here's how.

## Context

> The Rust programming language was designed for slow compilation times.
(Brian Anderson, founding member of Rust core team)

Rust is known for slow compilation times, mainly because it prioritizes runtime performance at the cost of build performance. However, the Rust compiler (rustc) is actually quite advanced, and has been constantly improved over the years. It uses a very sophisticated incremental compilation and benefits from a modular compilation model.

While incremental compilation is enabled by default, achieving faster compilation times in Rust may not be straightforward. Several well-established techniques help control build times on developer machines. These include:

- **Modularizing application logic**: Breaking down application logic into multiple crates that avoid long dependency chains. This not only aids in compilation parallelization, but  also reduces cascade compilation, since a crate will be recompiled whenever a dependent one is.
- U**sing check for quick feedback**: `cargo check` performs a partial compilation that skips the costly step of code generation. It is useful for getting rapid feedback during development, helping catch potential issues early in the coding process.
- **Mindful use of macros and generics**: Careful consideration of the impact of macros and generics on build times is essential. They may bring costly dependencies into your tree and they may generate a ton of code to be compiled.
- **Disabling Link-Time Optimization (LTO)**: In certain cases, disabling LTO can expedite compilation, as it avoids the extra time spent on whole-program optimizations. This is at expense of runtime performance though, usually only suited for development binaries.
- U**sing a faster linker**. While not technically a compiler optimization, using a faster linker is a common and effective way to get faster builds.

In this article, we won't delve into the subject of making local Rust builds fast. We'll assume a Rust project performs well enough on a developer's machine. Instead, our focus will be on achieving a similar level of performance for Rust builds in continuous integration (CI).

### Cargo Caches

Cargo, the official package manager and build tool for Rust, streamlines and automates Rust development tasks such as building, testing, and managing dependencies. It is the widely adopted standard over using the Rust compiler directly, thanks to its convenience and rich feature set.

The caching in Cargo is designed to reduce redundant work by storing previously built artifacts and information about dependencies.

Although Cargo caches' internal structures are not standardized and are subject to change, it is paramount to understand them to maximize their usage in CI builds.

Here are the relevant locations to have in mind when thinking about Cargo caching:

- `$CARGO_HOME/registry/`:  Contains source code of downloaded crates.
- `$CARGO_HOME/git/`:  Contains cloned repositories for git dependencies.
- `$CARGO_HOME/.package-cache`:  The lock file Cargo uses to synchronize cache access from parallel builds.
- .`/target`: The build cache. It contains the binaries and intermediate files of the dependencies corresponding to a particular build specification (e.g. compiler optimizations, target architecture, etc.), as well as the output artifacts of the build.

### Caching in CI

When it comes to CI, the main bottleneck is storing and retrieving information from the cache. Ephemeral CI runners, like GitHub Actions and CircleCI don't have a way to save and retrieve cache without using slow upload/download cache transfers on every run.

For years, the community has been actively seeking improved strategies to minimize build inefficiencies in CI, with the ultimate goal of achieving caching performance for iterative builds that matches the efficiency experienced in local development.

The most popular techniques employed by developers include:

- [Docker bind mounts](https://docs.docker.com/build/guide/mounts/#add-bind-mounts) + CI remote caching (such as [GitHub Actions cache](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)): These approaches can lead to good results but they require hybrid configurations (both at the Dockerfile and workflow definition level).
- Building directly in CI workflows (no Docker) + CI remote caches: Directly building Rust projects within CI workflows and persisting Cargo caches as CI remote caches is an alternative. This method might offer more control for running tests and other build steps, but is still constrained when the goal is generating a Docker image. [Swatinem/rust-cache](https://github.com/Swatinem/rust-cache) falls into this category.
- [sccache](https://github.com/mozilla/sccache), a distributed compiler cache supporting multiple programming languages. While originally designed for Rust, it does have [some limitations](https://github.com/mozilla/sccache/blob/main/docs/Rust.md), notably the absence of support for incremental compilation, which makes it less conducive for development environments. With Cargo providing exceptional caching mechanisms and considering the added complexity of maintaining an sccache server, it doesn't seem to be a widely embraced choice among Rust developers these days.

#### `cargo-chef`

While not designed to optimize Rust CI builds per-se, the tool [cargo-chef](https://github.com/LukeMathWalker/cargo-chef) is worth mentioning since it is the most adopted way of speeding up the creation of Rust Docker images.

In CI, it is commonly used in combination with [Buildkit cache storage backends](https://docs.docker.com/build/cache/backends/).

It works by building the dependencies first, a strategy that allows for caching in the image layer, eliminating the need for downloading and compiling dependencies in subsequent builds that only involve source code changes.

While `cargo-chef` significantly boosts the performance of plain Docker builds, it comes with certain drawbacks that should be taken into account:

- **Cache-within-a-cache-entry**: Since cargo caches are stored in a Docker layer, the invalidation is all-or-nothing. If just one dependency changes, the entire cache is reset.
- **No deduplication**: When multiple builds run concurrently, there is no synchronization across them, resulting in redundant downloads and compilations of crates.
- **Increased verbosity**: Integrating cargo-chef introduces additional complexity to Dockerfiles. Different build arguments necessitate distinct cargo-chef preparations, contributing to increased verbosity.

### Remote Cache Performance

Finally, it's important to note that the previously mentioned approaches come with the inherent speed penalty associated with utilizing remote caching, primarily related to network latency, data transfer, and (de)compression. Every run requires that you download the cache before you start, and upload the cache at the end. This delay impacts the overall efficiency of the caching system, sometimes causing CI builds to be slower with the cache than without it. In addition, remote caches might be significantly constrained in size, like is the case for Github Actions (10GB/repo). Therefore, it should be carefully considered in the broader context of optimizing development and build processes.

## The Insight: Persistent Build Runners

As mentioned above, the community has been looking for better ways to store cached artifacts for years, but we've been missing the fact that using persistent build runners, like [remote Buildkit instances](https://docs.docker.com/build/drivers/remote/) or [Earthly remote runners](https://docs.earthly.dev/ci-integration/remote-buildkit) (also based on Buildkit), can provide a solution for optimal cache performance and management by using them as the cache itself.

Caching via remote runners works by simply reusing the same runner for multiple builds. The runner retains the cache between executions in its local storage, and thus is able to perform significantly better than any caching mechanism that relies on upload and download. There is nothing special that needs to be configured for this to work. All of the features of caching in Earthly or Docker work as expected, including layer caching and cache mounts.

In essence, the runners serve as the cache itself, allowing us to bring the computation to the data rather than the other way around. That is, not only do we side-step the issue of cache persistence, but we also get optimal performance out of the box, since that cache is local to the runner.

## Cache Mounts

Cache mounts are Buildkit constructs that let you complement layer caching, by allowing the contents of a directory to be reused across multiple builds.

~~~{.bash caption=">_"}
RUN --mount=type=cache,sharing=shared,target=$CARGO_HOME
~~~

Cache mounts are ideal in cases where the tool you're using to build is able to leverage incremental caching on its own, like is the case for Cargo, since they:

- Provide great flexibility in defining the scope of cached data.
- Support fine-grained locking, allowing for concurrent access to different parts of the cache.
- Support cache misses without having the whole cache invalidated.
- Reduce redundancy, since the cache can be shared across multiple build steps.

By using cache mounts in combination with persistent remote Buildkit runners we can replicate in CI the exact same iterative efficiency of local builds.

## `lib/rust`

Getting cache mounts right is tricky for Rust though. That's why we decided to implement it as a library. Earthly's [lib/rust](https://github.com/earthly/lib/tree/main/rust) library is a set of Earthly [functions](https://docs.earthly.dev/docs/guides/functions) that your Earthfiles can import as an external API.

This ensures a smoother collaborative experience, keeping your code readable while seamlessly incorporating enhancements from our end into its implementation.

~~~{.bash caption=">_"}
IMPORT github.com/earthly/lib/rust AS rust

lint:
  DO rust+CARGO --args="clippy --all-features --all-targets -- -D warnings"
~~~

Here are some key details about its implementation:

- It stores Cargo caches in cache mounts rather than in the layer cache. As mentioned before, this solves the cache-within-a-cache-entry problem present in cargo-chef, while providing enough flexibility to guarantee the isolation and parallelization of builds.
- One mount cache is for `$CARGO_HOME`, shared across all targets of the same Earthfile under the same Linux OS release version, supporting concurrent builds.
- The second mount cache is for `./target`, shared across all the builds of the same Earthly target but in a blocking mode, resulting in a serial order of execution across them.
- Includes `$CARGO_HOME/.package-cache` in the mount cache so Cargo locking can work and the cache is not corrupted by parallel builds.
- It also makes sure that `$CARGO_HOME/bin` binaries are still accessible, after mounting the caches.
- Ensures installed binaries are stored in the build layers rather than in the mount cache. Notice that `$CARGO_HOME/bin` is not a cache folder, and its contents are not fetched on-demand if they're missing. Storing these binaries in the mount cache could lead to scenarios where BuildKit garbage collects the mount cache, but the layer of the `RUN` command that populated it (installed the binary) is still cached, resulting in a runtime failure.
- Automatically uses [cargo-sweep](https://github.com/holmgr/cargo-sweep) under the hood to keep cache sizes small and efficient. At least until native Cargo CG is fully released.
- We've added an `--output` argument, allowing users to specify which files in the `./target` folder will be copied to the layer cache. Due to the inconsistent structure across various Cargo subcommands and potentially large size of this folder, automatically copying its entire contents is not a feasible option.

## Preliminary Results

We've been building this library with the help of the ExpressVPN core team over the last couple of months, and now, after some time without any issues running their builds across multiple repos, we are comfortable sharing these results with a wider audience.

We've observed significant performance gains across all their repositories (4 so far) by using this library in combination with [Earthly Satellites](https://docs.earthly.dev/earthly-cloud/satellites) (remote runners managed by Earthly) due to the low latency of local caches in combination with the Cargo native optimizations for iterative builds.

Here are some examples from the [wolfssl-rs](https://github.com/expressvpn/wolfssl-rs) repo. The following [Github Actions](https://github.com/expressvpn/wolfssl-rs/blob/main/.github/workflows/ci.yaml) builds comprise multiple parallel jobs, each one of them running an Earthly target in a common Earthly Satellite:

- Cold cache: [22m 41s](https://github.com/expressvpn/wolfssl-rs/actions/runs/6957128755) (similar performance as before using Earthly) ([raw files](https://drive.google.com/file/d/13WTW_aucpagkzDaufZJWS5dnL4108o4P/view?usp=drive_link))
- Warm cache, no code changes: [56s](https://github.com/expressvpn/wolfssl-rs/actions/runs/6957613411) (e.g. just a readme edit) ([raw files](https://drive.google.com/file/d/1bqJUsHN5DzLIwGkJZWoBmdPmoPMJuf1Y/view?usp=drive_link))
- Warm cache, dependency change: [2m 35s](https://github.com/expressvpn/wolfssl-rs/actions/runs/6957752671) ([raw files](https://drive.google.com/file/d/1k52lfWM-UO3KeFjmFncs6GqjT2Yuxnf2/view?usp=drive_link))
- Warm cache, source file change: [2m 31s](https://github.com/expressvpn/wolfssl-rs/actions/runs/6957805365) ([raw files](https://drive.google.com/file/d/1LtR3cXZANTbIRK0rZqqCIVK4_oZqLK0a/view?usp=drive_link))

Relevant points to notice in these examples are:

- For the initial build (empty cache), notice the synchronization among the Github jobs that Cargo enforces. Each job triggers a parallel build in the Satellite – 5 in total – and `lib/rust` sets the same `$CARGO_HOME` and lock file for all of them. As a consequence, crates are downloaded and compiled only once across all the parallel jobs.
- After the cache is initially populated, no more crates are downloaded in the following builds.

If your iterative builds repeatedly download and compile the same crates, it signals an opportunity for improvement, and using `lib/rust` in conjunction with persistent build runners should be beneficial.

## A Complete Example

### Source Code

Suppose the following project structure:

~~~{ caption=">_"}
.
├── Cargo.lock
├── Cargo.toml
├── Earthfile
├── package1
│   ├── Cargo.toml
│   └── src
│       └── ...
└── package2
    ├── Cargo.toml
    └── src
        └── ...
~~~

### Earthfile

The Earthfile would look like:

~~~{ caption=">_"}
VERSION --global-cache 0.7

IMPORT github.com/earthly/lib/rust AS rust

install:
  FROM rust:1.73.0-bookworm
  RUN rustup component add clippy rustfmt

# Call +INIT before copying the source file to avoid installing function depencies every time source code changes

# This parametrization will be used in future calls to functions of the library

  DO rust+INIT --keep_fingerprints=true

source:
  FROM +install
  COPY --keep-ts Cargo.toml Cargo.lock ./
  COPY --keep-ts --dir package1 package2  ./

# lint runs cargo clippy on the source code

lint:
  FROM +source
  DO rust+CARGO --args="clippy --all-features --all-targets -- -D warnings"

# build builds with the Cargo release profile

build:
  FROM +lint
  DO rust+CARGO --args="build --release" --output="release/[^/\.]+"
  SAVE ARTIFACT ./target/release/ target AS LOCAL artifact/target

# test executes all unit and integration tests via Cargo

test:
  FROM +lint
  DO rust+CARGO --args="test"

# fmt checks whether Rust code is formatted according to style guidelines

fmt:
  FROM +lint
  DO rust+CARGO --args="fmt --check"

# all runs all other targets in parallel

all:
  BUILD +build
  BUILD +test
  BUILD +fmt
~~~

### Setting Up the Remote Runner

To get started with deploying your own Buildkit-based remote runner, check out the [Remote Buildkit page in the Earthly docs](https://docs.earthly.dev/ci-integration/remote-buildkit).

For simplicity and completeness of the example, I'll be using [Earthly Satellites](https://docs.earthly.dev/earthly-cloud/satellites), a managed remote runner offering that uses Buildkit underneath (also, there's a [6,000 min/mth free tier](https://cloud.earthly.dev/login) you can use to experiment with).

#### Earthly Install

First of all, you'll need an Earthly Cloud account and Earthly installed on your machine. [Sign up](https://cloud.earthly.dev/login) here and follow the instructions to get you ready.

#### Satellite Creation

From the terminal run:

~~~{.bash caption=">_"}
earthly sat launch my-satellite
~~~

This will create a new Earthly Satellite associated with your account.

### Setting up a Github Actions Workflow

First, you'll need a token for authenticating the Earthly CLI.

#### Authentication Token

The following command will create a token named "github-actions-token" with the default permissions and expiration time. More details about tokens can be found on [Earthly](https://docs.earthly.dev/docs/earthly-command#earthly-account-create-token).

~~~{.bash caption=">_"}
earthly account create-token github-actions-token
~~~

This instruction will return a token value. Copy that value and save it as a secret with the name `EARTHLY_TOKEN` in your [Github Actions configuration](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

> If you are wondering about how your secret could be exfiltrated from a forking PR, the settings in this example should be safe according to the [official GH recommendations](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/).

### Workflow Implementation

Finally, create the following workflow definition in `./.github/workflows/ci.yaml` to run the `+all` target every time a commit is pushed to main or to a pull request.

~~~{.yaml caption="ci.yaml"}
name: GitHub Actions CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  
jobs:
  ci:
    name: +ci
    runs-on: ubuntu-latest
    env:
      FORCE_COLOR: 1
      EARTHLY_TOKEN: "${{ secrets.EARTHLY_TOKEN }}"
    steps:
      - uses: earthly/actions/setup-earthly@v1
      - uses: actions/checkout@v2
      - name: Run +all on Earthly satellite
        run: earthly --ci --satellite my-satellite +all

~~~

At this point you should be able to enjoy the new cache performance 🙂.

Push some commits and see how the build gets cached.

## Feedback Appreciated

We're excited about what we've been working on and would really love to hear your thoughts on it. Your feedback is worth its weight in gold to us, and would help us improve the technique for everybody!

The lib/rust library is open-source! Feel free to [open an issue](https://github.com/earthly/lib/issues/new?labels=rust) in our [lib](https://github.com/earthly/lib) repo or hop into our [#rust](https://earthly.dev/slack) channel on our community Slack for more in-depth discussions.

If you have any comparison data with other techniques, that would be the icing on the cake!

Thanks a bunch for helping us out.

## Acknowledgements

Thanks to:

- [Peter Membrey](https://the.engineer/), Chief of Engineering at ExpressVPN, for planting the seed that made this possible.
- [Ian Campbell](https://www.hellion.org.uk/), Staff Software Engineer on the ExpressVPN core team, for his sharp feedback and contributions to the library implementation.
- [Luca Palmieri](https://www.lpalmieri.com/), author or [cargo-chef](https://github.com/LukeMathWalker/cargo-chef), for his in-depth review of the draft.
- The whole [ExpressVPN](http://www.expressvpn.com) core team for their collaboration, trust and support.
- *`rust-lang`* team members: [Jake Goulding](https://jakegoulding.com/), [Ed Page](https://epage.github.io/), [Josh Triplett](https://joshtriplett.org/), [Weihang Lo](https://github.com/weihanglo), [bjorn3](https://github.com/bjorn3) and [The 8472](https://github.com/the8472) for reviewing early drafts of this article and providing important insights.

If you would like to become a part of ExpressVPN's core team and work on their Rust projects and Earthly build systems, [apply for their job openings](https://www.expressvpn.com/jobs/job-openings/job?gh_jid=7046141002).

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

- [ ] Create header image in Canva

- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
