---
title: "Understanding Docker Multistage Builds"
categories: 
  - Tutorials
toc: true 
author: Lukonde Mwila
sidebar:
  nav: "docker"
---

At first glance, writing Dockerfiles appears to be a straightforward process. After all, most basic examples reflect the same set of steps. However, not all Dockerfiles are created equal. There is an optimal way of writing these files to produce the kind of Docker images you want for your final product. If you were to pop the hood, you'd see that Docker images actually consist of file system layers that correlate to the individual build steps involved in the creation of the image.

To build an efficient Docker image, you want to eliminate some of these layers from the final output. Optimizing an image can take a lot of effort as you attempt to filter out what you don't need. Building these kinds of images has a lot to do with keeping them as small as possible, because large images lead to a host of other issues.

One approach to keeping Docker images small is using multistage builds. A multistage build allows you to use multiple images to build a final product. In a multistage build, you have a single Dockerfile, but can define multiple images inside it to help build the final image.

In this post, you'll learn about the core concepts of multistage builds in Docker and how they help to create production-grade images. In addition, I will detail how you can create these types of files, as well as highlight some challenges that they present.

## Core Concepts of Docker Multistage Builds

Before getting to the details of multistage builds, it's good to have an understanding of the main idea behind them. You're already familiar with the starting point of container images, the Dockerfile. Dockerfiles are text files that make it easy to assemble all the relevant commands required to create your container image. These commands in the Dockerfile should be combined whenever possible for the sake of optimization.

When I first came across this idea of building the right kind of Docker image, I asked myself a few questions that may be crossing your mind as you read this. What are the implications of *not* optimizing an image? Can it really have that much of a negative impact on your application? The answer to the latter question is yes.

