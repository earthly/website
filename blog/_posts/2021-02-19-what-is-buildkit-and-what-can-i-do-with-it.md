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
excerpt: |
    Learn how to use BuildKit, an open-source project that turns Dockerfiles into Docker images. Discover its history, how to install it, and how to build images using BuildKit directly. Explore different output types and gain insights into the inner workings of BuildKit.
last_modified_at: 2023-07-19
---
**The article explores BuildKit's capabilities. Earthly enhances BuildKit with additional build automation and optimization. [Check it out](https://cloud.earthly.dev/login/).**

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
------
 > [internal] load metadata for docker.io/agbell/test:local:
------
error: failed to solve: rpc error: code = Unknown desc = failed to solve 
with frontend dockerfile.v0: failed to create LLB definition: docker.io/agbell/
test:local: not found

~~~

It doesn't work. It looks like it is trying to fetch the image from docker.io, the default docker hub registry.  

We can verify this by quickly [capturing requests](https://earthly.dev/blog/mitmproxy/) from buildkitd:

~~~{.dockerfile caption="Dockerfile"}
FROM moby/buildkit 
RUN apk update && apk add curl
WORKDIR /usr/local/share/ca-certificates
COPY mitmproxy.crt mitmproxy.crt
RUN update-ca-certificates
~~~

~~~{.bash caption=">_"}
> docker build . -t buildkit:mitm
 ...
> docker run --rm --privileged -d --name buildkit buildkit:mitm
6676dc0109eb3f5f09f7380d697005b6aae401bb72a4ee366f0bb279c0be137b
~~~

![404 on mitmproxy](/blog/assets/images/what-is-buildkit-and-what-can-i-do-with-it/2.png)

We can see a `404`, and this confirms buildkitd is expecting registry that it can access over the network using the docker registry v2 api.

## Watching It Build

`buildkitd` is responsible for building the image, but `runc` does the actual execution of each step. `runc` executes each `RUN` command in your dockerfile in a separate process. runc requires Linux kernel 5.2 or later with support for cgroups, and is why buildkitd can't run natively on macOS or Windows.

### What Is `runc`?

> "Please note that runc is a low-level tool not designed with an end-user in mind. It is mostly employed by other higher-level container software. Therefore, unless there is some specific use case that prevents the use of tools like Docker or Podman, it is not recommended to use runc directly." - [runc readme](https://github.com/opencontainers/runc)

We can watch the execution of our build by using `pstree` and `watch`. Open two side by side terminals, run `docker exec -it buildkit "/bin/watch" "-n1" "pstree -p"` in one and call `buildctl build ...` in the other. You will see `buildkitd` start a `buildkit-runc` process and then a separate process for each `RUN` command.

<div class="wide">
![Diagram of BuildKit running and pstree showing the process tree of buildkitd](/blog/assets/images/what-is-buildkit-and-what-can-i-do-with-it/3.png)
</div>

## How to See Docker Processes on macOS and Windows

On macOS and Windows, Docker processes run on a separate virtual machine (VM). If you're using the default and recommended Docker Desktop, this VM is the Linux container host.  

*Note: Docker Machine is an earlier approach to running Docker on macOS and Windows where the Docker VM runs in VirtualBox or VMware. Docker Machine steps may differ.*

The above `exec` trick lets us see the processes inside a specific container, but to see all the processes running across all the containers, we need a different technique. To do that, we can use `docker run` and `nsenter`:

~~~{.bash caption=">_"}
docker run -it --rm --privileged --pid=host ubuntu \
  nsenter -t 1 -m -u -n -i s
~~~

We can now use `watch` and `pstree` to view the whole container host in a single view:

~~~{caption="pstree -p"}
init(1)-+-containerd(983)
        |-containerd-shim(1018)---acpid(1039)
        |-containerd-shim(1064)---diagnosticsd(1085)---sh(1354)
        |-containerd-shim(1109)-+-containerd-shim(2495)-+-buildkitd(2522)
        |                       |                       `-sh(2614)---watch(2903)
        |                       |-containerd-shim(4035)---sh(4062)---pstree(5058)
        |                       |-docker-init(1136)---entrypoint.sh(1154)---logwrite(1183)---lifecycle-serve(1188)-+-logwrite(1340)---containerd(1345)
        |                       |                                                                                  |-logwrite(1550)---dockerd(1555)
        |                       |                                                                                  `-logwrite(1800)
        |                       |-rpc.statd(1293)
        |                       `-rpcbind(1265)
        |-containerd-shim(1162)---host-timesync-d(1199)
        |-containerd-shim(1245)---kmsg(1282)
        |-containerd-shim(1310)---start(1347)---sntpc(1397)
        |-containerd-shim(1374)
        |-containerd-shim(1433)---trim-after-dele(1460)
        |-containerd-shim(1483)---vpnkit-forwarde(1517)
        |-memlogd(442)
        |-rungetty.sh(429)---login(431)---sh(443)
        |-rungetty.sh(432)---login(433)---sh(437)
        `-vpnkit-bridge(452)
~~~

We can use pstree with a process id (pid) while a build is running to focus on just the buildkitd tree:

~~~{.bash caption=">_"}
> docker-desktop:/# watch -n 1 pstree -p 2522 
~~~

## BuildKit Output Types

So far, we have only used `output type=image,` but BuildKit supports several types of outputs.

We can output a tar:

~~~{.bash caption=">_"}
buildctl build \
    --frontend=dockerfile.v0 \
    --local context=. \
    --local dockerfile=. \
    --output type=tar,dest=out.tar
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 31B                       0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
...
 => exporting to client                                   2.6s
 => => sending tarball                                    2.6s
~~~

~~~{.bash caption=">_"}
> ls *.tar
 out.tar
~~~

And if we try to load it as a docker image, it will fail:

~~~{.bash caption=">_"}
> docker load < out.tar
open /var/lib/docker/tmp/docker-import-013443725/bin/json: 
 no such file or directory
~~~

This tag isn't an image of any sort. There are no layers or manifests, just the full filesystem that the built image would contain.

We can also export directly to the local filesystem:

~~~{.bash caption=">_"}
buildctl build \
   --frontend dockerfile.v0 \
   --local context=. \
   --local dockerfile=. \
   --output type=local,dest=output   
[+] Building 2.6s (10/10) FINISHED                             
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 31B                       0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
 => [internal] load metadata for docker.io/library/alpin  0.6s
 => [auth] library/alpine:pull token for registry-1.dock  0.0s
 => [1/5] FROM docker.io/library/alpine@sha256:08d6ca16c  0.0s
 => => resolve docker.io/library/alpine@sha256:08d6ca16c  0.0s
 => CACHED [2/5] RUN apk update                           0.0s
 => CACHED [3/5] RUN apk upgrade                          0.0s
 => CACHED [4/5] RUN apk add gcc                          0.0s
 => CACHED [5/5] RUN sleep 1                              0.0s
 => exporting to client                                   1.9s
 => => copying files 121.14MB                             1.9sr
~~~

This filesystem output could be useful if we were trying to trim our image down. We could look through the output and find things to remove and use a multi-stage build to remove them. [broot](https://github.com/Canop/broot) is pretty handy for this:

<div class="wide">
![tree view of alpine image showing space used in each directory]({{site.images}}{{page.slug}}/4.png)
</div>

## What Is in `FROM scratch`

One thing we can do with our newfound powers is investigate the `scratch` keyword. The scratch keyword doesn't correspond to an actual image. We can't run it:

~~~{.bash caption=">_"}
docker run scratch
Unable to find image' scratch:latest' locally
docker: Error response from daemon: 'scratch' is a reserved name.
~~~

However, does it actually contain anything? Is a `FROM scratch` image literally empty or are there certain required elements of unix filesystem that `scratch` provides? Let's find out:

~~~{.bash caption=">_"}
> mkdir scratch
> cat .\Dockerfile
FROM scratch
> buildctl build --frontend dockerfile.v0 --local context=. --local dockerfile=. --output type=local,dest=scratch
[+] Building 0.1s (3/3) FINISHED                               
 => [internal] load build definition from Dockerfile      0.0s
 => => transferring dockerfile: 31B                       0.0s
 => [internal] load .dockerignore                         0.0s
 => => transferring context: 2B                           0.0s
 => exporting to client                                   0.0s
 => => copying files                                      0.0s
 > ls scratch
 > br -s scratch
 0 ./output
~~~

It's empty! The scratch keyword indicates a completely empty docker layer. The more you know! *(The more you know is a trademark of The National Broadcasting Company, who in no way endorse this article 😀 )*

## Conclusion

So, we've gone over a few ways to use BuildKit directly, which offers more features than the modern `docker build`. With it, you can do cool stuff like changing the output type and monitoring process and network requests. But we've just scratched the surface! BuildKit aids in multi-platform builds, enables parallel builds, supports caching, and boosts multi-stage builds, among other things.

If you've enjoyed exploring BuildKit and are looking to take things up a notch, you might want to check out [Earthly]((https://cloud.earthly.dev/login)). It offers an optimized build process and extends the functionality available in BuildKit.

Stay tuned for a future post where we'll ditch Dockerfile syntax and explore creating a custom frontend.
