---
title: "Introducing Earthly Functions: Reusable Code for More Modular, Consistent Build Files"
categories:
  - News
toc: true
author: Gavin
topcta: false
internal-links:
 - introducing earthly functions
 - introduction to earthly functions
 - reusable code with earthly functions
 - consistent build files with earthly functions 
excerpt: |
    Introducing Earthly Functions: Reusable code blocks can enhance modularity and consistency in your Earthfiles.
---

The concept of functions runs deep in software development. Pretty much every programming language has functions or something similar that delivers the same capabilities: a block of code that performs a specific task that you can call from anywhere. Functions are a fundamental part of C. Methods, functions associated with specific classes, are part of almost every object-oriented programming language. Even SQL has functions.

Every programming language has functions because they are incredibly valuable. They make it easier to make programs modular and code reusable. These same benefits of modularity and reusability are valuable in your builds too. That's why we want to introduce you to Earthly Functions. Functions are exactly what you'd expect, reusable sets of instructions that can be imported into build targets or other functions in your Earthfiles. They are designed to make it easier to make your Earthfiles more modular and your build code less redundant.

## How to Use Functions

![how]({{site.images}}{{page.slug}}/how.png)\

Functions are defined similarly to build targets except that the function name must be in ALL_UPPERCASE_SNAKE_CASE and they must start with `FUNCTION`. For example:

~~~{.dockerfile caption="Earthfile"}
MY_COPY:
    FUNCTION
    ARG src
    ARG dest=./
    ARG recursive=false
    RUN cp $(if $recursive =  "true"; then printf -- -r; fi) "$src" "$dest"
~~~

You invoke a function using the `DO` command. For example:

~~~{.dockerfile caption="Earthfile"}
build:
    FROM alpine:3.18
    WORKDIR /function-example
    RUN echo "hello" >./foo
    DO +MY_COPY --src=./foo --dest=./bar
    RUN cat ./bar # prints "hello"
~~~

Functions look and are used in a very similar way to build targets. There are a few differences though. Functions inherit the build context and the build environment from the caller. So any local `COPY` operations in a function will use the directory where the calling Earthfile exists; any files, directories, and dependencies created by previous steps of the caller are available to the function to operate on; and any file changes resulting from execution of the function are passed back to the caller as part of the build environment.

_[Visit our docs from more information and details about using functions](https://docs.earthly.dev/docs/guides/functions)_

You can use functions that are defined in other Earthfiles in your repo or even other repositories. To do this you need to use `IMPORT` just like you would if you were importing build targets from another directory or repository. For an example, I'll be using Earthly [lib](https://github.com/earthly/lib). Earthly lib is a collection of reusable functions that we maintain to be used for common operations in Earthfiles. Here's how to easily mount and cache Gradle's cache using our [Gradle functions from Earthly lib](https://github.com/earthly/lib/tree/main/gradle).

~~~{.dockerfile caption="Earthfile"}
VERSION 0.8
IMPORT github.com/earthly/lib/gradle:3.0.2 AS gradle
FROM gradle:8.7.0-jdk21

deps:
    COPY settings.gradle.kts build.gradle.kts ./
    COPY src src
    # Sets $EARTHLY_GRADLE_USER_HOME_CACHE and $EARTHLY_GRADLE_PROJECT_CACHE
    DO gradle+GRADLE_GET_MOUNT_CACHE

build:
    FROM +deps
    RUN --mount=$EARTHLY_GRADLE_USER_HOME_CACHE --mount=$EARTHLY_GRADLE_PROJECT_CACHE gradle --no-daemon build
    SAVE ARTIFACT ./build AS LOCAL ./build
~~~

_[Visit our Earthly lib repo for more pre-built functions and details on how to use them](https://github.com/earthly/lib/tree/main)_

## Sign Up for Earthly Cloud and Start Using Functions Today

![Cloud]({{site.images}}{{page.slug}}/cloud.png)\

You can use Functions with open source Earthly. The easiest way to get Earthly is to [sign up for Earthly Cloud](https://cloud.earthly.dev/login). It walks you through the process of downloading and getting started with Earthly. Earthly Cloud also gives you 6,000 build minutes per month free on Earthly Satellites. Try Functions out, and let us know how they work for you.

{% include_html cta/bottom-cta.html %}
