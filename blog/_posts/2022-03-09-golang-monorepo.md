---
title: "Building a Monorepo in Golang"
toc: true 
author: Brandon
sidebar:
  nav: monorepos

internal-links:
 - mono repo
 - monorepo
topic: monorepo
funnel: 2
excerpt: |
    Learn how to successfully build a monorepo in Go, where each module independently manages its own build, test, and release cycles. Discover the benefits of using a monorepo and how to import local Go modules. Plus, explore efficient caching and versioning strategies for monorepo builds.
last_modified_at: 2023-07-11
categories:
  - build
---
**This article discusses the management of Go monorepos. Earthly simplifies the build process for each module within a monorepo. [Check it out](https://cloud.earthly.dev/login/).**

<!-- markdownlint-disable MD036 -->
A repository in Go traditionally contains a single Go Module, which lends naturally to a polyrepo setup – but
what if you try to build multiple Golang projects in a single monorepo?

It sounds simple enough, but there are actually a few tricks required to get a multi-module monorepo working smoothly.

In this article, I demonstrate how to successfully build a monorepo in Go, where each
module independently (and efficiently!) manages its own build, test, and release cycles.

## Why Build in a Monorepo?

Whether to build your Go projects in a [monorepo or polyrepo](/blog/monorepo-vs-polyrepo/)
may depend on your organization and personal preferences.
<!-- vale HouseStyle.OxfordComma = NO -->
I find a monorepo especially appealing when working with a small team, where a few developers collectively maintain
multiple software projects. In large organizations, however, where many teams independently maintain their own projects,
I can see how a polyrepo setup could be more comfortable and empower teams to work more autonomously. It isn't always
the case though, as large organizations like Google, Facebook and Twitter
[have been known](https://en.wikipedia.org/wiki/Monorepo) to employ very large monorepos successfully.

[Love them](https://medium.com/@adamhjk/monorepo-please-do-3657e08a4b70)
or [hate them](https://medium.com/@mattklein123/monorepos-please-dont-e9a279be011b),
there are can be some benefits to using a monorepo to develop your projects.

Based on my own experiences, these are some potential pros and cons you may want to consider when deciding on a
monorepo.

**Pros:**

- Easier to integrate changes across multiple projects at once in a monorepo
- Code reviews are in one place, and the scope of code the team owns is easy to comprehend
- Easy to share knowledge, code (e.g. libraries), and keep a consistent style across projects

**Cons:**

- build tooling can be more complicated in a monorepo
- It can be easy to accidentally tightly-couple components that should be decoupled
- Components may be less autonomous, and developers may have less freedom to do things "their own way"

We'll try our best to address some of these potential downsides in a Go monorepo in the rest of the article.

## What Does a Monorepo Layout Look Like in Golang?

A monorepo may contain multiple components, such as applications and libraries. Let's consider how we might organize
those components as distinct Go modules.

As a simple example, we'll consider a monorepo that has two backend Microservices and a single shared Library.

Our monorepo will have the following structure, with a total of three distinct Go modules.

~~~{.bash caption=">_"}
├── libs
│   └── hello
│       ├── go.mod
│       └── main.go
└── services
    ├── one
    │   ├── go.mod
    │   └── main.go
    └── two
        ├── go.mod
        └── main.go
~~~

To keep our example simple, we'll create a single REST endpoint in each of `services/one` and `services/two`.
We'll also have both of the microservices use a shared "Hello World" library in `libs/hello`.

> **Note:** Following good Microservice design principles, we should strive for
> [loose coupling](https://microservices.io/microservices/2021/01/04/loosely-coupled-services.html) in our
> `services`. In a real-world scenario, the services may have separate
> [bounded-contexts](https://martinfowler.com/bliki/BoundedContext.html) and business logic. In our monorepo,
> service code is internal to each service, and shared code is made explicitly (and carefully) via packages in the
> `libs` directory.

Below is all the code so far in our monorepo example.

### Service One

~~~{.go caption="services/one/main.go"}
package main

import (
  "net/http"

  "github.com/earthly/earthly/examples/go-monorepo/libs/hello"
  "github.com/labstack/echo/v4"
)

func main() {
  e := echo.New()
  e.GET("/one/hello", func(c echo.Context) error {
    return c.String(http.StatusOK, hello.Greet("World"))
  })
  _ = e.Start(":8080")
}
~~~

### Service Two

~~~{.go caption="services/two/main.go"}
package main

import (
  "net/http"

  "github.com/earthly/earthly/examples/go-monorepo/libs/hello"
  "github.com/labstack/echo/v4"
)

func main() {
  e := echo.New()
  e.GET("/two/hello", func(c echo.Context) error {
    return c.String(http.StatusOK, hello.Greet("Friend"))
  })
  _ = e.Start(":8080")
}
~~~

### Hello Library

~~~{.go caption="libs/hello/hello.go"}
package hello

import (
  "fmt"
)

func Greet(audience string) string {
  return fmt.Sprintf("Hello, %s!", audience)
}
~~~

## Importing Local Go Modules in a Monorepo

In the example above, both Service One and Service Two import the "Hello" Library, which is a local module
inside the same repository.

Typically, a [module's path](https://go.dev/ref/mod?id=go-work-file-replace#module-path) specifies a location in
a different repository and Go will attempt to find a requested module over the network via an HTTP request.

In our case, however, we would like to import our module locally instead. This can be achieved using the ["replace"
feature](https://go.dev/ref/mod?id=go-work-file-replace#go-mod-file-replace) in our `go.mod`. By doing so, we can instruct Go
to replace what would normally be a module found online, with a local module found at a relative path within the
monorepo.

Using the "replace" strategy for a local library has a few advantages:

- We can iterate faster on code changes in the library and service(s) which import it
- Allows checking-in changes to both the library and service(s) in a single commit or pull-request
- Updates to a library are immediately used and validated by the service(s) that import it

Here's how the `replace` syntax works in our example microservice:

~~~{.go caption="services/one/go.mod"}
module github.com/earthly/earthly/examples/go-monorepo/services/one

go 1.17

require (
  github.com/earthly/earthly/examples/go-monorepo/libs/hello v0.0.0
  github.com/labstack/echo/v4 v4.6.3
)

replace github.com/earthly/earthly/examples/go-monorepo/libs/hello v0.0.0 => ../../libs/hello
~~~

Using the strategy above, we're now able to compile Service One and Service Two in our example, as well as develop and
run our unit tests.

> **VSCode Users:** By default, Visual Studio may give you errors when opening an entire Go monorepo project as a
> workspace. Those issues can usually be resolved by adding the following experimental feature flag to your settings:

~~~{.json caption=".vscode/settings.json"}
{
    "gopls": {
        "experimentalWorkspaceModule": true
    }
}
~~~

## Build Tooling for a Monorepo in Go

Now that we have our monorepo running locally, the next step might be to configure a build tool to containerize
the microservices, run unit tests, end-to-end integration tests, and any other typical steps we might want as part of
a Continuous Integration pipeline.

[Earthly](https://cloud.earthly.dev/login) is a great tool for this job. It allows each service or library to independently manage
its own build and test cycles. It can also effectively utilize cache so that only the services or libraries
which have changed will re-trigger their build.

We can add an Earthfile to each of our services and libraries, as well as a parent Earthfile at the root of the monorepo.
The parent Earthfile will act as an orchestrator, calling into the more specific Earthfiles lower down in the hierarchy.

Below are the various Earthfiles used to build and test our example monorepo.

### Hello Library

Compiles itself into a self-contained artifact, which can be referenced by the other services.

~~~{.Dockerfile caption="libraries/hello/Earthfile"}
VERSION 0.6

deps:
    FROM golang:1.17-alpine
    WORKDIR /libs/hello
    COPY go.mod go.sum ./
    RUN go mod download

artifact:
    FROM +deps
    COPY hello.go .
    SAVE ARTIFACT .

unit-test:
    FROM +artifact
    COPY hello_test.go .
    RUN go test
~~~

### Service One

Uses the Hello library as an artifact and configures its own build and test steps.
Service Two looks basically the same, so I've left it out.

~~~{.Dockerfile caption="services/one/Earthfile"}
VERSION 0.6

deps:
    FROM golang:1.17-alpine
    WORKDIR /services/one
    COPY ../../libs/hello+artifact/* /libs/hello
    COPY go.mod go.sum ./
    RUN go mod download

compile:
    FROM +deps
    COPY main.go .
    RUN go build -o service-one main.go

unit-test:
    FROM +compile
    COPY main_test.go .
    RUN CGO_ENABLED=0 go test

docker:
    FROM +compile
    ENTRYPOINT ["./service-one"]
    SAVE IMAGE service-one:latest
~~~

### Parent Earthfile

Located at the root of the monorepo, the parent Earthfile can be used conveniently by developers or a CI pipeline.

~~~{.Dockerfile caption="/Earthfile"}
VERSION 0.6

all-unit-test:
    BUILD ./libs/hello+unit-test
    BUILD ./services/one+unit-test
    BUILD ./services/two+unit-test

all-docker:
    BUILD ./services/one+docker
    BUILD ./services/two+docker
~~~

The entire monorepo can now be built by running `earthly +all-docker` on the command-line. Similarly, unit tests for
the entire monorepo can be run using `earthly +all-unit-test`.

### Efficient Caching in a Monorepo Build

An efficient build tool for a monorepo should not rebuild components that haven't changed, nor should it re-run tests
that aren't necessary. Earthly does this naturally in a local environment, which is super useful in speeding up
development.

It's also possible to utilize caching in a CI pipeline. On many platforms such as
[Github Actions](https://github.com/features/actions), each build is run on a fresh instance of the build environment,
so Earthly loses its cache history from previous runs.
[Shared caching](https://docs.earthly.dev/docs/caching/caching-via-registry), however, can be used to improve this.

Note that shared cache does require upload and download steps to sync the cache during each CI run, so it does have a
cost. It can yield a nice performance boost though for compute-heavy steps, such as long-running integration tests
which do not always need to be re-run.

### Releasing and Versioning Microservices in a Monorepo

Another interesting difference when building Go Modules in Monorepo is versioning, since typically a repo contains a
single module, with semantic version numbers specified as Git Tags. For monorepos, we may have a couple of options.

In the example monorepo above, libraries are used via the `replace` syntax in `go.mod`. Hence, they are only used
within the context of the monorepo, and all consumers of the library are always getting the current copy via local
import. We can say that publishing versions of those libraries are not relevant.

For the microservices in our monorepo, on the other hand, versioning may be more important. The microservices are
eventually deployed as containers, and different versions of those containers may need to be available for deployment
at any given time. We also may wish to communicate the scope of changes through semantic version numbers to any
consumers of those microservices.

Our options are to either version the entire monorepo together using Git Tags, or declare the versions for each
microservice elsewhere. I prefer the latter, since versioning all microservices at once may falsely communicate a
change in a service where there may have been none.

One way we can version microservices in a monorepo is to store the version as a file within each service, then publish
the resulting image from our build with a tag based on that version file.

Here's an example of doing that in a new `+release` target in our microservice build, using the open source
[`semver-cli`](https://github.com/maykonlf/semver-cli) tool.

~~~{.Dockerfile caption="services/one/Earthfile"}
release-tag:
    FROM golang:1.17-alpine
    RUN go install github.com/maykonlf/semver-cli/cmd/semver@v1.0.2
    COPY .semver.yaml .
    RUN semver get release > version
    SAVE ARTIFACT version

release:
    FROM +docker
    COPY +release-tag/version .
    ARG VERSION="$(cat version)"
    SAVE IMAGE --push service-one:$VERSION
~~~

## Conclusion

Building a multi-module monorepo in Go is made possible and effective using the `replace` feature in `go.mod` to
import local modules. In a monorepo environment, using the right build tooling can also make development and
Continuous Integration more efficient.

You can find the full working monorepo covered in this article in the official
[Earthly examples collection](https://github.com/earthly/earthly/tree/main/examples/go-monorepo).

For more on using Earthly to improve Go builds checkout [Earthly.dev](https://cloud.earthly.dev/login):

{% include_html cta/bottom-cta.html %}
