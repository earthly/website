---
title: "Docker and Makefiles: Building and Pushing Images with Make"
categories:
  - Tutorials
toc: true
sidebar:
  nav: "makefile"
author: Kasper Siig
internal-links:
 - makefiles
topic: make
excerpt: |
    Learn how to effectively use Docker and Makefiles together to simplify your deployment process. Discover the advantages of integrating Make into your Docker projects and see how it can streamline building, pushing, releasing, and versioning your Docker images.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about using Docker and Makefiles together for building and pushing images. Earthly is a powerful build tool that can greatly simplify the process of building and deploying Docker images, making it an ideal tool to use in conjunction with Docker and Makefiles. [Check us out](/).**

Deployments have been one of the hassles for many organizations for a long time, with companies sometimes even hiring engineers whose sole job is to get applications deployed more effectively. Because of this, many tools have been developed to help with this exact use case. However, some prefer to use tools that have already existed for many years: Docker and Makefiles.

As these are both very popular tools, it's likely that hearing they're commonly used isn't a surprise to many people, but the full extent to which they can be used together might be. Back when one of my colleagues first opened my eyes to using Docker and Makefiles together, I certainly wasn't aware of all the possibilities.

In this post, you'll be taken through some of the ways that Docker and GNU Make can effectively be used together. This will be shown by providing a simple Go example application, around which a Dockerfile and Makefile will be built. To follow along, you'll need to have at least a basic understanding of Makefiles and Docker.

## Why Use Docker With Make?

Many developers already know why it makes sense to use Docker for your application. It helps you run things locally, ensuring that the environment is exactly what it will be when you run it on your servers. On top of that, it removes the need to install every tool locally, and instead allows you to simply run a `docker` command to have your application running.

Adding GNU Make to the recipe is where some people will fail to see the advantage. You'll hear some asking "Isn't Make an old tool?" or "Isn't it only meant for C and C++ projects?". In reality, this couldn't be farther from the truth. It's correct that Make is a utility developed back in the '70s and '80s, and yes, it's perceived as being tied to C and C++ applications, but that doesn't mean it doesn't have its advantages in other projects.

In the following sections of this article, you'll see just how useful Make can be when integrated into a Docker project. You'll see some of the simple advantages like not having to type out long commands, as well as some more advanced use cases like dynamically created Make targets for different Dockerfiles.

### Integrating Make Into Your Docker Project

To see how you can integrate Make into your Docker projects, you'll first need to define a project to work on. As mentioned in the introduction, this tutorial will use a simple Go project for this. If you'd like to look at the completed project as a whole, the code for this tutorial can be found in [this GitHub Repo](https://github.com/KSiig/docker-make).

#### Defining the Application

First, you need to define the application itself. Create a new folder, and create a file called `main.go` inside of it. In `main.go`, paste the following code:

> The code for this specific step can be found in the branch "starter".

~~~{.go caption="main.go"}
package main
 
import "fmt"
 
func main() {
         fmt.Println("Hello World!")
}
~~~

If you're not familiar with Go, this is simply a "Hello World" example. You start by defining the package called `main`, after which you import `fmt`. `fmt` is to Go what "stdio" is to C++—it's the library used to communicate with the console. Next, the function `main` is defined, inside of which "Hello World!" is printed to the command line.

Go requires that a Module needs to be specified in order to build the application. This is done by simply running `go mod init` in your terminal. Once this is done, all that's left is to create the Dockerfile. Create a file named `Dockerfile`, and paste the following into it:

~~~{.dockerfile caption="Dockerfile"}
FROM golang:1.18-alpine
 
WORKDIR /app
 
COPY go.mod ./
COPY *.go ./
 
RUN go build -o /hello-world
 
CMD ["/hello-world"]
~~~

If you've worked with Dockerfiles before, this should be very familiar. Start by defining the base image on line one, and then define the working directory inside the container. After that, you copy some files into the container, build the application by running `go build -o /hello-world`, and set the built binary to be executed when the container is spun up. You can make sure that everything works as expected by running `docker build --tag username/hello-world . && docker run username/hello-world`, replacing `username` with your own username in both instances. If the last line in your terminal is now "Hello World!", everything is working as intended!

Time to add a Makefile to the equation.

### Building and Pushing the Application

> The code for this step can be found in the "build-and-push" branch.

Start by creating a file called `Makefile`. In this file, you'll need to paste the following:

~~~{.Makefile caption="Makefile"}
DOCKER_USERNAME ?= username
APPLICATION_NAME ?= hello-world
 
build:
         docker build --tag ${DOCKER_USERNAME}/${APPLICATION_NAME} .
~~~

Again, be sure to replace the `DOCKER_USERNAME` variable with your own username. As you can see, this is a very simple Make target, and you can now run `make build` in your terminal to have your application built. At this point, you can start to see the advantages of using Make. You can now run just `make build` instead of `docker build --tag username/hello-world .`. Not only that, but if you integrate Make into all of your projects, you can always just run `make build`, and not even have to think about what the name of the project is.

The next step is to push the image. Again, this is a very simple target inside Make:

~~~{.Makefile caption="Makefile"}
push:
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}
~~~

