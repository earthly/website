---
title: "Golang Workspaces"
categories:
  - Tutorials
toc: true
author: Ryan
author2: Josh
last_modified_at: 2023-06-29

sidebar:
  nav: monorepos

internal-links:
 - go workspaces
 - monorepos
 - multiple modules
excerpt: |
    Learn how to simplify your Go development process with Golang Workspaces. This article explores the concept of workspaces and how they can help you manage dependencies across multiple modules in your project, without the need for manual editing of `go.mod` files. Discover how to set up a workspace, make local changes to modules, and ensure that your changes are reflected across all dependent modules.
last_modified_at: 2023-07-19
---
**In this article, we delve into the subtleties of Go workspaces. Earthly simplifies your build process, whether you're managing several modules or beginning your journey. [Learn how](/).**

## The Problem

In a [previous article](/blog/golang-monorepo), we wrote about how you should be using replace in `go.mod` files for modules local to the repository, like in a large monorepo This works because we can safely make assumptions about the organization of the checked-out directory structure. **But what to do when you are working on dependant modules spread across multiple repos?**

For example, say you are working on a project that uses several Golang modules. Each will have their own `go.mod` and their own dependencies. Furthermore, each may have their own repository. Within your project you have a library, maybe a parser for example, that is used in several other modules in your project. You want to do some work on the parser, and then you want to also start using these updates in other modules in your project.

Before Go version 1.18, you'd need to pull the repos locally and then edit each module's `go.mod` with a `replace` to be able to use and test the local changes. That might look something like this:

~~~{.go caption="example mod file"}
module my-module

go 1.18

require github.com/jalletto/parserGo v0.0.2

replace github.com/jalletto/parserGo => ./local-path/parserGo
~~~

This works for small projects, but you still need to remember to remove the replace before pushing your code since you can't be certain other devs will have the same local set up as you. And if you are working on a project with dozens of modules, you can see how this would become cumbersome. These are the problems Go workspaces aim to solve.

## What Are Golang Workspaces?

Go introduced the concept of workspaces in `1.18`. Workspaces allow you to create projects of several modules that share a common list of dependencies through a new file called `go.work`. The dependencies in this file can span multiple modules and anything declared in the `go.work` file will override dependencies in the modules' `go.mod`.

To further illustrate how this works, let's take a look at a simple example. First, we'll set up the project the old way, using `replace`. After that, we'll take a look at how workspaces can improve this process and make our lives easier.

### The Old Way

I have a library with one function in it that adds two numbers together. I want to do some work on that library, and I also want to do some work on a module called `service` that uses that library.

~~~{.go caption="./adder/main.go"}
package adder

func Add(x int, y int) int {
    return x + y
}
~~~

I've set the module path to be a github repo. Let's say this is where the module will live in the future, but for now **I haven't pushed anything**; the module only exists locally.

~~~{.bash caption="./adder/go.mod"}
module github.com/jalletto/adder

go 1.18
~~~

Now, in the same directory, I have another module that uses my adder library.

~~~{.go caption="./service/main.go"}
package main

import (
    "fmt"
    "github.com/jalletto/adder"
)

func main() {
    sum := adder.Add(1, 2)
    fmt.Println("Sum is ", sum)

}
~~~

Here's what my directory looks like to start with.

~~~{.text caption=""}
.
├── adder/
│   ├── go.mod
│   └── adder.go
└── service/
    └── main.go
~~~

Notice I don't have a `go.mod` yet in my service. Let's try to create one.

~~~{.bash caption=">_"}
$ go mod init github.com/jalletto/service

go: creating new go.mod: module github.com/jalletto/service
go: to add module requirements and sums:
        go mod tidy
~~~

That worked and created a `go.mod` as expected.

~~~{.go caption="./service/go.mod"}
module github.com/jalletto/service

go 1.18
~~~

But when we run `go mod tidy` to try to add our requirements we get an error.

~~~{.bash caption=">_"}
go mod tidy

go: finding module for package github.com/jalletto/adder
github.com/jalletto/service imports
        github.com/jalletto/adder: cannot find module providing package github.com/jalletto/adder: module github.com/jalletto/adder: git ls-remote -q origin in /Users/joshalletto/go/pkg/mod/cache/vcs/d8fe82965d5fea8be6f27791ff06a6f2a77b0ca4d1c4921d77852ef26a2d5ba5: exit status 128:
        remote: Repository not found.
        fatal: repository 'https://github.com/jalletto/adder/' not found
~~~

Which you would expect, since we haven't pushed our code yet. If it had existed, it would have pulled it and added it to our `go.mod`. Either way, we want to set up our project to use the local version of `adder`.

Go has had a solution for this for a while. We can use the `replace` flag.

~~~{.bash caption=">_"}
go mod edit -replace github.com/jalletto/adder=../adder
~~~

This will update our `go.mod` file.

~~~{.go caption="./service/main.go"}

module github.com/jalletto/service

go 1.18

replace github.com/jalletto/adder => ../adder

~~~

We can now run `go mod tidy` without getting an error. That will add this line to our `go.mod`.

~~~{.go caption="./service/go.mod"}
require github.com/jalletto/adder v0.0.0-00010101000000-000000000000
~~~

Now we can run our program without error.

~~~{.bash caption=">_"}
$ go run .
Sum is  3
~~~

With this set up we can make changes to our local `adder` library and be sure that they are used when we run `service/main.go`. The main drawback is that we need to remember to remove this line from our `go.mod` before we push.

~~~{.go caption="./service/go.mod"}
replace github.com/jalletto/adder => ../adder
~~~

Not a big deal for this tiny program, but in a large monorepo this is not ideal.

### Refactor With Go Workspaces

To start, I removed the `replace` from `./service/go.mod`. The whole point of workspaces is that we won't be needing to use `replace` for developing locally. In the parent directory, I created a `go.work` file. So now my directory structure looks like this:

~~~{.text caption="we've added the go.work file"}
.
├── adder/
│   ├── go.mod
│   └── adder.go
├── service/
│   ├── go.mod
│   └── main.go
└── go.work
~~~

Then I can run `go work use ./adder`. This will add a line to my `go.work` file.

~~~{.bash caption=">_"}
use ./adder
~~~

And if I try to run my program, it works again!

~~~{.bash caption=">_"}
$ go run ./service/main.go
Sum is  3
~~~

Now I can keep working on my adder library and test it in my service without having to worry about managing multiple `go.mod` files.

<div class="notice--info">

### Don't Push Your Workspace

Remember, workspaces are personal to each developer and should be kept out of the source code. So, add it to your `.gitignore` or delete it before you push changes. Plus, the cool thing is, if I include modules in the workspace that require my `adder` library, they'll default to the local version I'm editing, no need to tweak anything in the `go.mod` of each module.

If you're loving the efficiency of Golang Workspaces, you might want to take it up a notch. If so check out [Earthly](https://www.earthly.dev/) for more streamlined builds. It could be the next tool to add to your developer toolkit.

{% include_html cta/bottom-cta.html %}