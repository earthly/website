---
title: "Building a Monorepo with Rust"
categories:
  - Tutorials
toc: true
author: Kumar Harsh

internal-links:
 - just an example
excerpt: |
    This markdown content provides a checklist for writing and publishing an article, including steps such as outlining, drafting, proofreading, creating a header image, and adding internal links. It also includes a checklist for optimizing an article for external publication, including adding an author page, optimizing images, and incorporating external links.
---

Managing multiple software projects and their dependencies can often become a complex and time-consuming task, but monorepos can help.

A monorepo, or monolithic repository, is a single repository that houses all of the code for an organization or project, including its libraries, applications, and tools. This approach offers several advantages over traditional multirepository setups, particularly for Rust projects.

For instance, for Rust developers, monorepos provide a unified platform for managing code dependencies, ensuring consistent versioning and facilitating code reuse across projects. Additionally, monorepos streamline the development process by enabling developers to easily share code between projects and quickly test changes across the entire codebase.

In this article, you'll learn all about monorepos, including the benefits they offer for Rust projects. You'll also see what the process of setting up a monorepo using Cargo, Rust's package manager, looks like.

## Why Should You Use a Monorepo?

When it comes to working with multiple projects, sooner or later, you'll need to choose between using a monorepo or polyrepo setup.

In a monorepo layout, multiple projects coexist in the same repository (according to a preset hierarchical structure). In a polyrepo setup, each project gets its own repository. This means you need to manage the dependencies and lifecycle of each project independently.

There are multiple reasons why you would want to go with a monorepo approach when working in Rust, including:

* **Simpler dependency management:** Monorepos eliminate the need to manage dependencies across multiple repositories, which simplifies the process of installing, updating, and tracking dependencies. With all the code residing in a single repository, developers can easily browse, search, and understand the relationships between different codebases and ensure that dependencies are compatible and up to date.
* **Consistent versioning:** Monorepos enforce consistent versioning across all codebases, eliminating the potential for conflicts and discrepancies between dependencies. This consistency simplifies dependency management, reduces the risk of compatibility issues, and ensures that all projects within the monorepo are working with the same versions of shared libraries and tools.
* **Enhanced code reuse:** Monorepos provide a centralized repository for shared code modules and libraries. Developers can easily discover and utilize common code components across different projects, promoting code consistency, reducing development time, and minimizing code duplication.
* **Facilitated cross-project testing:** Monorepos enable developers to easily test changes across the entire codebase. With all the code residing in a single repository, developers can quickly identify and address integration issues between different projects, ensuring that changes in one project don't break dependencies in others.
* **Improved collaboration and communication:** Monorepos encourage collaboration and communication among developers by providing a shared workspace for all codebases. Developers can easily track changes made by others, share code snippets, and discuss potential issues or improvements. This fosters a more collaborative and productive development environment.

While monorepos offer numerous benefits, it's crucial to carefully consider the size and complexity of your project before adopting this approach. Monorepos can become challenging to manage for large-scale projects with a lot of contributors. Additionally, the size of a monorepo can impact development tools, such as IDEs, and may require specialized tooling to optimize performance.

## What a Monorepo Layout in Rust Looks Like

A monorepo can contain multiple components, such as services and libraries. For instance, if you're working with a monorepo that's focused on providing content moderation functionality, it should have a dedicated library for content moderation operations, namely censoring ableist and violent language. These operations can be used at various points of interaction with data, such as when recording (or ingesting) user input or when running routine cleanup jobs.

Here's what the directory structure for such a monorepo would look like:

~~~
.
├── libs
│   └── filter
│       └── src
│           └── lib.rs
└── services
    ├── cleanup
    │   └── src
    │       └── main.rs
    └── ingest
        └── src
            └── main.rs
~~~