You can now run `make push` to push the application to Docker Hub. If you're using your own Docker repository, remember to add that to the name of the image to make it work. You may still be unconvinced that it's worth using Docker and Makefile together. The really impressive part comes when you get used to not using those two make targets individually, but together:

~~~{.bash caption=">_"}
$ make build push
~~~

This will become a huge time saver, especially if you integrate Make in all your Docker projects.

### Releasing and Versioning the Application

> The code for this step can be found in the "release-and-versioning" branch.

You've been shown how to build and push your Docker images with Make, but the biggest advantage when using Make is when it comes to releasing and versioning. With the way your Makefile is defined right now, all your images with be given the tag "latest". This isn't great, especially if you're using this in production and you accidentally execute `make push` locally.

Instead, let's add some functionality to the Makefile so it uses the Git SHA hash when building and pushing your image. Start by adding this variable to the top of your Makefile:

~~~{.Makefile caption="Makefile"}
GIT_HASH ?= $(shell git log --format="%h" -n 1)
~~~

This gets the SHA hash from Git and stores it in the `GIT_HASH` variable. Now you can append this to both cases where you define the tag for your Docker image:

~~~{.Makefile caption="Makefile"}
build:
         docker build --tag ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} .
 
push:
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH}
~~~

Now you can run `make build push` again, and see that it's now using the Git hash to tag your image. This is great for working on it locally, but what do you do when you want to actually push a `:latest` tag? In theory, you could overwrite the `GIT_HASH` variable when executing `make build push`, but that's more of a workaround. Instead, let's create a new target:

~~~{.Makefile caption="Makefile"}
release:
         docker pull ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH}
         docker tag  ${DOCKER_USERNAME}/${APPLICATION_NAME}:${GIT_HASH} ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest
~~~

Three things are happening here. First, the image with the given Git hash is pulled from the Docker repository. This may seem excessive since the image has just been built, but is incredibly useful if, as an example, you're running this in a CI/CD pipeline where you don't want to build the application again, you just want to tag it with `latest` and release it. This is exactly what happens in the following two lines. The existing image is tagged with `latest`, and then it's pushed to the Docker repository.

You've now fully integrated Make into your Docker repository, and hopefully you can see the advantages that it'll bring to your workflow. This is all you really need to get started with using Make in Docker, but read on to see a more advanced use case.

### Working With Multiple Dockerfiles

> The code for this step can be found in the branch `multiple-dockerfiles`.

There are instances where you want your project to contain multiple Dockerfiles. Maybe you have a repository that defines a bunch of different pipeline runners, or maybe you just want to have a version of your application that's easier to debug. Whatever the case, this step is useful if you have more than one Dockerfile.

As an example, let's take the case of wanting to have a version of your Docker image that has `make` installed, which is something our version of Alpine doesn't have by default. You don't want to add it to your production image, as it increases the image size, so instead you create a `Dockerfile.debug` where `make` is installed:

