---
title: What is Buildkit?
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "docker"
internal-links:
   - buildkit
   - buildctl
   - buildkitd
   - runc
   - docker daemon
last_modified_at: 2022-11-17
excerpt: |
    Learn how to use BuildKit, an open-source project that turns Dockerfiles into Docker images. Discover its history, how to install it, and how to build images using BuildKit directly. Explore different output types and gain insights into the inner workings of BuildKit.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

There is an excellent open-source project that you have probably used without realizing it. It's called BuildKit, and it is what turns a Dockerfile into a Docker image. And it doesn't just build Docker images; it can build OCI images and several other output formats. [OpenFasS](https://www.openfaas.com/) uses it to turn functions into full containers, and here at Earthly, we use it to create complete continuous integration pipelines.  

You may not know you've used BuildKit because other applications wrap it. Modern versions of `docker build` can use BuildKit and it will soon be enabled by default. Today let's look at how to use BuildKit directly.

## History

> BuildKit is a new project under the Moby umbrella for building and packaging software using containers. It's a new codebase meant to replace the internals of the current build features in the Moby Engine. - [Introducing BuildKit](https://blog.mobyproject.org/introducing-buildkit-17e056cc5317)

Tõnis Tiigi, a Docker employee and BuildKit's primary developer, created BuildKit to separate the logic of building images from the main Moby project and to enable future development. BuildKit has support for pluggable frontends, which allow it to make more than just docker images using dockerfiles. With BuildKit, we can substitute the dockerfile syntax for [hlb](https://github.com/openllb/hlb) and replace the docker image format for a pure tar file output. That is just one of the possible combinations BuildKit, with its pluggable backends and frontends, unlocks.

![animation of `buildctl` building a dockerfile](/blog/assets/images/what-is-buildkit-and-what-can-i-do-with-it/1.gif)

The original BuildKit proposal is found in the Moby project:
<!-- markdownlint-disable MD028 -->

> "BuildKit is a proposal to separate out docker build experience into a separate project, allowing different users to collaborate on the underlying technology and reuse and customize it in different ways."

> "One of the main design goals of BuildKit is to separate frontend and backend concerns during a build process" - [Initial BuildKit Proposal](https://github.com/moby/moby/issues/32925)

## Install BuildKit

### buildctl

BuildKit has two primary components: buildctl and buildkitd. buildctl is the BuildKit controller, and it communicates with `buildkitd`. Though designed for Linux, it can run on macOS and Windows under WSL2.  

On macOS, you can install buildctl with brew.  

~~~{.bash caption=">_"}
> brew install buildkit
~~~

On Linux and Windows, grab a release from [GitHub](https://github.com/moby/buildkit/releases).

Afterward, you should be able to call buildctl

~~~{caption=">_"}
> buildctl
NAME:
   buildctl - build utility

USAGE:
   buildctl [global options] command [command options] [arguments...]

VERSION:
   0.8.1

COMMANDS:
   du        disk usage
   prune     clean up build cache
   build, b  build
   debug     debug utilities
   help, h   Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug                enable debug output in logs
   --addr value           buildkitd address (default: "unix:///run/buildkit/
   buildkitd.sock")
   --tlsservername value  buildkitd server name for certificate validation
   --tlscacert value      CA certificate for validation
   --tlscert value        client certificate
   --tlskey value         client key
   --tlsdir value         directory containing CA certificate, client 
   certificate, and client key
   --timeout value        timeout backend connection after value seconds 
   (default: 5)
   --help, -h             show help
   --version, -v          print the version
~~~

 ***Other Tools**: In this guide, we will use [pstree](https://linux.die.net/man/1/pstree), [br](https://github.com/Canop/broot), and [mitmproxy](/blog/mitmproxy/). They are not required to use BuildKit or to follow this guide, but they help us demonstrate how BuildKit works.m

### buildkitd

buildkitd does the actual work of transforming a build definition into some output. It is designed to be a long-running process. It also isn't possible to run it on macOS or Windows. For this tutorial, we will run it as a docker container. That will work regardless of your host OS.

~~~{caption=">_"}
> docker run --rm --privileged -d --name buildkit moby/buildkit
Unable to find image 'moby/buildkit:latest' locally
latest: Pulling from moby/buildkit
05e7bc50f07f: Already exists 
d7d1da19a5ee: Already exists 
10f8f68c5adb: Already exists 
00d21c774e02: Already exists 
Digest: sha256:ecd5ad4910c322cad6995f8a1a0805d9da4b09ed4aaef40627f5bcb8ebf74068
Status: Downloaded newer image for moby/buildkit:latest
6c4342639e07eedc16ba2f5d9f91fb2f82e1793cdea73aec1725e6652cab315a
~~~

~~~{caption=">_"}
➜ docker ps
CONTAINER ID   IMAGE           COMMAND       CREATED          STATUS          
6c4342639e07   moby/buildkit "buildkitd" 45 seconds ago  
~~~

We also need to tell buildctl where to find buildkitd:

~~~{.bash caption=">_"}
> export BUILDKIT_HOST=docker-container://buildkit
~~~

*On Linux, you can substitute these steps with just running `buildkitd` to avoid the container.*

## Building an Image

Now that we have all dependencies we need, let's build an image using BuildKit:

~~~{.dockerfile caption="DockerFile"}
FROM alpine
RUN echo "built with BuildKit!" >  file
CMD ["/bin/sh"]
~~~

~~~{caption=">_"}
> buildctl build \
    --frontend=dockerfile.v0 \
    --local context=. \
    --local dockerfile=.
[+] Building 1.4s (5/5) FINISHED                               
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 453B                      0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
 => [internal] load metadata for docker.io/library/alpin  1.3s
 => [auth] library/alpine:pull token for registry-1.dock  0.0s
 => [1/2] FROM docker.io/library/alpine@sha256:08d6ca16c  0.0s
 => => resolve docker.io/library/alpine@sha256:08d6ca16c  0.0s
  => [2/2] RUN echo "built with buildkit!" >  file   
~~~

We have built the image, but we haven't given it a name nor told BuildKit what to do with it.

By default, the build result will remain internal to BuildKit. An output type needs to be specified to retrieve the result. Let's specify a docker hub account that we have permission to push to:

~~~{caption=">_"}
> buildctl build \
    --frontend=dockerfile.v0 \
    --local context=. \
    --local dockerfile=. \
    --output type=image,name=docker.io/agbell/test,push=true
[+] Building 2.9s (8/8) FINISHED                               
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 32B                       0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
 => [internal] load metadata for docker.io/library/alpin  0.7s
 => [auth] library/alpine:pull token for registry-1.dock  0.0s
 => [1/1] FROM docker.io/library/alpine@sha256:08d6ca16c  0.0s
 => => resolve docker.io/library/alpine@sha256:08d6ca16c  0.0s
 => [2/2] RUN echo "built with buildkit!" >  file 
 => exporting to image                                    2.2s
 => => exporting layers                                   0.0s
 => => exporting manifest sha256:a81d7671b5ceeb534739c95  0.0s
 => => exporting config sha256:4c8c89bca725572cf9ff3bd6a  0.0s
~~~

After that, we can pull it and run it:

~~~{.bash caption=">_"}
> docker run -it agbell/test
> cat file
built with BuildKit!
~~~

## Tangent: Where Are `FROM`'s From?

If we have an image locally on our machine, can we use it in a `FROM` to build something based on it? Let's find out by altering our `FROM` to use a local image:

~~~{.dockerfile caption="Dockerfile"}
FROM agbell/test:local
RUN echo "BuildKit built">  file
CMD ["/bin/sh"] 

~~~

~~~{caption=">_"}
> docker tag alpine agbell/test:local
> buildctl build \
    --frontend=dockerfile.v0 \
    --local context=. \
    --local dockerfile=. \