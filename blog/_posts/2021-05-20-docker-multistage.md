---
title: "Understanding Docker Multistage Builds"
categories: 
  - Tutorials
toc: true 
author: Lukonde Mwila
sidebar:
  nav: "docker"
internal-links:
 - multistage build
 - docker multistage build
 - docker multi-stage builds
 - multistage
topic: docker
funnel: 2
excerpt: |
    Learn how to optimize your Docker images and create production-grade images using multistage builds. Discover the core concepts of multistage builds, the challenges they present, and a better way to do multi-stage builds with Earthly.
last_modified_at: 2023-07-14
---
**Explore the advantages of Docker multistage builds in this article. Earthly enhances your build process through efficient layer caching and parallel execution. It's an improved Docker Multi-stage build. [Learn more](https://cloud.earthly.dev/login).**

At first glance, writing Dockerfiles appears to be a straightforward process. After all, most basic examples reflect the same set of steps. However, not all Dockerfiles are created equal. There is an optimal way of writing these files to produce the kind of Docker images you want for your final product. If you were to pop the hood, you'd see that Docker images actually consist of file system layers that correlate to the individual build steps involved in the creation of the image.

To build an efficient Docker image, you want to eliminate some of these layers from the final output. Optimizing an image can take a lot of effort as you attempt to filter out what you don't need. Building these kinds of images has a lot to do with keeping them as small as possible, because large images lead to a host of other issues.

One approach to keeping Docker images small is using multistage builds. A multistage build allows you to use multiple images to build a final product. In a multistage build, you have a single Dockerfile, but can define multiple images inside it to help build the final image.