~~~{.dockerfile caption="Dockerfile"}
FROM golang:1.18-alpine
 
WORKDIR /app
 
COPY go.mod ./
COPY *.go ./
 
RUN go build -o /hello-world
RUN apk update
RUN apk add make # install make
 
CMD ["/hello-world"]
~~~

Now you have a debug version of your Dockerfile, but there's currently no way to build it using `make` commands. This requires some changes to your Makefile. First the existing targets have to be changed slightly:

~~~{.Makefile caption="Makefile"}
_BUILD_ARGS_TAG ?= ${GIT_HASH}
_BUILD_ARGS_RELEASE_TAG ?= latest
_BUILD_ARGS_DOCKERFILE ?= Dockerfile
 
_builder:
         docker build --tag ${DOCKER_USERNAME}/${APPLICATION_NAME}:${_BUILD_ARGS_TAG} -f ${_BUILD_ARGS_DOCKERFILE} .
 
_pusher:
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:${_BUILD_ARGS_TAG}
 
_releaser:
         docker pull ${DOCKER_USERNAME}/${APPLICATION_NAME}:${_BUILD_ARGS_TAG}
         docker tag  ${DOCKER_USERNAME}/${APPLICATION_NAME}:${_BUILD_ARGS_TAG} ${DOCKER_USERNAME}/${APPLICATION_NAME}:latest
         docker push ${DOCKER_USERNAME}/${APPLICATION_NAME}:${_BUILD_ARGS_RELEASE_TAG}
~~~

Two major changes have been made. First of all, the variables `_BUILD_ARGS_RELEASE_TAG`, `_BUILD_ARGS_TAG`, and `_BUILD_ARGS_DOCKERFILE` have been added. These follow the changes that have been made to the targets, which have been changed to `_builder`, `_pusher`, and `_releaser`, respectively. You can still use these targets as you have so far, like running `make _builder _releaser`, but if you're familiar with Make syntax, you'll know that the `_` at the start of these variables and targets indicates that they're not meant to be called from outside.

Instead, these targets are now internal. To restore the simple functionality of `make build push release`, we're going to create three new targets:

~~~{.Makefile caption="Makefile"}
build:
         $(MAKE) _builder
 
push:
         $(MAKE) _pusher
 
release:
         $(MAKE) _releaser
~~~

Now you once again have the functionality of `make build push release`. This might seem redundant, which so far is correct. The exciting part about this is the next three targets that will be added to the Makefile:

~~~{.Makefile caption="Makefile"}
build_%:
         $(MAKE) _builder \
                     -e _BUILD_ARGS_TAG="$*-${GIT_HASH}" \
                     -e _BUILD_ARGS_DOCKERFILE="Dockerfile.$*"
 
push_%:
         $(MAKE) _pusher \
                     -e _BUILD_ARGS_TAG="$*-${GIT_HASH}"
 
release_%:
         $(MAKE) _releaser \
                     -e _BUILD_ARGS_TAG="$*-${GIT_HASH}" \
                     -e _BUILD_ARGS_RELEASE_TAG="$*-latest"
~~~

This is where the magic of this configuration really lies. To understand what's happening, take a look at the `build_%` target. It's using `%` and `$*` in combination to make for dynamic targets. In this case, if you execute `make build_debug`, it will build an image with the tag `debug-${GIT_HASH}` based on the `Dockerfile.debug` target. Now you can make endless variations of your Dockerfiles—without having to create multiple different make targets.

This does add some complexity to your project, but it makes everything much more dynamic and easier to work with in the long run.

## Conclusion

By now, you've seen how you can easily and quickly add Make to your project. The advantages of using Make can range from simple use cases like avoiding typing out long commands, getting everyone on the team used to the same syntax in all projects, and even being able to create dynamic targets that create new possibilities for you and your team.

{% include_html cta/makefile-cta.html %}

<!-- If you're looking at this and thinking to yourself that it's still a bit complex for you and your organization, check out [Earthly](https://earthly.dev/), a tool that combines the best of Dockerfiles and Makefiles to make builds as easy as possible. -->