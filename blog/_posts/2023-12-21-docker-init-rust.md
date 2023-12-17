---
title: "Using Docker Init in Rust"
categories:
  - Tutorials
toc: true
author: Ikeh Akinyemi

internal-links:
 - just an example
excerpt: |
    This markdown content provides a checklist for writing and publishing an article, including steps such as outlining, drafting, proofreading, creating a header image, and adding internal links. It also includes a checklist for optimizing an article for external publication, including adding an author page, optimizing images, and incorporating external links.
---


[Docker](https://www.docker.com/) has consistently evolved to meet the needs of developers, and the [Docker Init](https://docs.docker.com/engine/reference/commandline/init/) plugin is one of its recent additions. It simplifies the process of setting up Docker-related files for projects, eliminating the need to start from scratch.

In this tutorial, you'll learn how `docker init` can be used with Rust, a language known for its performance and safety. If you're looking to leverage Docker for containerization, this article will show you how `docker init` can be an invaluable tool for quickly bootstrapping projects and ensuring a stable and efficient development environment.

## What Is Docker Init?

`docker init` is a command line utility that enhances the user experience, especially for developers working with languages like Rust.

Before its introduction, the initial setup of a Docker environment for a project was a manual and meticulous task. Developers had to write a Dockerfile from scratch, specifying each instruction to build the image, as well as a `docker-compose.yaml` file to define how the containerized application should run. This process was not only time-consuming but fraught with the potential for errors. A misplaced command or an incorrect image tag could derail the entire containerization effort.

For example, before `docker init`, developers would have to manually write Dockerfiles like this, which required an understanding of both Docker and Rust's compilation process:

~~~
# Use the official Rust image as a base
FROM rust:1.58 as builder

# Create a new empty shell project
RUN USER=root cargo new --bin myapp
WORKDIR /myapp

# Copy your manifests
COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml

# Build only the dependencies to cache them
RUN cargo build --release
RUN rm src/*.rs

# Now that the dependencies are built, copy your source code
COPY ./src ./src

# Build for release
RUN rm ./target/release/deps/myapp*
RUN cargo build --release

# Final base
FROM debian:buster-slim

# Copy the build artifact from the build stage
COPY --from=builder /myapp/target/release/myapp .

# Set the startup command to run your binary
CMD ["./myapp"]
~~~

This Dockerfile demonstrates a multistage build, which is an advanced Docker concept. It first creates a build environment, compiles the Rust application, and then creates a lean final image by copying over the compiled binary. This approach minimizes the final image size, which is crucial for deployment efficiency, but setting it up manually can be time-consuming and repetitive, especially if you're working with multiple images.

`docker init` simplifies this setup by automatically generating three crucial files: `Dockerfile`, `compose.yaml`, and `.dockerignore`. This automation is particularly helpful to those who may not be deeply familiar with Docker's best practices or the nuances of containerization. It ensures that the project is set up efficiently and securely and minimizes the risk of mistakes. Additionally, the Docker Compose file is set up to ensure that your application runs smoothly in a local development environment, mirroring the conditions it will face in production.

The command syntax for `docker init` is straightforward:

~~~
docker init [OPTIONS]
~~~

When executed, `docker init` prompts you to select the type of application you're working on. Once you select Rust and specify the version and your port number, the command produces `Dockerfile`, `compose.yaml`, and `.dockerignore` files that are functional and that adhere to best practices for Rust applications.

To see the current options available for the `docker init` command, you can run `docker init --help` in your terminal. This command displays the most up-to-date list of options and their descriptions. At the time of writing, the primary option available is `--version`, which reveals the version number of the Docker Init plugin.

The use cases for `docker init` are numerous. It allows developers to quickly set up a consistent Docker environment for any Rust project, whether it's a simple CLI tool or a complex web service. It's also helpful in continuous integration (CI) pipelines, where build speed and reliability are critical.

For any existing open source Rust projects that lack or are yet to adopt containerization, `docker init` offers a significant advantage. It automates the process of creating Dockerfile and Docker Compose files, thus removing the need to manually comb through the repository to identify essential configurations like ports or environment variables. This makes setting up containerized environments for contributors much easier and faster.

## Using Docker Init With Rust

Now that you know a little more about `docker init`, it's time to see it in action. In this section, you'll learn how to use `docker init` to set up a Rust project. All the code for this tutorial is available in [this GitHub repo](https://github.com/Ikeh-Akinyemi/earthly-docker-init).

### Initialize a Rust Project

Navigate to the root directory of your Rust project in the terminal. If you haven't yet created a directory for your project, you can run `mkdir <project-name>` and then `cd <project-name>`.

Once you've created your root directory, run the following command:

~~~
docker init
~~~

This command kicks off the initialization process. It prompts you to select the type of application you're working on; choose Rust. Then, `docker init` generates configuration files tailored for a Rust environment. This step is crucial, as it lays down the Docker framework for your project and ensures that the containerization is optimized for Rust's ecosystem:

~~~
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - dockerignore
  - Dockertile
  - compose-yaml

Let's get started!

? What application platform does your project use? Rust
? What version of Rust do you want to use? 1.73.0
? What port does your server listen on? 8080

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

WARNING: Cargo.lock was not found but is required to run your application. You can create it by running cargo generate-lockfile

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8080
~~~

### The Generated Files

After running `docker init` and selecting Rust, the following files are typically created: `Dockerfile`, `compose.yaml`, and `.dockerignore`.

#### Dockerfile

`Dockerfile` contains the instructions Docker uses to build the image for your Rust application:

~~~
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

################################################################################
# Create a stage for building the application.

ARG RUST_VERSION=1.73.0
ARG APP_NAME=
FROM rust:${RUST_VERSION}-slim-bullseye AS build
ARG APP_NAME
WORKDIR /app

# Build the application.
# Leverage a cache mount to /usr/local/cargo/registry/
# for downloaded dependencies and a cache mount to /app/target/ for 
# compiled dependencies which will speed up subsequent builds.
# Leverage a bind mount to the src directory to avoid having to copy the
# source code into the container. Once built, copy the executable to an
# output directory before the cache mounted /app/target is unmounted.
RUN --mount=type=bind,source=src,target=src \
    --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    <<EOF
set -e
cargo build --locked --release
cp ./target/release/$APP_NAME /bin/server
EOF

################################################################################
# Create a new stage for running the application that contains the minimal
# runtime dependencies for the application. This often uses a different base
# image from the build stage where the necessary files are copied from the build
# stage.
#
# The example below uses the debian bullseye image as the foundation for running the app.
# By specifying the "bullseye-slim" tag, it will also use whatever happens to be the
# most recent version of that tag when you build your Dockerfile. If
# reproducability is important, consider using a digest
# (e.g., debian@sha256:ac707220fbd7b67fc19b112cee8170b41a9e97f703f588b2cdbbcdcecdd8af57).
FROM debian:bullseye-slim AS final

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser

# Copy the executable from the "build" stage.
COPY --from=build /bin/server /bin/

# Expose the port that the application listens on.
EXPOSE 8080

# What the container should run when it is started.
CMD ["/bin/server"]
~~~

This `Dockerfile` template can be used to build and run Rust applications in Docker. It demonstrates best practices like using multistage builds, caching dependencies, running the application as a non-privileged user, and keeping the final image size small. The use of arguments like `ARG APP_NAME` allows for customization of the `Dockerfile` without modifying the file itself, making it reusable for different applications.

#### `compose.yaml`

`compose.yaml` defines how your Rust application runs and interacts with other services:

~~~
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker compose reference guide at
# https://docs.docker.com/compose/compose-file/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080

# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql/data
#     environment:
#       - POSTGRES_DB=example
#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
#     expose:
#       - 5432
#     healthcheck:
#       test: [ "CMD", "pg_isready" ]
#       interval: 10s
#       timeout: 5s
#       retries: 5
# volumes:
#   db-data:
# secrets:
#   db-password:
#     file: db/password.txt
~~~

This file is set up to build and run a Rust application as defined in the `Dockerfile`. It also provides a template for adding a database service, which can be customized and activated as needed.

The `compose.yaml` file is designed to be flexible and easily extendable to fit the requirements of different applications. You can simply uncomment and configure the relevant sections.

#### `.dockerignore`

`.dockerignore` includes any files or directories you wish to exclude from being copied into your container:

~~~
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/engine/reference/builder/#dockerignore-file

**/.DS_Store
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/charts
**/docker-compose*
**/compose*
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/secrets.dev.yaml
**/values.dev.yaml
/bin
/target
LICENSE
README.md
~~~

The `.dockerignore` file helps maintain project security by preventing unintended secrets and sensitive files from being included in the Docker image. Overall, this file ensures that Docker images are built efficiently and without unnecessary bloat.

All three of these files dictate how your application is built and run in a Docker container.

### Create a Basic Rust App with Dependencies

Now that you know a little more about the files that `docker init` generates, it's time to create a simple Rust application.

Consider a scenario where you have a `main.rs` file with a basic HTTP server or a command line tool. You need to ensure that your `Cargo.toml` file accurately reflects any external crates your application depends on.

In this example, you'll use `actix-web` because it performs well and is easy to use. Add `actix-web` to your `Cargo.toml` file under `[dependencies]`:

~~~
[dependencies]
actix-web = "4"
~~~

Next, it's time to write some basic code to handle CRUD operations. Open the `main.rs` file in the `src` directory and replace its contents with the following:

~~~
use actix_web::{web, App, HttpResponse, HttpServer, Responder};

async fn create_post() -> impl Responder {
    HttpResponse::Created().body("Post created")
}

async fn read_posts() -> impl Responder {
    HttpResponse::Ok().body("Here are all the posts")
}

async fn update_post() -> impl Responder {
    HttpResponse::Ok().body("Post updated")
}

async fn delete_post() -> impl Responder {
    HttpResponse::Ok().body("Post deleted")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/posts", web::post().to(create_post))
            .route("/posts", web::get().to(read_posts))
            .route("/posts/{id}", web::put().to(update_post))
            .route("/posts/{id}", web::delete().to(delete_post))
    })
    .bind("127.0.0.1:8081")?
    .run()
    .await
}
~~~

