---
title: "Making Your Docker Builds Faster with cargo-chef"
categories:
  - Tutorials
toc: true
author: Utibeabasi Umanah

internal-links:
 - make docker builds faster
 - builds faster with cargo-chef
 - cargo-chef making docker builds faster
 - fast builds with cargo-chef
excerpt: |
    This article discusses how to make Docker builds faster for Rust applications using the cargo-chef tool. It explains the factors that contribute to slow Docker builds and demonstrates how cargo-chef's caching capabilities can improve build performance.
---
**The article focuses on enhancing Rust Docker build efficiency. Earthly streamlines Docker builds for Rust, reducing compilation times. Learn more about Earthly's capabilities for Rust Docker builds at [Earthly](https://cloud.earthly.dev/login).**

[Docker](https://www.docker.com/) is an open source platform that allows you to package applications and all their dependencies in isolated containers. This means you can easily deploy and run these containers consistently across different environments, making building, testing, and deploying applications effortless.

Docker is particularly useful when building applications with languages that compile down to a single binary, like Rust and Golang. However, building Docker images for Rust applications can take a long time because you need to install all of the dependencies with every build. Thankfully, tools like [cargo-chef](https://github.com/LukeMathWalker/cargo-chef) can help enhance build performance in Docker.

In this article, you'll learn about some of the factors contributing to slow Docker builds and how you can use cargo-chef's caching capabilities to improve build performance.

## Understanding Slow Docker Builds

Despite the many benefits Docker brings to developers, building a Docker image can be time-consuming. This is thanks to the intricacies of layer caching, where any modification to a layer or subsequent layers invalidates the cache and triggers a time-consuming rebuild.

The following are a few other factors that contribute to slow Docker build performance:

* **Large dependencies:** If your project has large dependencies, it can take longer to download and install them during the build process.
* **Inefficient caching mechanisms:** Docker uses caching to speed up builds by reusing previously built layers. However, if your Dockerfile isn't optimized to take advantage of caching, it can result in slower builds. For instance, if a layer is invalidated due to a change in the code, all subsequent layers need to be rebuilt.
* **Using large base images:** If you use a base image like [Ubuntu](https://ubuntu.com/), it might take longer to download the image and start the build. It's usually recommended to start with a lightweight base image, such as [Alpine](https://www.alpinelinux.org/).
* **Hardware constraints:** The amount of CPU and memory resources available on the host machine can contribute to the build speed. Greater availability of resources typically leads to faster build times.
* **Large build context:** The entire build context, including files and directories, is sent to the Docker daemon. The larger your build context, the longer it takes to transfer data.
* **Large images:** Large Docker images, especially those with many layers or dependencies, take longer to build and transfer.

## Why You Need `cargo-chef`

cargo-chef is a new Cargo subcommand that can be used to build the dependencies of a Rust project based on a JSON description file. cargo-chef fully leverages Docker layer caching, resulting in faster Docker builds for Rust projects.

Traditional build processes in Rust typically involve running `cargo build` or `cargo build --release` to compile the project and its dependencies from scratch (any time you build a project, all dependencies are recompiled even if they haven't changed since the last build). This can be time-consuming, especially for large projects with a lot of dependencies.

In contrast, cargo-chef analyzes the project dependencies and their configuration to create a "recipe" for building the project. This recipe includes information about the dependencies' source code and build artifacts. cargo-chef uses this recipe file to skip unnecessary steps. It checks if the dependencies and their build artifacts are still the same, and if so, it reuses the previously built artifacts, avoiding unnecessary recompilation and rebuilding of dependencies.

The `recipe.json` file is the equivalent of the Python `requirements.txt` file—it's the only input required for `cargo chef cook`, the command used to build out dependencies.

In the following sections, you'll learn how to set up cargo-chef to speed up your Docker build processes.

## Managing Your Docker Builds with `cargo-chef`

Before you begin this tutorial, you'll need:

* [Docker](https://docs.docker.com/engine/install/) installed on your operating system (version 24.0.7 is used here)
* [`rustup`](https://rustup.rs/) installed

Once rustup is installed, make sure you have the latest toolchain. You can verify that with the following command:

~~~{.bash caption=">_"}
rustup default stable
~~~

### Creating a Rust Project

Before you get started with cargo-chef, you need to create a new Rust project by running the following command:

~~~{.bash caption=">_"}
cargo new hello-world --bin
cd hello-world
~~~

Your output will look like this:

~~~{ caption="Output"}
PS C:\Users\LENOVO\Documents\docs> cargo new hello-world --bin
     Created binary (application) `hello-world` package
~~~

To create a simple web server app, you'll use the [Rocket](https://rocket.rs/) crate. Go ahead and add it as a dependency in `Cargo.toml`:

~~~{.toml caption="Cargo.toml"}
[dependencies]
rocket = "0.5.0"
~~~

Then, replace the code in `src/main.rs` with the following:

~~~{.rust caption="main.rs"}
#[macro_use] extern crate rocket;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index])
}
~~~

This creates a simple web server that returns `Hello, world!` at the `/` path.

Use `cargo run` in your terminal to run the code locally. Then, visit [http://localhost:8000](http://localhost:8000) to view the app:

<div class="wide">
![Browser output]({{site.images}}{{page.slug}}/klGuQVk.png)
</div>

### Building the Docker Image

After viewing your app, it's time to build a Docker image for your application.

Create a file called `Dockerfile` with the following code:

~~~{.Dockerfile caption="Dockerfile"}
FROM rust:latest

WORKDIR /usr/src/app

COPY Cargo.toml Cargo.lock ./

RUN mkdir src

COPY src/ ./src/

RUN cargo build --release

EXPOSE 8000

CMD ["./target/release/hello-world"]
~~~

This is a pretty standard Rust Dockerfile that currently doesn't have any of the caching capabilities of cargo-chef.

Run the following command to try building this unoptimized image to see how long it takes:

~~~{.bash caption=">_"}
docker build -t hello-world-unoptimized .
~~~

Your output should look something like this:

~~~{ caption="Output"}
// Some output omitted
[+] Building 157.2s (11/11) FINISHED                                                                  docker:default
 => [internal] load build definition from Dockerfile                                                            0.0s
 => => transferring dockerfile: 221B                                                                            0.0s
 => [internal] load metadata for docker.io/library/rust:latest                                                  0.6s
 => [internal] load .dockerignore                                                                               0.0s
 => => transferring context: 2B 
... # Some output omitted for brevity
...
=> [internal] load build context                                                                               0.0s
 => => transferring context: 40.00kB                                                                            0.0s
 => [2/6] WORKDIR /usr/src/app                                                                                  0.5s
 => [3/6] COPY Cargo.toml Cargo.lock ./                                                                         0.0s
 => [4/6] RUN mkdir src                                                                                         0.3s
 => [5/6] COPY src/ ./src/                                                                                      0.0s
 => [6/6] RUN cargo build --release                                                                           133.2s
 => exporting to image                                                                                          2.8s 
 => => exporting layers                                                                                         2.8s 
 => => writing image sha256:1ad45f71201f8dcd910d341efc1195afc4cc60d5c2fba4dfdac33b3b360c5488                    0.0s 
 => => naming to docker.io/library/hello-world-unoptimized                                                      0.0s 
~~~

The time may vary depending on your build machine, but in this example, this code took 157.2 seconds to run.

To shorten this time, go ahead and update the code, rebuild the image, and check to see if Docker's build cache kicks in.

Change the code to say `Hello, World! from unoptimized image` and rerun the build command. Your output should look something like this:

~~~{ caption="Output"}
[+] Building 138.8s (11/11) FINISHED                                                                  docker:default
 => [internal] load build definition from Dockerfile                                                            0.0s
 => => transferring dockerfile: 221B                                                                            0.0s
 => [internal] load metadata for docker.io/library/rust:latest                                                  0.3s
 => [internal] load .dockerignore                                                                               0.0s
 => => transferring context: 2B   
... # Some output omitted for brevity
...
=> => transferring context: 307B                                                                               0.0s
 => CACHED [2/6] WORKDIR /usr/src/app                                                                           0.0s
 => CACHED [3/6] COPY Cargo.toml Cargo.lock ./                                                                  0.0s
 => CACHED [4/6] RUN mkdir src                                                                                  0.0s
 => [5/6] COPY src/ ./src/                                                                                      0.0s
 => [6/6] RUN cargo build --release                                                                           135.2s
 => exporting to image                                                                                          2.8s 
 => => exporting layers                                                                                         2.8s 
 => => writing image sha256:45a641a1dfa96df76aca67f4737a6b108798982dd70a11cd83cf3dbe48b242c1                    0.0s 
 => => naming to docker.io/library/hello-world-unoptimized                                                      0.0s
~~~

You can see that you saved a few seconds, but the majority of the build time was spent compiling the Cargo dependencies, even though they weren't updated.

### Optimizing Your Dockerfile

Now, let's use cargo-chef to optimize the build time of your image. cargo-chef is designed to be leveraged in Dockerfiles, which is the recommended mode of installation. However, it can be installed via the command line as well.

First, you'll need a Dockerfile that uses cargo-chef. To do so, replace the code in your Dockerfile with the following:

~~~{.Dockerfile caption="Dockerfile"}
FROM lukemathwalker/cargo-chef:latest-rust-1 AS chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder 
COPY --from=planner /app/recipe.json recipe.json
# Build dependencies (this is the caching Docker layer)
RUN cargo chef cook --release --recipe-path recipe.json
# Build application
COPY . .
RUN cargo build --release --bin hello-world

# You do not need the Rust toolchain to run the binary!
FROM debian:bookworm-slim AS runtime
WORKDIR /app
COPY --from=builder /app/target/release/hello-world /usr/local/bin
CMD ["/usr/local/bin/hello-world"]
~~~

In this code, you make use of the `lukemathwalker/cargo-chef` base image, which has cargo-chef preinstalled. If you want to run cargo-chef locally, you can install it by running `cargo install cargo-chef` in your terminal.

Here, you're making use of Docker multistage builds by creating the `recipe.json` file that contains all the Rust dependencies. The `builder` step runs `cargo chef cook --release --recipe-path recipe.json`, which installs all the cargo-chef dependencies.

The first time you build this image, it will take some time, but subsequent steps will be quicker since the dependencies won't change.

To build the optimized Docker image, run the following command:

~~~{.bash caption=">_"}
docker build -t hello-world-optimized .
~~~

Your output should look something like this:

~~~{ caption="Output"}
[+] Building 151.6s (17/17) FINISHED                                                                  docker:default
 => [internal] load build definition from Dockerfile                                                            0.0s
 => => transferring dockerfile: 652B                                                                            0.0s
 => [internal] load metadata for docker.io/library/debian:bookworm-slim                                         0.6s
 => [internal] load metadata for docker.io/lukemathwalker/cargo-chef:latest-rust-1                              0.6s
 => [internal] load .dockerignore                                                                               0.0s
 => => transferring context: 2B  
... # Some output omitted for brevity
...
=> [chef 2/2] WORKDIR /app                                                                                     0.1s
 => [runtime 2/3] WORKDIR /app                                                                                  0.4s
 => [planner 1/2] COPY . .                                                                                      1.8s
 => [planner 2/2] RUN cargo chef prepare --recipe-path recipe.json                                              0.3s
 => [builder 1/4] COPY --from=planner /app/recipe.json recipe.json                                              0.0s
 => [builder 2/4] RUN cargo chef cook --release --recipe-path recipe.json                                     120.7s
 => [builder 3/4] COPY . .                                                                                      1.7s 
 => [builder 4/4] RUN cargo build --release --bin hello-world                                                  17.5s 
 => [runtime 3/3] COPY --from=builder /app/target/release/hello-world /usr/local/bin                            0.1s 
 => exporting to image                                                                                          0.1s 
 => => exporting layers                                                                                         0.1s 
 => => writing image sha256:1781bd70f82b6e0993329de545af9da42341fea9079b69a2ab55d0ee9da0631c                    0.0s 
 => => naming to docker.io/library/hello-world-optimized                                                        0.0s
~~~

As you can see, this build took 187.6 seconds because you're installing the dependencies for the first time.

To make this build faster, update the code to say `Hello, World! from optimized image` and rerun the build command:

Your output should look something like this:

~~~{ caption="Output"}
[+] Building 22.9s (17/17) FINISHED                                                                   docker:default
 => [internal] load build definition from Dockerfile                                                            0.0s
 => => transferring dockerfile: 652B                                                                            0.0s
 => [internal] load metadata for docker.io/library/debian:bookworm-slim                                         0.3s
 => [internal] load metadata for docker.io/lukemathwalker/cargo-chef:latest-rust-1                              0.3s
 => [internal] load .dockerignore                                                                               0.0s
 => => transferring context: 2B      
... # Some output omitted for brevity
...
CACHED [builder 1/4] COPY --from=planner /app/recipe.json recipe.json                                       0.0s
 => CACHED [builder 2/4] RUN cargo chef cook --release --recipe-path recipe.json                                0.0s
 => [builder 3/4] COPY . .                                                                                      1.3s
 => [builder 4/4] RUN cargo build --release --bin hello-world                                                  16.3s
 => CACHED [runtime 2/3] WORKDIR /app                                                                           0.0s
 => [runtime 3/3] COPY --from=builder /app/target/release/hello-world /usr/local/bin                            0.0s
 => exporting to image                                                                                          0.1s
 => => exporting layers                                                                                         0.1s
 => => writing image sha256:c0679dc200a08c1d019b56307924e514c50da9b5dd185d7f0db88a8efd243311                    0.0s
 => => naming to docker.io/library/hello-world-optimized                                                        0.0s
~~~

As you can see, the build time decreased by 22.9 seconds!

## Optimizing `cargo-chef` Usage

Because Rust compiles down to a single binary, it's perfect for use in Dockerfiles in which you're leveraging [multistage builds](https://earthly.dev/blog/docker-multistage/) that allow you to build Docker images in stages. This is particularly useful because you can create a final Docker image that only contains the required dependencies to run the image, copied over from the previous stages. By using multistage builds with cargo-chef, you can separate the recipe computation, dependency building, and the final compilation into different stages, which helps leverage Docker's caching mechanism.

To get full efficiency from cargo-chef, you must use the same Rust version in all stages. A version mismatch will cause caching to not work as expected.

### `cargo-chef` Limitations

While the advantages of cargo-chef are noteworthy, there are still a few limitations that you should be aware of, including the following:

* `cargo cook` and `cargo build` must be executed from the same working directory. If you examine the `*.d` files under `target/debug/deps` for one of your projects using `cat`, you'll notice that they contain absolute paths referring to the project target directory. If moved around, Cargo will not leverage them as cached dependencies.
* `cargo build` builds local dependencies (outside of the current project) from scratch, even if they have not changed. This is because Cargo relies on file timestamps for fingerprinting, and copying the dependencies changes the timestamp. For more information, check out this [extensive issue on Cargo's repository](https://github.com/rust-lang/cargo/issues/2644).

## Conclusion

In this article, you learned all about Docker builds and some of the factors that contribute to a slow build, such as large dependencies, frequent code changes, and inefficient caching mechanisms. You also learned how to use Docker layer caching to accelerate builds by reusing previously built layers with cargo-chef.

[Earthly](https://earthly.dev/) allows you to leverage incremental builds to speed up your Rust builds in your CI workflow. You can read more about this on the [official Earthly blog](https://earthly.dev/blog/incremental-rust-builds/).

In this article, you've learned how Docker layer caching with cargo-chef speeds up Rust project builds. Yet, it's not perfect, especially when we dive into the CI world.

Luca Palmieri, creator of cargo-chef suggests trying out Earthly for Rust CI builds:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">They&#39;ve achieved _very_ significant speed-ups on large repositories: from ~22.5 minutes to ~2.5 minutes, on a warm cache, for the <a href="https://twitter.com/expressvpn?ref_src=twsrc%5Etfw">@expressvpn</a> repo.<br>And their cache invalidation story is as good as your local one: changing one dependency won&#39;t bust it!<a href="https://t.co/jrN0neEMJG">https://t.co/jrN0neEMJG</a></p>&mdash; Luca Palmieri (@algo_luca) <a href="https://twitter.com/algo_luca/status/1732399581605015967?ref_src=twsrc%5Etfw">December 6, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Earthly provides an innovative approach to Rust builds in CI by leveraging the same caching features that make local Rust builds fast, in combination with persistent build runners. Teams like ExpressVPN have already seen how much time it saves. And the best part? It's not rocket science. Earthly makes it easy to get those fast, efficient builds without the headache.

To learn more about how Earthly can transform your Rust CI builds and to see it in action, continue reading about [Incremental Rust builds in CI with Earthly](https://earthly.dev/blog/incremental-rust-builds/).

{% include_html cta/bottom-cta.html %}
