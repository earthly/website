---
title: "Creating a Golang Makefile"
categories:
  - Tutorials
toc: true
author: Milap Neupane
author2: Adam
sidebar:
  nav: "makefile"
internal-links:
 - makefile 
 - go makefile
 - golang make
topic: make
excerpt: |
    Learn how to automate repetitive tasks in Golang development using Makefiles. This tutorial covers creating a Makefile to build, run, clean, test, and manage dependencies in your Go projects, making your development process faster and more efficient.
last_modified_at: 2023-07-24
---
**This article teaches you how to automate Golang tasks. Tired of struggling with Makefiles in your Golang projects? Earthly simplifies your build process with strong caching and the ability to run tasks in parallel. [Learn more](/).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/QPfNopc6B_g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Building and testing any large codebase is time-consuming, error-prone, and repetitive. Golang supports multi-platform builds, which is excellent, but it needs multiple commands to build the binaries for different platforms, which means more time-consuming and repetitive steps when building binaries. If that's not enough, most projects have some dependencies that need to be installed before building the binary, and you probably want to run tests and ensure the code quality with linters and code coverage tools.

If this is starting to sound like a nightmare, rest assured: there is an easier way. The utility tool [Make](https://en.wikipedia.org/wiki/Make_(software)) is used to automate tasks. It streamlines development and automates repetitive tasks with a single command. Make helps with testing, building, cleaning, and installing Go projects. In this tutorial, you will learn how you can leverage make and makefiles to automate all those frustrating and repetitive Golang tasks. You will learn how to build, clean, and test a Go sample project using make and a `Makefile`.

## Adding a Makefile To Your Project

To start using make commands, you first need to create a `Makefile` in the root directory of your project. Let's create a simple `hello world` project with a `Makefile` in it.

### `main.go`

```go
package main

import "fmt"

func main() {
 fmt.Println("hello world")
}
```

To run this project, you would normally need to build the project and run the binary:

``` bash
go build main.go
```

If you want a different binary name and also want to create a build for a specific OS, you can specify this during the build:

``` bash
GOARCH=amd64 GOOS=darwin go build -o hello-world main.go
```

You may want the build to create binary for multiple OS. For that, you will need to run multiple commands:

```
GOARCH=amd64 GOOS=darwin go build -o hello-world-darwin main.go
GOARCH=amd64 GOOS=linux go build -o hello-world-linux main.go
GOARCH=amd64 GOOS=windows go build -o hello-world-windows main.go
```

```
go run hello-world
```

The above commands can be simplified using Makefile. You can specify rules to a specific command and run a simple make command. You would not need to remember the commands and the flags or environment variables needed for executing it.

### Makefile

```Makefile
BINARY_NAME=hello-world

build:
 GOARCH=amd64 GOOS=darwin go build -o ${BINARY_NAME}-darwin main.go
 GOARCH=amd64 GOOS=linux go build -o ${BINARY_NAME}-linux main.go
 GOARCH=amd64 GOOS=windows go build -o ${BINARY_NAME}-windows main.go

run: build
 ./${BINARY_NAME}

clean:
 go clean
 rm ${BINARY_NAME}-darwin
 rm ${BINARY_NAME}-linux
 rm ${BINARY_NAME}-windows
```

Now with these simple commands, you can build and run the Go project:

```
make run
```

Finally, you can run the clean command for the cleanup of binaries:

```
make clean
```

These commands are very handy and help to streamline the development process. Now all of your team members can use the same command. This reduces inconsistency and helps to eliminate project build-related errors that can arise with inconsistent manual commands.

## Improving the Development Experience with Makefiles

`make` uses the Makefile as its source of commands to execute and these commands are defined as a *rules* in the Makefile. A single rule defines target, dependencies, and the recipe of the Makefile.

### Terminology

- **Target:** Targets are the main component of a Makefile. The make command executes the recipe by its target name. As you saw in the last section, I used commands like `build`, `run`, and `build_and_clean`. These are called *targets*. Targets are the interface to the commands I want to execute.
- **Dependencies:** A target can have dependencies that need to be executed before running the target. For example, the `build_and_clean` command has two dependencies: `build` and `run`.
- **Recipe:** Recipes are the actual commands that will be executed when the target is run. A recipe can be a single command or a collection of commands. You can specify multiple commands in a target using a line break. In the example above, the recipe for the run target is `./${BINARY_NAME}`. A recipe should always contain a tab at the start.

### Variables

Variables are essential to any kind of script you write. So Makefiles also have a mechanism to use variables. These are useful when you want the same configs or outputs to be used for different targets. In the example above, I have added the `BINARY_NAME` variable, which is reused across different targets.

The variable can be substituted by enclosing it `${<variable_name>}`. I have used the variable in the run command to execute the binary that was created from the build command:

```Makefile
BINARY_NAME=hello-world

run:
 ./${BINARY_NAME}
```

Variables can be defined either by using `=` or `:=`. `=` will recursively expand the variable. This will replace the value at the point when it is substituted. For example:

```Makefile
x = foo
y = $(x) bar
x = later

all:
 echo $(y)
```

When you run the `all` command, it will replace the value of `x` with the last updated value. The value has been changed to `later`, so it will print:

```
> later bar
```

The other kind of variable assignment is `:=`. These are *simple expanded* variables. The variable is expanded at the first scan. So if you assign the variable using this operator, it will print the first value:

```Makefile
x := foo
y := $(x) bar
x := later

all:
 echo $(y)
```

```
> foo bar
```

#### Some Useful Tips

- To make comments in a Makefile, you can simply add a `#` before any line.
- To disable printing the recipe while running the target command, use `@` before the recipe.
- Use the `SHELL` variable to define the shell to execute the recipe.
- Define the `.DEFAULT_GOAL` with the name of the target.

You can also define functions or loops in the Makefile. You can find more details on it [in this make file tutorial](https://makefiletutorial.com).

## Automating Tasks Using Makefile

While developing a project, you will have a lot of repetitive tasks that you might like to automate. In Golang, some of those tasks are testing, running test coverage, linting, and managing dependencies. I will be creating a Makefile that contains all the rules to automate these tasks:

```Makefile
BINARY_NAME=hello-world

build:
 GOARCH=amd64 GOOS=darwin go build -o ${BINARY_NAME}-darwin main.go
 GOARCH=amd64 GOOS=linux go build -o ${BINARY_NAME}-linux main.go
 GOARCH=amd64 GOOS=windows go build -o ${BINARY_NAME}-windows main.go

run: build
 ./${BINARY_NAME}

clean:
 go clean
 rm ${BINARY_NAME}-darwin
 rm ${BINARY_NAME}-linux
 rm ${BINARY_NAME}-windows

test:
 go test ./...

test_coverage:
 go test ./... -coverprofile=coverage.out

dep:
 go mod download

vet:
 go vet

lint:
 golangci-lint run --enable-all
```

With this simple Makefile, you can now easily execute commands to run tasks:

```
make test
make test_coverage
make dep
make vet
make lint
```

**Note:** I am using an external package, [`golangci-lint`](https://github.com/golangci/golangci-lint), for linting. If you are using `go mod`, make sure to add it to your `go.mod` file.

Any CI/CD tool that you are using can now simply use these targets.

## Conclusion

Golang is a popular language for developing large-scale projects. Larger projects have multiple developers and require continuous automation to scale. Streamlining the development process by automating the tasks that are required during development, testing, and release will pay off with a faster and more reliable development process and a easier release process.

{% include_html cta/makefile-cta.html %}

<!-- For next-level automation and to further improve the automation, tools like [Earthly](https://earthly.dev/) can be helpful. If you are also using Docker along with Makefile, Earthly can help make your development process smoother, taking some of the best ideas from Makefiles and Dockerfiles and combining them into one specification. It's also a great solution for [mono-repos](/blog/golang-monorepo). -->