The `filter` library makes use of a dependency called [`censor`](https://docs.rs/censor). The two service modules use the library as a dependency to access the censoring functionality.

## How to Build a Monorepo With Rust

Using the previous example, the following sections show you how you can build a monorepo with Rust.

### Create Rust Modules

First, you need to create the Rust modules listed above. Here's what the `filter` library looks like:

~~~
use censor::*;

pub fn filter_ableism(text: String) -> String {

    let censor = Censor::Standard + "lame" + "dumb" + "retarded" + "blind" + "deaf";

    return censor.censor(&text);
}

pub fn filter_violence(text: String) -> String {
    let censor = Censor::Standard + "attack" + "dead" + "murder" + "kill";

    return censor.censor(&text);
}
~~~

It essentially censors out a standard set of blacklisted words, along with a few custom words defined by the user.

The `ingest` service looks like this:

~~~
use filter::filter_violence;

fn main() {

    let text = "A blind person was killed in yesterday's riots".to_string();

    let mut clean_text = filter_violence(text);

    println!("{}", clean_text);
}
~~~

Currently, the implementation is merely a `main` function that calls the `filter_violence` function from the `filter` library. In a real-world scenario, you would probably implement this as a REST endpoint that receives user-generated content, runs the moderation on it, and then saves the cleaned content to the data store.

Here's what the `cleanup` service looks like:

~~~
use filter::*;

fn main() {

    let text = "A blind person was killed in yesterday's riots".to_string();

    let mut clean_text = filter_ableism(text);
    clean_text = filter_violence(clean_text);

    println!("{}", clean_text);
}
~~~

This is similar to the `ingest` service, except that it uses two of the `filter` functions, `filter_ableism` and `filter_violence`, and is distinct from the `ingest` service. In a real-world project, you would implement this as a routine job that reads newly added records in a data store, runs the cleanup operations on them, and then writes the clean data back to the store.

To run this project, you need to set up the configuration in a way that allows the local `filter` module to be imported as a dependency by the two services. To do that, you need to use a monorepo management tool.

### Build Tooling for a Monorepo in Rust

There are multiple tools available to help you manage monorepos in Rust. Two of the most popular tools are [Cargo](https://doc.rust-lang.org/cargo/) and [Bazel](https://bazel.build/).

Cargo is the default package manager for Rust, and it offers a simple approach to building monorepos. It provides built-in support for managing multiple packages within a single repository, which allows developers to leverage their existing knowledge of Cargo for monorepo development.

Cargo workspaces, a key feature of Cargo, enable seamless management of dependencies between packages within the monorepo. Each module maintains its own `Cargo.toml` file, while a shared `Cargo.lock` file ensures consistent dependency versions across the codebase. This approach simplifies dependency management and promotes code reuse among packages.

In contrast, Bazel, a build system developed by Google, provides a more powerful and flexible approach to building monorepos. It offers advanced features like caching, remote execution, and distributed builds, making it well-suited for large-scale projects with complex dependency relationships.

Bazel's declarative build language allows developers to define how targets (representing units of compilation or execution) should be built. This explicitness provides greater control over the build process and enables optimization for specific platforms and configurations.

In this article, you'll learn how to use Cargo to manage the monorepo you've just created.

### Use Cargo to Manage the Monorepo

As mentioned previously, each Rust module needs to contain its own `Cargo.toml` file. Here's the `Cargo.toml` file for the `filter` library:

~~~
[package]
name = "filter"
version = "0.1.0"
edition = "2021"

[dependencies]
censor = "0.3.0"
~~~

This file sets the basic package details of the library and then defines an external dependency to be used in it (`censor`).

The `Cargo.toml` file for the `ingest` service looks like this:

~~~
[package]
name = "ingest"
version = "0.1.0"
edition = "2021"

[dependencies]
filter = { workspace = true }
~~~

After setting the basic package details of the service, this file imports the `filter` library as a dependency. However, since it's a local dependency, you can't specify a version for it as you did for `censor`. Instead, you would normally need to provide its path to Cargo, such as `filter = { path = "libs/filter" }`.

In this case, you need to provide the same path twice to the two services since they both use the same dependency. To avoid that added complexity (and to keep things easy to manage), this package inherits the `filter` library from its workspace's dependencies. You define the path to the dependency only once, in the workspace-level `Cargo.toml` file.

The `Cargo.toml` file for the `cleanup` service looks similar to that of `ingest`:

~~~
[package]
name = "cleanup"
version = "0.1.0"
edition = "2021"

[dependencies]
filter = { workspace = true }
~~~

This is what the `Cargo.toml` file for the workspace looks like:

~~~
[workspace]
members = [
    "services/cleanup",
    "services/ingest"
]

[workspace.dependencies]
filter = { path = "libs/filter" }
~~~

This differs from the package-level files because it defines the members of the workspace and references the `filter` library as a workspace-level dependency. Any member of the package can now easily inherit the library.

This is what your directory structure should look like now:

~~~
.
├── Cargo.toml
├── libs
│   └── filter
│       ├── Cargo.toml
│       └── src
│           └── lib.rs
├── services
│   ├── cleanup
│   │   ├── Cargo.toml
│   │   └── src
│   │       └── main.rs
│   └── ingest
│       ├── Cargo.toml
│       └── src
│           └── main.rs
~~~

At this point, you can build the monorepo by running the command `cargo build` at the root of your repo. Here's what the output looks like:

~~~
Compiling ingest v0.1.0 (/Users/kumarharsh/Work/Draft/rust-mono/services/ingest)
Finished dev [unoptimized + debuginfo] target(s) in 0.07s
~~~

Run `cargo run --bin ingest` or `cargo run --bin cleanup` to run the individual binaries built by Cargo. The outputs look like this:

~~~
$ cargo run --bin ingest
Finished dev [unoptimized + debuginfo] target(s) in 0.01s
Running `target/debug/ingest`
A blind person was ****ed in yesterday's riots

$ cargo run --bin cleanup
Finished dev [unoptimized + debuginfo] target(s) in 0.00s
Running `target/debug/cleanup`
A ***** person was ****ed in yesterday's riots
~~~

This confirms that the dependencies have been correctly configured in your project. You can now use `cargo add <dependency> --package <package-name>` to easily add new dependencies to the packages.

### A Simpler Solution: Earthly

Now that you know how to run and manage a monorepo locally, it's time to configure a build tool that can containerize the packages and run tests in a simpler way. [Earthly](https://earthly.dev/) is a great alternative for these tasks.

Earthly is a build tool that enables each service or library to independently handle its own build and test cycles. It also supports caching, which means that only the packages that have been updated will retrigger their build.

To configure Earthly in this project, you need to add an `Earthfile` in each of the packages and one parent `Earthfile` at the root of the project. Here's the `Earthfile` for the `filter` library:

~~~
VERSION --global-cache 0.7
IMPORT github.com/earthly/lib/rust:2.2.10 AS rust

FROM rust:slim-buster
WORKDIR /libs/filter

# build creates the binary target/release/filter
build:
    # Cargo UDC adds caching to cargo runs.
    # See https://github.com/earthly/lib/tree/main/rust
    DO rust+INIT --keep_fingerprints=true
    COPY --keep-ts --dir src Cargo.lock Cargo.toml .
    DO rust+CARGO --args="build --release --lib" --output="release/(.*).rlib"
    SAVE ARTIFACT target/release/libfilter.rlib filter

# test runs the tests present in the package
test: 
    FROM +build
    RUN cargo test
~~~

This file enables the package to be built into a self-contained artifact, which you can then reference easily in other services. Here's the `Earthfile` for the `ingest` service:

~~~
VERSION --global-cache 0.7
IMPORT github.com/earthly/lib/rust:2.2.10 AS rust

FROM rust:slim-buster
WORKDIR /services/ingest

deps:
    LOCALLY
    SAVE ARTIFACT ../../libs/filter src/libs/filter 
    SAVE ARTIFACT ../cleanup/ src/services/cleanup
    SAVE ARTIFACT ./ src/services/ingest
    SAVE ARTIFACT ../../Cargo.toml src/Cargo.toml

build:
    FROM rust:slim-buster
    COPY --dir +deps/src .
    WORKDIR src
    DO rust+INIT --keep_fingerprints=true
    DO rust+CARGO --args="build --release --bin ingest" --output="release/[^/\.]+"
    SAVE ARTIFACT target/release cleanup


# test runs the tests present in the package
test: 
    FROM +build
    RUN cargo test

# docker creates docker image ingest:latest
docker:
    FROM +build
    ENTRYPOINT ["./ingest"]
    SAVE IMAGE ingest:latest
~~~

This file defines its own build and Docker steps and makes use of the artifact generated by the `filter` library to include it in the final binary.

The `Earthfile` for the `cleanup` service is quite similar to that of `ingest`:

~~~
VERSION --global-cache 0.7
IMPORT github.com/earthly/lib/rust:2.2.10 AS rust

FROM rust:slim-buster
WORKDIR /services/cleanup

deps:
    LOCALLY
    SAVE ARTIFACT ../../libs/filter src/libs/filter 
    SAVE ARTIFACT ../ingest/ src/services/ingest
    SAVE ARTIFACT ./ src/services/cleanup
    SAVE ARTIFACT ../../Cargo.toml src/Cargo.toml

build:
    FROM rust:slim-buster
    COPY --dir +deps/src .
    WORKDIR src
    DO rust+INIT --keep_fingerprints=true
    DO rust+CARGO --args="build --release --bin cleanup" --output="release/[^/\.]+"
    SAVE ARTIFACT target/release cleanup


# test runs the tests present in the package
test: 
    FROM +build
    RUN cargo test

# docker creates docker image cleanup:latest
docker:
    FROM +build
    ENTRYPOINT ["./cleanup"]
    SAVE IMAGE cleanup:latest
~~~

Finally, here's the parent `Earthfile` that allows you to use the steps defined in the package `Earthfile`s easily:

~~~
VERSION 0.7

all-docker:
    BUILD ./services/ingest+docker
    BUILD ./services/cleanup+docker

all-test:
    BUILD ./libs/filter+test
    BUILD ./services/cleanup+test
    BUILD ./services/ingest+test
~~~

You can now build the entire monorepo using the command `earthly +all-docker`. You can also run tests for all packages using the command `earthly +all-test`.

## Conclusion

Monorepos in Rust facilitate code reuse, streamline dependency management, and enhance collaboration among developers. However, choosing the right approach and tooling is crucial for maximizing the benefits of monorepos.

In this article, you learned that [Cargo workspaces](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html) provide a straightforward and efficient solution for managing monorepos. However, for larger, more complex projects, it becomes important to set up a build tool like [Earthly](https://earthly.dev/) that enables easy containerization, testing, and other operations that you would want to run as part of your CI pipelines.

You can find the complete monorepo created as part of this article in [this GitHub repository](https://github.com/krharsh17/rust-monorepo.git). Make sure to check out the [Earthly blog](https://earthly.dev/blog/) to learn more ways you can simplify your DevOps efforts.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images
* [ ] Verify look of article locally
  * Would any images look better `wide` or without the `figcaption`?
* [ ] Add keywords for internal links to front-matter
* [ ] Run `link-opp` and find 1-5 places to incorporate links
