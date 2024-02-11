---
title: "Monorepos with Cargo Workspace and Crates"
categories:
  - Tutorials
toc: true
author: Kumar Harsh

internal-links:
 - just an example
---

Building software can feel like assembling a complex puzzle, with scattered pieces, intricate dependencies, and evolving needs that can quickly lead to chaos. [Monorepos](https://earthly.dev/monorepos) offer a solution to this problem by consolidating all project code—from core libraries to individual applications—in one centralized location. This approach provides various benefits, including improved code sharing, simplified build processes, and enhanced visibility across the entire codebase.

If you use Rust, you may be wondering how you can translate monorepos into that programming language. Enter [Cargo](https://doc.rust-lang.org/cargo/), Rust's versatile package and build manager. Cargo is the ideal tool for managing dependencies. However, it's best to use Cargo workspaces for larger projects.

Workspaces allow you to organize your codebase into individual crates (representing libraries, binaries, or even tests). Each crate lives within the monorepo, is managed by its own `Cargo.toml` file, and seamlessly integrates with other crates through Cargo's powerful dependency resolution.

In this article, you'll learn all about monorepos, Cargo workspaces, and crates in the context of Rust development. By the end of the article, you'll be able to tame development complexity, foster collaboration, and build robust, maintainable Rust projects within the confines of a single, unified codebase.

## Understanding Cargo Workspaces

Cargo workspaces are a foundational feature for monorepo development in Rust. They function as a container to organize your project's codebase into distinct and optionally interrelated crates. Each crate, whether representing a library, binary, or test suite, maintains its individual identity and purpose within the workspace.

Cargo workspaces establish a collaborative environment where crates can interact, enabling the construction of complex systems without the added complexities of managing multiple repositories. These collaborative environments also act as a centralized knowledge base, with each crate fulfilling a specific role and seamlessly integrating with others. This eliminates the need to navigate multiple repositories or tackle inconsistencies in dependency versions.

In addition to improving code organization and modularity, Cargo workspaces streamline dependency management across multiple projects. Dependencies between crates are declared and managed within the monorepo itself, removing the need to rely on external packages and ensuring uniform versioning across the entire codebase. This approach promotes tighter integration and significantly mitigates the potential for dependency conflicts.

### How to Set Up a Cargo Workspace

Cargo is easy to use. Once you [install Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html), all you need to do is add a `[workspace]` table to a project's `Cargo.toml` file. Then, you define its members like this:

~~~
[workspace]

members = [
    "binary_1",
    "binary_2"
]
~~~

At least one member is mandatory for a workspace to exist. This member can be a root package (with a `[package]` group defined in the same TOML file), or it can be an independent package. If it's an independent package, it's possible to create the root `Cargo.toml` file as a [virtual manifest](https://doc.rust-lang.org/cargo/reference/workspaces.html#the-workspace-section:~:text=is%20called%20a-,virtual%20manifest,-.%20This%20is%20typically) that links to the member packages.

You can add new packages to a workspace by adding them to the `members` list in the workspace-level `Cargo.toml` file. You can also create new binaries and libraries using the `cargo new` command, but you need to manually add their paths to the `members` list if you want to add them as part of the same monorepo.

Some other [workspace-specific settings](https://doc.rust-lang.org/cargo/reference/workspaces.html#the-workspace-section) you can manage under the `[workspace]` group in the root `Cargo.toml` file include:

* `resolver`: Allows you to choose your dependency resolver.
* `exclude`: Lets you exclude particular packages from the workspace.
* `default-members`: Allows you to choose which packages to operate on when a specific package wasn't selected through package selection flags when running Cargo commands.
* `package`: Lets you set keys to be inherited in all packages.
* `dependencies`: Allows you to set keys to be inherited in all package dependencies.
* `lints`: Lets you set keys to be inherited in package lints.
* `metadata`: Allows you to set extra settings for external tools.

## Understanding Crates in Rust

In Rust, a crate serves as a unit of compilation, encapsulating modules, types, and functionalities. It's a foundational element in structuring and organizing code within a Rust project. Acting as a container for logical components, a crate can range from a single file to an entire library with multiple modules, aligning with Rust's commitment to code clarity and maintainability.

Crates also play a vital role in enforcing Rust's ownership and borrowing system. Each crate represents a boundary where ownership rules are enforced, contributing to the language's robust memory safety guarantees. Crates also provide a mechanism for packaging and distributing functionality. Developers can share their crates through Cargo, enabling others to easily integrate and leverage existing solutions.

### Creating and Publishing Crates

Creating and publishing crates with Cargo is easy. You can create new crates using the following commands:

~~~
cargo new crate_name           # for crates with a binary target
cargo new crate_name --lib     # for crates with a library target
~~~

This code creates a new crate with the following file structure:

~~~
|
└── crate_name
    ├── Cargo.toml
    └── src
        └── main.rs   # or lib.rs if you used the --lib flag when creating the crate
~~~

Then, you can edit the `main.rs` file to build the crate as you'd like. When done, don't forget to create documentation for the crate using the `cargo doc` command.

Once you're ready to publish, you need to create an account on [crates.io](https://crates.io/) and verify your email address.

Once you've created your account, log in to your crates.io account in your Cargo CLI by running the following command:

~~~
cargo login
~~~

You'll receive an output like this, asking you to paste an API token found on `https://crates.io/me`:

~~~
please paste the API Token found on https://crates.io/me below
~~~

Paste the API token and press **Enter** to log in. Once you're logged in, you can easily publish crates using the `cargo publish` command. However, there are a few other things you should do before publishing.

To ensure that your crate can be discovered easily on `crates.io`, the [official docs](https://doc.rust-lang.org/cargo/reference/manifest.html#the-manifest-format) recommend specifying the relevant data for the following fields in your crate's `Cargo.toml` file:

* `license` or `license-file`
* `description`
* `homepage`
* `documentation`
* `repository`
* `readme`

In addition, make sure you run the `cargo publish` command with the `--dry-run` flag first to run some basic validations. You can then try building and compiling your crate to check for warnings and errors. If the output from the dry run looks good, you can run `cargo publish` to publish the crate.

## Best Practices for Monorepos with Cargo Workspace and Crates

Navigating the complexity of a monorepo demands strategic organization and planning. You can implement some best practices to help you manage Cargo workspaces and crates.

When it comes to code structuring, keep the following best practices in mind:

* **Modularize your architecture:** Divide your codebase into clearly defined crates with specific functionalities. This practice promotes code reuse, improves maintainability, and facilitates team collaboration.
* **Group and categorize crates:** Consider organizing crates based on their purpose or domain (*eg* UI components, data access layers, business logic). This enhances navigation and fosters understanding of the codebase structure.
* **Maintain consistent naming conventions:** Follow established naming patterns for crates and files to ensure clarity and ease of identification.

Apart from structuring your codebase correctly, another aspect to pay attention to is dependency management. The following are a few best practices you should consider implementing:

* **Pinning dependencies:** Utilize Cargo's [dependency pinning feature](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-dependencies) to lock specific versions of external dependencies across the monorepo. This minimizes build surprises and maintains project stability.
* **Handling versioning conflicts:** Implement a versioning strategy for internal crates to address potential conflicts. Versioning schemes like [semver](https://docs.rs/semver) provide predictability and control over releases and compatibility.

Finally, you should pay attention to continuous integration (CI) and testing in monorepos. A few tips that can help you with that are as follows:

* **Set up automated testing workflows:** Integrate CI tools to automatically run tests on any code change. This enables early detection of regressions and ensures code quality across the entire monorepo.
* **Ensure consistency across multiple projects:** Leverage shared testing frameworks and libraries to guarantee uniformity in testing methodologies and reporting practices across all crates.

## Conclusion

Monorepos with [Cargo workspaces](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html) and crate management in Rust open up a new world of organizational efficiency and code sharing for developers. This article explored the benefits of structuring projects within a monorepo and using Cargo's workspace features.

However, optimizing build performance is equally important. You can significantly enhance your Cargo and Rust build speed by implementing incremental builds. This powerful technique allows for faster iterations and quicker feedback loops during development, contributing to a more streamlined workflow. Make sure to check out Earthly's take on [optimizing Rust build performance with incremental builds](https://earthly.dev/blog/incremental-rust-builds) if you're looking to learn more.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images
* [ ] Verify look of article locally
* [ ] Would any images look better `wide` or without the `figcaption`?
* [ ] Add keywords for internal links to front-matter
* [ ] Run `link-opp` and find 1-5 places to incorporate links