As for the implications, you typically end up with bigger images. The reason big images should be avoided is because [they increase both potential security vulnerabilities and the surface area for attack](https://developers.redhat.com/blog/2016/03/09/more-about-docker-images-size/ "Keep it small: a closer look at Docker image sizing"). You definitely want to keep things lean by ensuring you only have what your application needs to run successfully in a production environment.

One way of reducing the size of your Docker images is through the use of what is informally known as the [builder pattern](https://en.wikipedia.org/wiki/Builder_pattern "builder design pattern entry at Wikipedia"). The builder pattern uses two Docker images to create a base image for building assets and the second to run it. This pattern was previously implemented through the use of multiple Dockerfiles. It has become an uncommon practice since the introduction and support of multistage builds in [Docker 17.06 CE](https://www.docker.com/blog/multi-stage-builds/ "Multi-Stage Builds").

For context, it's good to understand how this was typically done before multistage builds. The following example makes use of a basic React application that is first built and then has its static content served by an [Nginx virtual server](https://www.nginx.com/ "Nginx web servers"). Following are the two Dockerfiles used to create the optimized image. In addition, you'll see a shell script that demonstrates the Docker CLI commands that have to be run in order to achieve this outcome. You can find the source code for this example in [this repository](https://github.com/LukeMwila/builder-pattern-example "builder pattern example in Lukonde Mwila's GitHub repository").

```
Dockerfile.build
FROM node:12.13.0-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
```

```
Dockerfile.main
FROM nginx
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY /app/build /usr/share/nginx/html
```

```
Build.sh
#!/bin/sh
echo Building lukondefmwila/react:build

docker build -t lukondefmwila:build . -f Dockerfile.build

docker create --name extract lukondefmwila:build

docker cp extract:/app/build ./app

docker rm -f extract

echo Building lukondefmwila/react:latest

docker build --no-cache -t lukondefmwila/react:latest . -f Dockerfile.main
```

While using the builder pattern does give you the desired outcome, it presents additional challenges. This process introduces the management overhead that comes with maintaining multiple Dockerfiles—not to mention the cumbersome procedure of running through several Docker CLI commands, even if this can be streamlined by a shell script.

## How to Use Docker Multistage Builds

Now that you get the underlying concept, turn your attention to how this translates to the modern implementation of the builder pattern. What the former approach accomplishes with multiple Dockerfiles, the multistage feature does in one. You can get the same results with your builds without the added complexity.

Multistage builds make use of one Dockerfile with multiple FROM instructions. Each of these FROM instructions is a new build stage that can COPY artifacts from the previous stages. By going and copying the build artifact from the build stage, you eliminate all the intermediate steps such as downloading of code, installing dependencies, and testing. All these steps create additional layers, and you want to eliminate them from the final image.

The build stage is named by appending AS _name-of-build_ to the FROM instruction. The name of the build stage can be used in a subsequent FROM and COPY command by providing a convenient way to identify the source layer for files brought into the image build. The final image is produced from the last stage executed in the Dockerfile.

Try taking the example from the previous section that used more than one Dockerfile for the React application and replacing the solution with one file that uses a multistage build.

```
Dockerfile
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
```

This Dockerfile has two FROM commands, with each one constituting a distinct build stage. These distinct commands are numbered internally, stage 0 and stage 1 respectively. However, stage 0 is given a friendly alias of `build`. This stage builds the application and stores it in the directory specified by the WORKDIR command. The resultant image is over 420 MB in size.

The second stage starts by pulling the official Nginx image from Docker Hub. It then copies the updated virtual server configuration to replace the default Nginx configuration. Then the COPY --from command is used to copy only the production-related application code from the image built by the previous stage. The final image is approximately 127 MB.

## Problems That Docker Multistage Builds Might Encounter

Depending on how they are designed, multistage builds can introduce some serious issues around the speed of the build process. Since these Dockerfiles have multiple stages to produce the production-grade image, your cache will not consist of the images built in the previous steps leading to your final output. Simulating the build locally might give you the impression that it's worth the wait. However, when you're working with build services such as [AWS CodeBuild](https://aws.amazon.com/codebuild/), [Travis CI](https://travis-ci.org/), or [CircleCI](https://circleci.com/), you want to keep your build time as short as possible for cost reasons, as well as streamlining application delivery.

In order to make use of the cache, you will have to tag, push, and pull the images produced from the preliminary build stages. As an example, take the multistage Dockerfile from the previous section and split it into two files, Dockerfile.stage-one and Dockerfile.final. The first Dockerfile will create the image that will be pulled and used in stage 0 of the multistage Dockerfile.

```
Dockerfile.stage-one
FROM node:12.13.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
```

```
Dockerfile.final
FROM lukondefmwila/react:build-stage as build

FROM nginx
EXPOSE 3000
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
```

That being said, following such an approach for every stage can create an increasingly verbose process every stage that you have. Another way of solving this issue is to make use of [BuildKit](https://earthly.dev/blog/what-is-buildkit-and-what-can-i-do-with-it/). BuildKit came about to address issues and improve on the build features in the [Moby Engine](https://mobyproject.org/). It allows for better cache efficiency and control when building. To enable BuildKit builds, follow the steps outlined in [Docker's documentation](https://docs.docker.com/develop/develop-images/build_enhancements/#to-enable-buildkit-builds).

## More Stages

As your multi-stage build grows in complexity, comprehending how each step follows from the next can become a challenge.  If the number of stages extends beyond two or if caching is becoming a challenge, you may want to consider using [Earthly](http://earthly.dev/) to produce your docker images. Earthly mirrors the dockerfile syntax but allows for naming the stages and for more fine-grained caching.

```
FROM node:12.13.0-alpine as build
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
```

## Conclusion

While creating Docker images the right way is not a small task, the final outcome does a great deal of good for the speed and security of your application delivery. Larger images have a high number of security vulnerabilities that shouldn't be overlooked for the sake of speed. The reality is that quality images take time and care.

The builder pattern has evolved over time in its implementation, with multistage builds coming to the rescue from the tedious steps that previously had to be followed. Tools like BuildKit and Earthly further improve on this process. Though not foolproof, multistage builds have made it much easier to create optimized images that you can be more pleased and confident to have running in your production environment.
