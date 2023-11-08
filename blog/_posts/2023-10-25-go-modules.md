---
title: "Understanding Go Package Management and Modules"
categories:
  - Tutorials
toc: true
author: Israel Ulelu

internal-links:
 - what is go package management
 - what is go package modules
 - how to use go package modules
 - how to use go package management 
last_modified_at: 2023-10-20
excerpt: |
    This article provides a comprehensive guide to Go package management and modules. It explains the benefits of using Go modules, introduces essential commands and workflows, and offers tips and best practices for efficient package management.
---
<!--sgpt-->**Meet [Earthly](https://earthly.dev/). We simplify and speed up building software with containerization. If you're working with Go Modules, Earthly could be your perfect build tool companion for your Continuous Integration tasks. [Give us a look](/).**

[Go](https://go.dev/), often referred to as Golang, is an open source programming language that offers a unique blend of attributes, including efficiency, performance, simplicity, and readability. Go also embraces the principle of reusability, promoting a programming model where developers can seamlessly organize, distribute, and recycle preexisting code. This process, facilitated by Go's package management system, encourages developers to effortlessly incorporate external packages and libraries into their projects. This approach considerably mitigates the need to reinvent the wheel for routine functionalities, streamlining the development process and promoting code efficiency.

Go [modules](https://go.dev/blog/using-go-modules), introduced in Go v1.11, address the limitations and complexities experienced with package management processes in previous versions by offering a streamlined method for defining, versioning, and managing project dependencies.

In this article, you'll learn all about the intricacies of package management and modules within the Go programming language.

## What Are Go Modules

Go modules are a solution for dependency management that lets you specify the exact versions of external packages your project needs. This means that when you use those packages in a new setup, everything will work the way it's intended to.

Go modules help with:

- **Versioning:** Go modules enable developers to explicitly declare the version of a package that their project relies upon. This versioning information is stored in a `go.mod` file within your project.
- **Dependency management:** Go modules automatically download and resolve project packages and their dependencies, preventing conflicts and ensuring projects use compatible package versions.
- **Checksums:** The go.mod file tracks your project's dependencies and their versions, while the go.sum file ensures the integrity of these dependencies by storing cryptographic checksums. This guards against unauthorized or unexpected modifications to the packages.

## Go Modules: Commands and Workflow

In Go, package management is executed via the command line tool using the `go` command. Here are some frequently used commands integral to package management in Go:

### `go get`

The `go get` command is used to add, update, or remove packages as well as their dependencies. It also updates the `go.mod` file to reflect the new dependencies.

The syntax for the `go get` command is the words `go` and `get`, followed by the package path:

~~~{.bash caption=">_"}
go get [package_path]
~~~

### `go install`

The `go install` command is used to build and install executables. It was introduced in [Go 1.17](https://go.dev/doc/go-get-install-deprecation), streamlining `go get` to the sole task of adding and modifying dependencies. To install an executable, run the `go install` command, followed by the package path:

~~~{.bash caption=">_"}
go install [package_path]
~~~

### `go mod init`

The `go mod init` command creates and initializes a new module. On execution of the command, a `go.mod` file is created to manage all project dependencies and versions:

~~~{.bash caption=">_"}
go mod init [module_name]
~~~

### `go mod tidy`

On execution of the `go mod tidy` command, the import statements of all project files are analyzed and the `go.mod` file is updated to include only the packages used in your code:

~~~{.bash caption=">_"}
go mod tidy
~~~

### `go list`

The `go list` command lists packages and modules contained in your project. The `go list` command also accepts flags and arguments such as `-m` and `-m all`, which streamlines the command to packages in the current module:

~~~{.bash caption=">_"}
go list
~~~

### `go mod vendor`

The `go mod vendor` command creates a self-contained project with all its dependencies stored locally. On execution of this command, a vendor folder containing copies or clones of all the packages used in the project is created:

~~~{.bash caption=">_"}
go mod vendor
~~~

### `go mod verify`

The `go mod verify` command verifies the integrity of the packages and dependencies by comparing the checksums in the `go.sum` file:

~~~{.bash caption=">_"}
go mode verify
~~~

Now that you've familiarized yourself with some of the core commands for Go modules, create and initialize a Go module.

## Initializing Go Modules

To initialize a new Go module, create a new folder on your device to store your project file.

Then open a new terminal window targeting the recently created folder. Execute the `go mod init` command accompanied by your preferred module path, which functions as the module's identifier. It's recommended that the module path be the repository location of your source code:

~~~{.bash caption=">_"}
go mod init example.com/package_management_in_go
~~~

After you run this command, you can expect a printout resembling the following to be displayed in your terminal:

~~~{ caption=">Output"}
$ go mod init example.com/package_management_in_go 
go: creating new go.mod: module example.com/package_management_in_go
~~~

This command equally generates a `go.mod` file designed to track your project dependencies and external packages. On generation, the file only includes your module name and Go version:

<div class="wide">
![`go mod` content]({{site.images}}{{page.slug}}/6bV8z9O.png)
</div>

## Introducing Dependencies

As you begin to integrate new dependencies into your project, the `go.mod` dynamically updates to keep track of these dependencies and their corresponding versions. So introduce a new dependency in your project to observe changes in the `go.mod` file.

For the purpose of this article, the [gorm](https://pkg.go.dev/gorm.io/gorm) package is introduced as a dependency. To initiate this process, execute the following command in your terminal:

~~~{.bash caption=">_"}
go get gorm.io/gorm
~~~

Your output should look like this:

~~~{ caption="Output"}
$ go get gorm.io/gorm
go: downloading gorm.io/gorm v1.25.4
go: downloading github.com/jinzhu/now v1.1.5
go: added github.com/jinzhu/inflection v1.0.0
go: added github.com/jinzhu/now v1.1.5
go: added gorm.io/gorm v1.25.4
~~~

Additionally, the content of your `go.mod` automatically updates to reflect the gorm package. This update not only includes the gorm package itself but also encompasses its dependencies along with their respective versions. This update manifests as a requirement for your project like this:

<div class="wide">
![`go mod` content after adding gorm]({{site.images}}{{page.slug}}/cqoW7D3.png)
</div>

The `go.sum` file is equally generated on the addition of your first dependency. This file serves as a comprehensive record, capturing not only the dependencies themselves but also crucial information like version identifiers and cryptographic checksums:

<div class="wide">
![`go.sum` content]({{site.images}}{{page.slug}}/ZgvCF2h.png)
</div>

## Modifying Dependencies

It's also possible to precisely define or modify the preferred version of a dependency for integration into your project. This can be achieved by indicating the intended version within the scope of the `go get` command. The execution of this command triggers an update of the `require` directive in the `go.mod` file, solidifying the dependency's version.

Alternatively, you can manually edit the `go.mod` file; however, it's recommended to use the `go get` command approach. Specifying the preferred version might prove particularly useful when experimenting with a prerelease iteration of a package or reverting to a prior version in cases where the current version presents compatibility issues with your project.

In the previous example, you installed the gorm package. In this section, you'll modify the dependency version of the gorm package.

To define a particular version of the gorm package for utilization, simply execute the following command within your terminal, attaching the corresponding version as a suffix:

~~~{.bash caption=">_"}
go get gorm.io/gorm@v1.20.0
~~~

Your output looks like this:

~~~{ caption="Output"}
$ go get gorm.io/gorm@v1.20.0
go: downgraded gorm.io/gorm v1.25.4 => v1.20.0
~~~

On execution of the command, the `go.mod` and `go.sum` files automatically update to reflect the specified version:

<div class="wide">
![`go mod` file after downgrade]({{site.images}}{{page.slug}}/5w6HrAR.png)
</div>

<div class="wide">
![`go sum` file after downgrade]({{site.images}}{{page.slug}}/33lXIBl.png)
</div>

Now that you know how to create Go modules and efficiently manage dependencies and packages, let's take a look at a few tips and tricks that can help you along the way.

## Go Package Management: Tips and Best Practices

Outlined subsequently are a series of essential tips and recommended practices developers can use to effectively manage project packages with Go modules:

### Package Files With Integrity

When it comes to security, necessary attention should be given to the `go.sum` file to ensure package integrity. Vigilantly review changes in the `go.sum` file and, whenever feasible, steer clear of manually altering its contents.

Additionally, you should perform periodic reviews of security advisories for your project's dependencies. By adhering to these practices, you bolster the safeguarding of your project's codebase and enhance its overall security.

### Commit `go.mod` and `go.sum` to Your Version Control System

To maintain consistency and reproducibility across diverse environments, it's imperative that you commit both the project's `go.mod` and `go.sum` files to your version control system. This practice safeguards against discrepancies and ensures that the exact versions of dependencies are utilized, regardless of the development environment.

### Document and Track Changes

Following [semantic versioning](https://semver.org) principles ensures that version changes accurately reflect the nature of code modifications. Similarly, robust documentation practices that track and detail changes in each model version, clarify the purpose of each dependency, and outline how they're being used is crucial. This not only aids in preserving code compatibility but also establishes a clear communication channel for developers regarding changes, updates, and potential impacts.

### Regularly Update Your Dependencies

You need to regularly update the dependencies of your project to their latest compatible versions. This practice ensures that your project remains current with security enhancements, bug fixes, new functionalities, and performance optimizations.

However, When you update dependencies, it's possible that the new versions of those dependencies may introduce changes that affect how your code functions, possibly changing its semantics. While it's important to regularly update dependencies for security and feature benefits, developers should exercise caution and follow Semantic Versioning principles to minimize unexpected changes in code semantics.

### Test and Maintain Module Compatibility

In addition to regularly updating your dependencies, you need to conduct periodic and systematic tests to ensure uninterrupted compatibility. The implementation of automated unit and integration testing is strongly recommended, as it serves as a robust mechanism for detecting any latent issues at an early stage.

## Conclusion

Go modules offer an effective resolution to the intricacies surrounding package management within the Go programming language. In this article, you learned all about the nature of Go modules and the pivotal roles of the `go.mod` and `go.sum` files.

By fully embracing Go modules and diligently adhering to the best practices outlined in this article, you can confidently navigate the realm of package management, whether engaged in modest-scale projects or complex, large-scale applications.

{% include_html cta/bottom-cta.html %}
