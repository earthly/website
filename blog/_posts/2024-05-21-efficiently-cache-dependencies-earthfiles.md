---
title: "How To Efficiently Cache Dependencies in Earthfiles"
slug: efficiently-cache-dependencies-earthfiles
categories:
  - news
toc: true
author: Gavin
topcta: false

internal-links:
 - how to efficiently cache dependencies in earthfiles
 - efficiently cache dependencies
 - efficiently cache dependencies in earthfiles
 - how to cache dependencies
---

One piece of consistent feedback we get from Earthly users is that the caching benefits are real. Users love that Earthly starts caching parts of their build automatically. You don't have to do anything to get it to work, and that will always be the case.

But you don't have to stop there. Optimizing the structure of your Earthfile can often improve baseline caching and increase speed even more. To do this effectively, it's essential to understand how caching works in Earthly.

Most commands in an Earthfile create a cache layer as part of execution. Each target in an Earthfile is similar to a cake with multiple layers, each new command is a new layer on the top of the cake that is cached for reuse.

When a target is executed a subsequent time, Earthly will attempt to reuse as much of the cached "cake" as possible. Starting from the bottom of the "cake", each cached layer will be reused unless the command's input has changed – input being ARG values, files being COPY'd, or the command itself. Earthly will work its way up the cached layers of the "cake" until it runs into a command with input that has changed – a cache bust. At that point, it will execute that command and every command for the layers in the "cake" above it.

The more of the cached "cake" we can reuse, the faster our builds get. We want to ensure that, if there's a cache bust and a command must be executed again, it happens after as much execution as possible, generally as late in a build as possible. Because of this, how you structure your Earthfile can significantly impact your build speed.

## Structuring Earthfiles to Efficiently Cache Dependencies

![Structure]({{site.images}}{{page.slug}}/structure.png)\

### Copying Files into the Build Context as Late as Possible

Let's say you have a simple Go application with three files:  `go.mod`, `go.sum`, and `main.go`. In this example, the `go.mod` and `go.sum` files are updated locally by running `go mod tidy`.

#### `go.mod`

~~~{.go caption=""}
module github.com/earthly/earthly/examples/go

go 1.22

require github.com/sirupsen/logrus v1.9.3

require golang.org/x/sys v0.0.0-20220715151400-c0bba94af5f8 // indirect
~~~

#### `go.sum`

~~~{.go caption=""}

github.com/davecgh/go-spew v1.1.0/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/davecgh/go-spew v1.1.1 h1:vj9j/u1bqnvCEfJOwUhtlOARqs3+rkHYY13jYWTU97c=
github.com/davecgh/go-spew v1.1.1/go.mod h1:J7Y8YcW2NihsgmVo/mv3lAwl/skON4iLHjSsI+c5H38=
github.com/pmezard/go-difflib v1.0.0 h1:4DBwDE0NGyQoBHbLQYPwSUPoCMWR5BEzIk/f1lZbAQM=
github.com/pmezard/go-difflib v1.0.0/go.mod h1:iKH77koFhYxTK1pcRnkKkqfTogsbg7gZNVY4sRDYZ/4=
github.com/sirupsen/logrus v1.9.3 h1:dueUQJ1C2q9oE3F7wvmSGAaVtTmUizReu6fjN8uqzbQ=
github.com/sirupsen/logrus v1.9.3/go.mod h1:naHLuLoDiP4jHNo9R0sCBMtWGeIprob74mVsIT4qYEQ=
github.com/stretchr/objx v0.1.0/go.mod h1:HFkY916IF+rwdDfMAkV7OtwuqBVzrE8GR6GFx+wExME=
github.com/stretchr/testify v1.7.0 h1:nwc3DEeHmmLAfoZucVR881uASk0Mfjw8xYJ99tb5CcY=
github.com/stretchr/testify v1.7.0/go.mod h1:6Fq8oRcR53rry900zMqJjRRixrwX3KX962/h/Wwjteg=
golang.org/x/sys v0.0.0-20220715151400-c0bba94af5f8 h1:0A+M6Uqn+Eje4kHMK80dtF3JCXC4ykBgQG4Fe06QRhQ=
golang.org/x/sys v0.0.0-20220715151400-c0bba94af5f8/go.mod h1:oPkhp1MJrh7nUepCBck5+mAzfO9JrbApNNgaTdGDITg=
gopkg.in/check.v1 v0.0.0-20161208181325-20d25e280405/go.mod h1:Co6ibVJAznAaIkqp8huTwlJQCZ016jof/cbN4VW5Yz0=
gopkg.in/yaml.v3 v3.0.0-20200313102051-9f266ea9e77c h1:dUUwHk2QECo/6vqA44rthZ8ie2QXMNeKRTHCNY2nXvo=
gopkg.in/yaml.v3 v3.0.0-20200313102051-9f266ea9e77c/go.mod h1:K4uyk7z7BCEPqu6E+C64Yfv1cQ7kz7rIZviUmN+EgEM=
~~~

