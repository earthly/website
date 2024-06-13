---
title: "Optimizing Rust Build Speed with sccache"
toc: true
author: Ryan Peden

internal-links:
 - sccache
excerpt: |
    This tutorial explains how to use sccache, a tool that can speed up Rust compilation by caching the output of compilation and reusing it for subsequent builds. It covers installing and configuring sccache, integrating it with Cargo, measuring and optimizing build performance, and using caching in continuous integration (CI) environments.
categories:
  - rust
---
**This article discusses how to optimize Rust builds. Earthly significantly speeds up Rust build times. [Learn more](https://cloud.earthly.dev/login).**

Rust is a powerful and expressive programming language that offers many benefits, including memory safety, performance, and concurrency. However, Rust is also known for being slow to compile, especially for large and complex projects. This can frustrate developers who want to iterate quickly and test their code.

Thankfully, there's a way to speed up Rust compilation using a tool called [sccache](https://github.com/mozilla/sccache). sccache is a distributed compiler cache that caches the output of Rust compilation and reuses it for subsequent builds. It can significantly reduce the build time and improve the developer experience.

In this tutorial, you'll learn how to use sccache to optimize Rust build speed. During this process, you'll learn how to configure sccache for different scenarios, integrate sccache with Cargo, measure and optimize build performance, and use caching in continuous integration (CI) environments.

## Understanding the Rust Build Process

Before getting started with the tutorial, it's important to understand how the Rust compiler works and identify factors that can impact the speed of Rust builds.

Like most compilers, the Rust compiler lexes and parses Rust code, optimizes it, and then emits machine code. It also has an incremental compilation model, meaning it only recompiles the parts of the code that have changed since the last build. This can speed up the build process by avoiding unnecessary work.

The Rust compiler also has to deal with various factors that can slow down the build process, including the following:

- **Large codebases:** Rust projects can grow in size and complexity over time, which means that the compiler has to process more files and dependencies.
- **Complex dependencies:** Rust projects can depend on external libraries or crates, which can introduce additional compilation steps and increase the build time.
- **Debug information:** Rust projects can generate debug information, increasing the size of the output files and the compilation time.
- **Optimization levels:** Rust projects can use different optimization levels for different build profiles, such as debug or release. Higher optimization levels can improve the output binaries' performance but also increase the compilation time.

One way to improve Rust's build speed is to use [caching](https://doc.rust-lang.org/cargo/guide/build-cache.html). Caching is a technique that stores the output of a computation and reuses it for future requests. It can reduce the amount of work that the compiler has to do by reusing the previously compiled artifacts.

sccache implements caching for Rust compilation. It works by intercepting the calls to the Rust compiler and checking if the input files have been cached before. If the input files have been cached, sccache returns the cached output instead of invoking the compiler. If the input files have not been cached, sccache invokes the compiler, builds the code, and stores the output so it can be reused later.

sccache can also distribute the cache across multiple machines, which can improve the scalability and availability of the cache. sccache supports numerous storage backends for the cache, including local disk, [Amazon S3](https://aws.amazon.com/pm/serv-s3/), [Google Cloud Storage](https://cloud.google.com/storage) (GCS), [Redis](https://redis.com/redis-for-dummies/), and [memcached](https://memcached.org/).

## Using sccache to Improve Rust Build Speed

Now that you have a basic understanding of the Rust build process and the role of caching, it's time to learn how to use sccache to optimize Rust build speed.

### Installing and Configuring `sccache`

The first thing you need to do is install sccache on your machine. You can download [prebuilt binaries](https://github.com/mozilla/sccache/releases) from the GitHub release page or use [Cargo](https://doc.rust-lang.org/cargo/commands/cargo-install.html), the Rust package manager, to install it from [crates.io](https://crates.io/):

~~~{.bash caption=">_"}
cargo install sccache
~~~

The best configuration for sccache depends on your use case and preferences. For example, you can choose to store cached builds locally or in the cloud, and you can change the maximum size of the cache. Every choice has trade-offs; cloud cache storage makes it easy to share cached build artifacts with other developers, but it's slower than builds cached locally. Similarly, using a large cache reduces the chance you'll rebuild packages unnecessarily but also uses more disk space.

Since the optimal configuration depends on your situation, it's difficult to give prescriptive advice on how you should configure sccache. However, some general recommendations are:

- If multiple machines need to share the cache, use a distributed cache backend, such as Amazon S3 or GCS. This can improve the cache hit rate and reduce network latency.
- Use a local cache directory that has enough disk space and fast read/write speeds. This can improve the cache performance and avoid cache evictions.
- Use a reasonable cache size that balances the trade-off between cache efficiency and disk usage. A larger cache size can store more artifacts and increase the cache hit rate, but it can also consume more disk space and increase the cache maintenance cost.

You can use the `sccache --show-config` command to display the current configuration of sccache.

### Integrating `sccache` With Cargo

After installing and configuring sccache, the next step is to integrate it with Cargo. Cargo is the tool that manages dependencies and builds, tests, and runs Rust projects.

To use sccache with Cargo, you need to set the `RUSTC_WRAPPER` environment variable to point to the sccache executable. This tells Cargo to use sccache as a wrapper for the Rust compiler. You can do this by running the following command in your terminal:

~~~{.bash caption=">_"}
export RUSTC_WRAPPER=sccache
~~~

Alternatively, you can use a tool like [`direnv`](https://direnv.net/) to automatically set the environment variable for your project directory.

Once you set the `RUSTC_WRAPPER` environment variable, you can use Cargo commands as usual, and sccache will automatically cache the compilation output. For example, run the following command to build your project:

~~~{.bash caption=">_"}
cargo build
~~~

The first time you run this command, sccache will invoke the Rust compiler and store the output in the cache. The next time you run the command, sccache will check the cache and return the cached output if it exists. This can significantly reduce the build time, especially for large and complex projects.

You can also use sccache with other Cargo commands, such as `cargo test`, `cargo run`, and `cargo bench`. sccache will cache the output of these commands as well, as long as they involve compilation.

Additionally, you can use sccache with different build scenarios, including the following:

- **Clean builds** are builds that start from scratch, without any existing artifacts. They're useful for testing the correctness and performance of your code. To perform a clean build, you can use the `cargo clean` command to remove the existing artifacts, and then use the `cargo build` command to rebuild your project. sccache will cache the output of the clean build and reuse it for future builds.
- **Debug builds** generate additional information for debugging purposes. They're useful for finding and fixing bugs in your code. To perform a debug build, you can use the `cargo build` command without any additional flags. sccache will cache the debug build and reuse it during future builds.
- **Release builds** generate optimized binaries for use in production. Release builds are useful for deploying your code to end users. To perform a release build, you can use the `cargo build --release` command. sccache will cache the output of the release build and reuse it for future builds.

You can also use Cargo features like [parallel compilation](https://blog.rust-lang.org/2023/11/09/parallel-rustc.html) and [build profiles](https://doc.rust-lang.org/cargo/reference/profiles.html) with sccache. Parallel compilation allows you to use multiple threads to compile your code, speeding up the build process. In contrast, build profiles let you customize the optimization level, debug information, and overflow checks for different build scenarios. Then, you can use the `cargo.toml` file to configure these features for your project.

### Measuring and Optimizing Build Performance

Another important step to optimizing Rust build speed is to measure build performance and then use this data to optimize build times. Measuring build performance can help you identify and address any performance bottlenecks in your compilation process and configuration.

There are many tools that you can use to measure and optimize Rust build performance, including the following:

- [`cargo-duplicates`](https://crates.io/crates/cargo-duplicates) analyzes the dependency graph of your project and reports any duplicate dependencies that can slow down the build process.
- [`time`](https://man7.org/linux/man-pages/man1/time.1.html) is a command line utility included with every Unix and Linux system that measures the execution time of a command. You can use it to measure the build time of your project and compare the results with and without sccache. You can also use `time` to measure the build time of different build scenarios, such as clean, debug, and release builds.
- [`cargo-bloat`](https://github.com/RazrFalcon/cargo-bloat) analyzes the size of the output binaries and reports the sources of bloat. You can use this tool to find and reduce the size of the output binaries, which usually improves compilation time.

Beyond these tools, there are other things you can do to optimize Rust build performance, including the following:

- **Use stable Rust versions:** Stable Rust versions are official releases of the Rust language that are tested and supported by the Rust team. Using stable Rust versions can ensure you're not using an outdated or beta compiler with performance issues.
- **Avoid unnecessary dependencies:** Dependencies introduce additional compilation steps and increase overall build time.
- **Consider using the `--no-default-features` flag when adding dependencies to your project:** This flag can disable the optional features that you don't need.

### CI Caching and Improving on sccache

In addition to caching local builds, caching can also be useful in CI environments where you need to build and test your code frequently and reliably. Caching in CI environments can reduce the build time and resource consumption, which can improve the productivity and quality of your code.

However, caching in CI environments with `sccache` can also be challenging, as CI environments are often ephemeral and distributed, meaning the cache needs to be stored and accessed across multiple machines and sessions.

One way to use sccache in CI environments is to use a distributed cache backend, such as Amazon S3 or GCS. This tactic lets you share the cache across multiple CI machines and sessions and leverage the scalability and availability of cloud storage services. However, it can also introduce some limitations and challenges, such as:

- **Network latency:** Using a distributed cache backend can incur network latency, affecting the cache performance and reliability. That means you should choose a cache backend close to your CI environment with a fast and stable network connection.
- **Cache invalidation:** A distributed cache backend can also introduce cache invalidation issues that affect cache correctness and consistency. Cache invalidation is the process of removing outdated or invalid cache entries from the cache. Various factors (such as code changes, compiler updates, and configuration changes) can trigger cache invalidation. sccache supports both cache invalidation and expiration policies, and you can use the `sccache --clear` command to clear the cache manually when necessary.
- **Cache security:** Using a distributed cache backend can also introduce cache security issues if the cache is not protected from unauthorized access and modification. You should use a cache backend that supports cache encryption and authentication and use the `sccache --show-stats` command to monitor the cache usage and activity.

## Limitations

While sccache significantly accelerates Rust compilation by caching output artifacts, it's important to recognize its limitations, especially in CI environments. One notable challenge is network overhead. When using sccache with distributed cache backends, such as Amazon S3 or Google Cloud Storage, CI builds can experience latency due to the time required to upload and download cache artifacts. This network overhead can diminish the time savings provided by caching, especially for incremental builds that generate many small, often unique artifacts.

Another limitation is that while sccache works well for caching complete compilations, incremental compilation in Rust generates many small, often unique artifacts that change with almost every compilation. This characteristic can limit the effectiveness of sccache for caching these artifacts because the cache hit rate may be lower than for complete compilations. In other words, the nature of incremental compilation—where small parts of the code are compiled separately—may not align well with sccache's approach, which is more beneficial for caching results of more substantial and less frequently changing compilation units.

### A New Approach: `lib/rust`

Recognizing the limitations of sccache, Earthly has developed an alternative solution [`lib/rust`](https://github.com/earthly/lib/tree/main/rust). This approach, particularly useful in CI environments, leverages Rust's incremental compilation feature, offering a more efficient caching mechanism.

[`lib/rust`](https://github.com/earthly/lib/tree/main/rust) optimizes CI build times by utilizing incremental compilation and more efficient caching strategies. It significantly reduces Rust build times, making it an invaluable tool for Rust developers.

| Feature               | sccache                                       | [`lib/rust`](https://github.com/earthly/lib/tree/main/rust)       |
|-----------------------|-----------------------------------------------|------------------------------------------------------------------|
| CI Build Time         | Reduced, but impacted by network overhead     | Significantly reduced, with minimal network overhead             |
| Incremental Compilation| Not well supported                           | Fully supported, optimizing incremental builds                   |
| Setup Complexity      | Moderate                                      | Simplified, with straightforward integration into CI pipelines   |
| Network Overhead      | Can be significant, especially with distributed caches | Minimized by using local caches and persistent build runners  |

## Conclusion

In this tutorial, you learned how to use sccache to optimize Rust build speed. You learned about the Rust build process and how to configure sccache for different scenarios.

While sccache has been a valuable tool for Rust developers, the advent of `lib/rust` offers new possibilities for optimizing CI build times. We recommend exploring `lib/rust` for your projects and welcome any feedback from those who have experience with either tool. The Rust community thrives on collaboration, and your insights can help others make informed decisions about these tools.

For more information on getting started with `lib/rust`, check-out [Incremental Rust builds in CI
](https://earthly.dev/blog/incremental-rust-builds/) and our [Earthly for Rust Resources](https://earthly.dev/rust).

{% include_html cta/bottom-cta.html %}