This code sets up a basic HTTP server with routes for creating, reading, updating, and deleting posts. Each route is associated with a function that, in this example, returns a simple text response.

### Modify the Docker Files

Review the generated `Dockerfile` and `compose.yaml` files. You may need to tweak them to suit your project's specific requirements, such as adding environment variables, exposing additional ports, or defining volume mounts.

For instance, you can update the `Dockerfile` and `compose.yaml` files to use port 8081 instead of port 8080. Additionally, you can set `ARG APP_NAME` in `Dockerfile` to correspond with the name of your project (as specified in the `Cargo.toml` file).

Make the following changes to `Dockerfile`:

~~~
...
ARG APP_NAME=earthly-docker-init-x
...
# Expose the port that the application listens on.
EXPOSE 8081
...
~~~

Make the following change to `compose.yaml`:

~~~
...
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8081:8081
...
~~~

`docker init` provides a strong starting point, but every Rust project is unique. Modifications may be necessary to align the Docker configuration with your application's needs and ensure that when the application is containerized, it behaves as expected.

### Run the App in a Container

Finally, it's time to build and run your application by executing the following:

~~~
docker-compose up --build
~~~

This command builds the Docker image for your application using the instructions from your `Dockerfile` and then starts a container based on that image. The `--build` flag ensures that Docker rebuilds the image to include any changes you've made.

Running the app in a container—and making an HTTP request to it—is the ultimate test to confirm that your application is correctly set up to run in a Dockerized environment:

<div class="wide">
![`docker compose` command sample]({{site.images}}{{page.slug}}/emr8669.png)
</div>

Use the following curl command to make a request to the running server, like this:

~~~
curl "http://localhost:8081/posts"
Here are all the posts
~~~

You've now effectively set up a Docker environment for a Rust project using `docker init` and ensured that your application can run within a container, thus replicating a production-like environment on your local machine.

## Conclusion

`docker init` is a powerful and simple command that can be leveraged within Rust projects to streamline the process of setting up Docker environments. It not only saves time by automatically generating `Dockerfile`, `compose.yaml`, and `.dockerignore` files, but it also ensures that these configurations adhere to best practices, minimizing the potential for errors.

As you continue to develop Rust applications, the knowledge and practices outlined here will serve as a foundation for incorporating `docker init` into your development process and ensure that your focus remains on crafting quality code while Docker handles the intricacies of containerization.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva


]- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