#### `main.go`

~~~{.go caption="main.go"}
package main

import "github.com/sirupsen/logrus"

func main() {
    logrus.Info("hello world")
}
~~~

It would make sense to add an Earthfile like the one below for your build. It has one build target, `+build`, that copies in the required source code, installs dependencies, and builds the application; and another build target, `+docker` that uses the built application from the previous build target and creates a Docker image with it.

#### Earthfile

~~~{.dockerfile caption="Earthfile"}
VERSION 0.8
FROM golang:1.22-alpine3.19
WORKDIR /app

build:
    COPY go.mod go.sum main.go .
    RUN go build -o output/example main.go
    SAVE ARTIFACT output/example AS LOCAL local-output/example

docker:
    COPY +build/example .
    ENTRYPOINT ["/app/example"]
    SAVE IMAGE go-example:latest
~~~

This works, but it isn't using Earthly's caching as efficiently as it could be. The first step `COPY go.mod go.sum main.go .` copies in all three files at once. If any of these files change, the whole `COPY` command and everything following it has to be re-executed.

Instead, break up the files that you are copying into your build instead of copying them all in at once. Try to move each one, but especially ones that are frequently changed, as far down your Earthfile as you can.

#### Earthfile

~~~{.dockerfile caption="Earthfile"}
VERSION 0.8
FROM golang:1.22-alpine3.19
WORKDIR /app

build:
    # Download deps before copying code.
    COPY go.mod go.sum .
    RUN go mod download
    # Copy and build code.
    COPY main.go .
    RUN go build -o output/example main.go
    SAVE ARTIFACT output/example AS LOCAL local-output/example

docker:
    COPY +build/example .
    ENTRYPOINT ["/app/example"]
    SAVE IMAGE go-example:latest
~~~

This change makes it so the infrequently changed `go.mod` and `go.sum` files are copied, and `go mod download` is executed, downloading the dependencies for the build. Then, the more frequently changed `main.go` is copied and the build command is executed.

In the previous Earthfile, dependencies would be re-downloaded every time `main.go` (or `go.mod` or `go.sum`) changed, underutilizing Earthly's caching. With this new Earthfile, dependencies are only re-downloaded if `go.mod` and `go.sum` change. Otherwise, they are pulled from Earthly's cache.

### Reusing Dependencies

You may want to do more with your Earthfiles than just build the application and create a Docker image though. You may want to run a preview of the application (which we'll cover in this example) or run tests against a build before the image is published. In these cases, reusing cached dependencies can decrease build times as well.

#### Earthfile

~~~{.dockerfile caption="Earthfile"}
VERSION 0.8
FROM golang:1.22-alpine3.19
WORKDIR /app

deps:
    # Download deps
    COPY go.mod go.sum .
    RUN go mod download

preview:
    FROM +deps
    # Copy and run code.
    COPY main.go .
    RUN go run main.go

build:
    FROM +deps
    # Copy and build code.
    COPY main.go .
    RUN go build -o output/example main.go
    SAVE ARTIFACT output/example AS LOCAL local-output/example

docker:
    COPY +build/example .
    ENTRYPOINT ["/app/example"]
    SAVE IMAGE go-example:latest
~~~

In this example, both the `+preview` and `+build` targets are using the `+deps` target as a base. So if the `+deps` target is cached, both `+preview` and `+build` targets will reuse the cached results whenever either is run.

In addition to more efficiently reusing the cache, this is also a good example of making your Earthfiles more modular. Downloading dependencies is a discrete unit of work, separate from running a preview or building the application. It's required for both, so it's often lumped in with each. This example breaks off the discrete unit of work that is downloading dependencies and puts it in its own build target so that its code and logic can be reused, in the `+preview` and `+build` targets in this example.

## Earthly Makes Your Builds Fast

Structuring your Earthfiles appropriately is just the tip of the iceberg when it comes to Earthly's making your builds fast. Aside from having efficient layer caching, you can dive into using [cache mounts](https://docs.earthly.dev/docs/caching/caching-in-earthfiles#id-2.-cache-mounts), which are particularly useful if you're using a build tool that offers incremental builds. Or you can [sign up for Earthly Cloud](https://cloud.earthly.dev/login) and start using [auto-skip](https://docs.earthly.dev/docs/caching/caching-in-earthfiles#id-3.-auto-skip) to squeeze even more speed out of your builds. Or you can start using [Earthly Satellites](https://earthly.dev/earthfile/satellites) to speed up your CI builds. Earthly offers a lot of ways to make your builds faster.

{% include_html cta/bottom-cta.html %}