In this post, you'll learn about the core concepts of multistage builds in Docker and how they help to create production-grade images. In addition, I will detail how you can create these types of files, as well as highlight some challenges that they present. I'll end with a better way to do multi-stage builds using [Earthly](https://cloud.earthly.dev/login).

**(For The Impatient: <a href="#a-better-way-earthly">Skip to 'Better Multi-Stage Builds'</a>)**

## Core Concepts of Docker Multistage Builds

Before getting to the details of multistage builds, it's good to have an understanding of the main idea behind them. You're already familiar with the starting point of container images, the Dockerfile. Dockerfiles are text files that make it easy to assemble all the relevant commands required to create your container image. These commands in the Dockerfile should be combined whenever possible for the sake of optimization.

When I first came across this idea of building the right kind of Docker image, I asked myself a few questions that may be crossing your mind as you read this. What are the implications of *not* optimizing an image? Can it really have that much of a negative impact on your application? The answer to the latter question is yes.

As for the implications, you typically end up with bigger images. The reason big images should be avoided is because [they increase both potential security vulnerabilities and the surface area for attack](https://developers.redhat.com/blog/2016/03/09/more-about-docker-images-size/ "Keep it small: a closer look at Docker image sizing"). You definitely want to keep things lean by ensuring you only have what your application needs to run successfully in a production environment.

## The Old Way: Builder Pattern

One way of reducing the size of your Docker images is through the use of what is informally known as the builder pattern. The builder pattern uses two Docker images to create a base image for building assets and the second to run it. This pattern was previously implemented through the use of multiple Dockerfiles. It has become an uncommon practice since the introduction and support of multistage builds.

For context, it's good to understand how this was typically done before multistage builds. The following example makes use of a basic React application that is first built and then has its static content served by an [Nginx virtual server](https://www.nginx.com/ "Nginx web servers"). Following are the two Dockerfiles used to create the optimized image. In addition, you'll see a [shell script](/blog/understanding-bash) that demonstrates the Docker CLI commands that have to be run in order to achieve this outcome. You can find the source code for this example in [this repository](https://github.com/LukeMwila/builder-pattern-example "builder pattern example in Lukonde Mwila's GitHub repository").

~~~{.dockerfile caption="Dockerfile.build"}
FROM node:12.13.0-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
~~~

~~~{.dockerfile caption="Dockerfile.main"}
FROM nginx
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY /app/build /usr/share/nginx/html
~~~

~~~{.bash caption="Build.sh"}
#!/bin/sh
echo Building lukondefmwila/react:build
docker build -t lukondefmwila:build . -f Dockerfile.build
docker create --name extract lukondefmwila:build
docker cp extract:/app/build ./app
docker rm -f extract

echo Building lukondefmwila/react:latest
docker build --no-cache -t lukondefmwila/react:latest . -f Dockerfile.main
~~~

While using the builder pattern does give you the desired outcome, it presents additional challenges. This process introduces the management overhead that comes with maintaining multiple Dockerfiles—not to mention the cumbersome procedure of running through several Docker CLI commands, even if this can be streamlined by a shell script.

## The Next Way: Docker Multistage Builds

Now that you get the underlying concept, turn your attention to how this translates to the modern implementation of the builder pattern. What the former approach accomplishes with multiple Dockerfiles, the multistage feature does in one. You can get the same results with your builds without the added complexity.

Multistage builds make use of one Dockerfile with multiple FROM instructions. Each of these FROM instructions is a new build stage that can COPY artifacts from the previous stages. By going and copying the build artifact from the build stage, you eliminate all the intermediate steps such as downloading of code, installing dependencies, and testing. All these steps create additional layers, and you want to eliminate them from the final image.

The build stage is named by appending `AS *name-of-build*` to the FROM instruction. The name of the build stage can be used in a subsequent FROM and COPY command by providing a convenient way to identify the source layer for files brought into the image build. The final image is produced from the last stage executed in the Dockerfile.

Try taking the example from the previous section that used more than one Dockerfile for the React application and replacing the solution with one file that uses a multistage build.

~~~{.Dockerfile caption="Dockerfile"}
FROM node:12.13.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
~~~

This Dockerfile has two `FROM` commands, with each one constituting a distinct build stage. These distinct commands are numbered internally, stage 0 and stage 1 respectively. However, stage 0 is given a friendly alias of `build`. This stage builds the application and stores it in the directory specified by the WORKDIR command. The resultant image is over 420 MB in size.

The second stage starts by pulling the official Nginx image from Docker Hub. It then copies the updated virtual server configuration to replace the default Nginx configuration. Then the `COPY --from` command is used to copy only the production-related application code from the image built by the previous stage. The final image is approximately 127 MB.

## Problems That Docker Multistage Builds Might Encounter

Depending on how they are designed, multistage builds can introduce some serious issues around the speed of the build process. Since these Dockerfiles have multiple stages to produce the production-grade image, they can take a while to build. If you are using the latest docker version and have enabled BuildKit then caching will likely help speed things up. But there is another problem, Readability.

<div class="notice--info">

### Enable BuildKit

You can enable BuildKit, and get faster multi-stage builds by setting the DOCKER_BUILDKIT environment variable to 1. In newer versions of Docker this is enabled by default.
</div>

## A Better Way: Earthly

As your multi-stage build grows in complexity, comprehending how each step follows from the next can become a challenge. If the number of stages extends beyond two or if caching is becoming a challenge even with Buildkit enabled, you may want to consider using [Earthly](https://cloud.earthly.dev/login) to produce your docker images.

Earthly mirrors the dockerfile syntax but allows for naming the stages and for more fine-grained caching.

Here is our previous solution in Earthly:

~~~{.Dockerfile caption="Earthfile"}
FROM node:12.13.0-alpine
WORKDIR /app

build:
  COPY package*.json ./
  RUN npm install
  COPY . .
  RUN npm run build

final:
  FROM nginx
  EXPOSE 3000
  COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
  COPY  +build/app/build /usr/share/nginx/html
~~~

The stages are now named `build` and `final` and the copy syntax has changed slightly from:

~~~{.Dockerfile caption=""}
COPY --from=build /app/build /usr/share/nginx/html
~~~

To:

~~~{.Dockerfile caption=""}
COPY  +build/app/build /usr/share/nginx/html
~~~

This is only scratching the surface of what the open source Earthly project can do. But once you have multiple stages in play, I'd recommend converting your Dockerfiles to Earthfiles.

<div class="notice--info">

### Using Earthly

* Mac users: `brew install earthly`. ([Other platforms](/get-earthly))
* Rename `Dockerfile` to `Earthfile`.
* Build image  (`earthly +final` for above example).
* Read more on [the website](https://cloud.earthly.dev/login/).

</div>

## Conclusion

While creating Docker images the right way is not a small task, the final outcome does a great deal of good for the speed and security of your application delivery. Larger images have a high number of security vulnerabilities that shouldn't be overlooked for the sake of speed. The reality is that quality images take time and care.

The builder pattern has evolved over time in its implementation, with multistage builds coming to the rescue from the tedious steps that previously had to be followed. Tools like BuildKit and Earthly further improve on this process.

Though not foolproof, multistage builds have made it much easier to create optimized images that you can be more pleased and confident to have running in your production environment.

{% include_html cta/bottom-cta.html %}
