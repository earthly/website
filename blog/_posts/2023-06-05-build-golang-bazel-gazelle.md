---
title: "Building Golang With Bazel and Gazelle"
toc: true
author: Amarachi Aso
editor: Mustapha Ahmad Ayodeji
sidebar:
  nav: "bazel"
internal-links:
 - golang
 - Gazelle
 - bazel
 - Builds
excerpt: |
    Learn how to build Go applications with Bazel and Gazelle, two powerful tools that automate the build process and significantly reduce build times. This tutorial covers the basics of setting up a workspace, running tests, and developing a basic application using Bazel and Gazelle.
last_modified_at: 2023-07-11
categories:
  - bazel
---
**The article examines the combined strengths of Bazel and Gazelle. Earthly's caching mechanisms improve incremental builds and augment Bazel's performance. [Learn more about Earthly](https://cloud.earthly.dev/login).**

[Bazel](https://earthly.dev/blog/bazel-build/), an open source build system created by Google, offers fast and incremental builds for your project through advanced local and distributed caching. It's popular due to its built-in support for multiple languages, extensibility, and ability to scale alongside your codebase, organization, and continuous integration (CI) systems.

Meanwhile, [Gazelle](https://github.com/bazelbuild/bazel-gazelle) is a build file–generation tool specifically designed for Bazel projects. It has native support for Golang (Go) and it can be extended to support new languages and custom rule sets.

Working with Bazel and Gazelle allows you to automate the build process and testing of your Go applications and significantly reduce the time it takes your application to build. This is because Bazel allows you to build only what has changed in your code since the last time you built your application.

In this article, you'll learn about the basics of building Go using Bazel and Gazelle. You'll learn how to prepare a workspace, run, and test it; and how to develop a basic application using Bazel. To follow along, you must be familiar with the basics of Golang and how the Golang build process works. You also need to have the latest version of Go installed on your system.

The code for this tutorial is available in this [GitHub repo](https://github.com/Shulammite-Aso/bazel-demo-app).

## How Go and Bazel Work Together

![Together]({{site.images}}{{page.slug}}/together.png)\

Bazel can be used to build a Go project of any size, and the [`go build`](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) command is often sufficient for small applications. However, if your Go project is considerably large, supports code generation, or is in the same repository as code written in other languages, these variables can add multiple layers of complexity to your build process and the `go build` command might not be sufficient.

For example, with complex projects, you may need to manage more than one build
tool for various sections of your application, or you may be forced to spend too much time rebuilding your whole application every time you implement a new feature. The simple `go build` command cannot work with that level of complexity. However, Bazel can help simplify this process.

Bazel has native support for Go. You just need to load [rules_go](https://github.com/bazelbuild/rules_go#setup), the Go rules for using Bazel, and its dependencies onto your project. It's important that you provide instructions on how to build all the subdirectories in your codebase containing `Go src` files, which can be written in the form of build files that Gazelle will automatically generate. The `rules_go` supports building libraries, binaries, and tests.

## Build and Develop a Go Application with Bazel

In this section, you'll build and develop a Go application with Bazel.

### Install and Set Up Bazel and Gazelle

To install Bazel, follow the [installation instructions](https://bazel.build/install) for your operating system.

Once you've installed Bazel, Gazelle is easy to install. You just need to open a terminal and run the following command:

~~~{.bash caption=">_"}
go install github.com/bazelbuild/bazel-gazelle/cmd/gazelle@latest
~~~

After installation, prior to running any `gazelle` commands, you need to make sure that your `GOPATH/bin` is added to `$PATH`. On Linux, you can do this with the following command:

~~~{.bash caption=">_"}
export PATH="$PATH:$HOME/go/bin/"
~~~

Adding `GOPATH/bin` to `$PATH` is needed to ensure that the gazelle command can be executed from anywhere on your system without specifying the full path to the executable. `GOPATH/bin` is where gazelle is installed after you run `go install github.com/bazelbuild/bazel-gazelle/cmd/gazelle`

However, this will only stay valid while your current terminal session is still in use. Make sure you rerun this command after you close and reopen your terminal, or for a permanent solution, add `GOPATH/bin` to `$PATH` [permanently](https://phoenixnap.com/kb/linux-add-to-path).

### Set Up the Project and Generate Build Files

![Generate]({{site.images}}{{page.slug}}/generate.png)\

The Go project you'll be creating is a build process for a simple web application. It depends on a package `greetings` that returns a simple greeting or a map of greetings to different names.

The following is the directory structure for this application:

<div class="wide">
![Go project directory structure]({{site.images}}{{page.slug}}/xKxuN5O.png)
</div>

Download the starting project from this [GitHub branch](https://github.com/Shulammite-Aso/bazel-demo-app/tree/before-bazel).

Or clone the repository and checkout to the branch `before-bazel` with the following command:

~~~{.bash caption=">_"}
git clone https://github.com/Shulammite-Aso/bazel-demo-app.git \
&& cd bazel-demo-app && git checkout before-bazel
~~~

Once downloaded, it's time to prepare the project for building with Bazel. To do so, create a `WORKSPACE` file on the root directory of this project. The existence of the `WORKSPACE` file lets Bazel know that the current directory is a Bazel project. The `WORKSPACE` file is also used to load project-specific dependencies and settings. Insert the following [Starlark code](https://bazel.build/rules/language) in the `WORKSPACE` file:

~~~{ caption="WORKSPACE.bazel"}

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "io_bazel_rules_go",
    sha256 = "56d8c5a5c91e1af73eca71a6fab2ced959b67c86d12ba37feedb0a2dfea441a6",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.37.0/rules_go-v0.37.0.zip",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.37.0/rules_go-v0.37.0.zip",
    ],
)

http_archive(
    name = "bazel_gazelle",
    sha256 = "ecba0f04f96b4960a5b250c8e8eeec42281035970aa8852dda73098274d14a1d",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.29.0/bazel-gazelle-v0.29.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.29.0/bazel-gazelle-v0.29.0.tar.gz",
    ],
)


load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", \
"go_rules_dependencies")
load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies", "go_repository")

############################################################
# Define your own dependencies here using go_repository.
# Else, dependencies declared by rules_go/gazelle will be used.
# The first declaration of an external repository "wins".
############################################################

go_rules_dependencies()

go_register_toolchains(version = "1.19.5")

gazelle_dependencies()
~~~

This code loads Bazel and Gazelle, as well as their dependencies, into your workspace. You can also find this code in the [Gazelle documentation](https://github.com/bazelbuild/bazel-gazelle#setup).

The following comment is seen in the Starlark code you just put into your `WORKSPACE` file:

~~~{ caption="WORKSPACE.bazel"}

############################################################
# Define your own dependencies here using go_repository.
# Else, dependencies declared by rules_go/gazelle will be used.
# The first declaration of an external repository "wins".
############################################################
~~~

As the comment suggests, you need to manually define or tell Bazel where it can find and download the external dependencies used in your project. You can define these dependencies manually using [`go_repository`](https://github.com/bazelbuild/bazel-gazelle/blob/master/repository.md#:~:text=go_repository%20downloads%20a%20Go%20project%20using%20either%20go%20mod%20download), or you can use Gazelle to define them (which you'll do later in this tutorial).

Now you need to generate `BUILD` files for your `src` codes. In Bazel, every subdirectory containing `src` code can only be built when it contains a `BUILD` file named `BUILD` or `BUILD.bazel`.When a directory has this file, it's considered a package by Bazel and can be built according to the instructions in the `BUILD` file.

Instead of manually creating and writing these files, you can generate them with Gazelle by running the following command from the root of your project and replacing `github.com/example/project` with the name of your project, which you can find in your `go.mod` file:

~~~{.bash caption=">_"}
gazelle -go_prefix github.com/example/project
~~~

Once you run the previous command, you should have a `BUILD.bazel` file in all the subdirectories in your workspace. If you wish to double-check, examine the `BUILD` files and confirm that they import and define `go_library`, `go_binary`, and `go_test` as you would by hand when following the [guide](https://bazel.build/concepts/build-files) for writing `BUILD` files.

### Build Your src Files and Run the Application

To build your `src` files, run the following Bazel command from the root of your project:

~~~{.bash caption=">_"}
bazel build //...
~~~

You should get this error:

~~~{ caption="Output"}

no such package '@com_github_gorilla_mux//': \
The repository '@com_github_gorilla_mux' could not be resolved: ……
~~~

This error message tells you that Bazel could not locate the package `github.com/gorilla/mux` because `gorilla/mux` is an external package, and there is no definition of how or where to load the package from.

Again, instead of writing this definition by hand, Gazelle can look into the `go.mod` file, find the path to all the external dependencies, and generate a `.bzl` file that contains a definition of your external dependencies.

To define your external dependencies, you'll use the `gazelle update-repo` command. The flags on the following command tell Gazelle to import repositories from `go.mod`, update macro, and remove the `go_repository` rules that no longer have equivalent repos in the
`Gopkg.lock/go.mod` file. You need to run this command from the root of your project:

~~~{.bash caption=">_"}
gazelle update-repos -from_file=go.mod \
-to_macro=deps.bzl%go_dependencies -prune
~~~

This will create the file `deps.bzl` on the root directory.

Then run `bazel build //...` again. You should find that the previous error has been resolved; however, you'll experience another issue:

~~~{ caption="Output"}
ERROR: Error computing the main repository mapping: \
Every .bzl file must have a corresponding package, \
but '//:deps.bzl' does not have one. Please create a \
BUILD file in the same or any parent directory. Note \
that this BUILD file does not need to do anything except exist.
~~~

This tells you that you need to create a `BUILD` file in the same directory as the generated `deps.bzl` file. This file doesn't need to do anything but exist, and you can create it with the following command:

~~~{.bash caption=">_"}
touch BUILD.bazel
~~~

Rerun `bazel build //...`, and you should find that your build is running successfully.

In your project, a test has been written for the package `greeting`. Run the test on the `greeting` package with the following command:

~~~{.bash caption=">_"}
bazel test //...
~~~

Your test should pass with the following output:

<div class="wide">
![Test output]({{site.images}}{{page.slug}}/0uY3I6v.png)
</div>

Before you finish, run your application with this Bazel command:

~~~{.bash caption=">_"}
bazel run //cmd
~~~

This web application should now run with a log output on the terminal that says the following:

~~~{.bash caption=">_"}
server started at port :5000
~~~

You can visit [http://localhost:5000/greet](http://localhost:5000/greet) and [http://localhost:5000/greet-many](http://localhost:5000/greet-many) to receive your greetings.

## Conclusion

In this tutorial, you learned how Bazel and Gazelle can be used to build a Go application. You learned how to prepare the workspace, how to run the test, and how to develop a basic application using Bazel.

Bazel and Gazelle help simplify the build process in cases where there would have been multiple complex layers. In addition, it's also significantly faster to build with Bazel since it doesn't have to rebuild your whole project every time it runs.

Yet, while Bazel is a fantastic tool for building apps, and Gazelle a great tool for generating those build files, the combination can also be complex and intricate. It may be overkill for smaller projects or for teams that aren't familiar with its intricacies. That's where [Earthly](https://cloud.earthly.dev/login) comes into the picture.

Earthly offers a simpler approach to building monorepos and containerization, focusing on streamlining the build process, maintaining a minimal setup, and promoting the use of best practices. It aims to simplify the build system and make it accessible for more developers, offering a potentially lower learning curve compared to Bazel. [Earthly](https://cloud.earthly.dev/login) can handle both small and large projects, offering you scalability without the additional complexity.

{% include_html cta/bottom-cta.html %}
