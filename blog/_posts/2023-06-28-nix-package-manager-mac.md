---
title: "How to Use Nix Package Manager on Mac"
categories:
  - Tutorials
toc: true
author: David Chibueze Ndubuisi
editor: Mustapha Ahmad Ayodeji

internal-links:
 - just an example
---

**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster – like Dockerfile and Makefile had a baby. This article shows use how to use Nix package manager on Mac.**

As a Mac user, you've likely used [Homebrew](https://brew.sh/) at some point, the beloved package manager that makes it easy to install and manage software packages on macOS. But have you ever felt like there must be a better way to manage your software packages? Introducing [Nix](https://nixos.org), a powerful package manager Nix is a powerful package manager that makes package management reliable and reproducible.

With Nix, you define the set of packages and their versions that you want to install, and Nix takes care of the rest. This approach allows for greater flexibility, reproducibility, and reliability, in managing system configurations, as Nix ensures that the specified set of packages and their versions are installed consistently across all systems. Additionally, the ability to roll back to a previous configuration in case of errors or updates adds an extra layer of reliability to Nix's management process.

Nix's unique approach to package storage (which will be discussed in a bit) sets it apart from other package managers like Homebrew, making it ideal for managing multiple versions of the same package without fear of conflicts. With Nix, you can easily install, remove, and update packages on your Mac, and have the added benefit of being able to revert to previous configurations if things go wrong. In this article, we'll explore what Nix is, how it differs from Homebrew, and how to install and use it on your Mac. Whether you're a seasoned package manager user looking for a more flexible solution, or just starting, Nix is worth a closer look.

## Nix Comparison With Homebrew Package Manager

In this section, we will compare Nix with Homebrew. We will start by providing a brief explanation of what package managers are and their role in software management. Then, we'll delve into the differences between Nix and Homebrew, highlighting the unique features and advantages that Nix offers over Homebrew.

### Package Managers

Package managers are vital tools for developers and users alike, as they simplify the process of installing, updating, and managing software packages. A package manager is a software tool that automates installing, updating, and removing software packages on a computer. With a package manager, users can easily search for and install software packages, without the need to manually download and install each package individually. If you're interested in a more in-depth discussion of package managers, check out this [page on Wikipedia](https://en.wikipedia.org/wiki/Package_manager).

### Difference Between HomeBrew and Nix

One of the key differences between Homebrew and Nix is how they handle package creation, storage, and management. Homebrew uses a [formula system](https://docs.brew.sh/Formula-Cookbook), where each package is defined by a formula file that specifies how to download, compile, and install the package. Nix, on the other hand, uses a functional programming language – called [Nix Expression Language](https://nixos.org/manual/nix/stable/#chap-writing-nix-expressions) – to define packages, making it easier to manage dependencies and ensure package compatibility.

Another significant difference between Homebrew and Nix is how they handle multiple versions of the same package. Homebrew only allows for one version of a package to be installed at a time, while Nix can manage multiple versions of the same package concurrently. This feature is particularly useful for developers who need to test their software against different versions of a library or package.

Both Homebrew and Nix have their strengths and weaknesses, and the choice of which one to use depends on your specific needs. For users looking for a straightforward package manager, Homebrew is a great option. On the other hand, Nix's unique approach to package management and built-in error-handling features make it a powerful choice for those who prioritize flexibility and reliability.

### Different Approaches to Package Creation in Nix and Homebrew

Creating packages with Homebrew and Nix follows different approaches. With Homebrew, creating a package involves writing a [Ruby script known as a formula](https://docs.brew.sh/Formula-Cookbook). The formula specifies where the package can be found, how it should be installed, and any dependencies that need to be resolved. The formula is then added to a repository - a centralized collection of formulas that have been contributed by developers and users, where it can be easily accessed and installed by other users.

For example, let's consider the [`imagemagick`](https://imagemagick.org/index.php) package in Homebrew. The formula for `imagemagick` is defined in a Ruby script that specifies the source URL, dependencies, and installation instructions. Here's an excerpt from the formula:

~~~
class Imagemagick < Formula
  desc "Tools and libraries to manipulate images in many formats"
  homepage "https://imagemagick.org/"
  url "https://imagemagick.org/download/releases/ImageMagick-7.1.0-3.tar.xz"
  sha256 "94d8c2f1b9c04b310aa4e4d4a80bae6a58a6a2b6d23c6a9b6c9b6edec50f9047"
  license "ImageMagick"

  depends_on "pkg-config" => :build
  depends_on "jpeg"
  depends_on "libheif"
  depends_on "libpng"
  depends_on "libtiff"
  depends_on "little-cms2"
  depends_on "openexr"
  depends_on "webp"
  depends_on "xz"
  ...
~~~

The above code is a Ruby class definition for the `Imagemagick` formula in Homebrew, a package manager for macOS. Let's break down the code:

- `class Imagemagick < Formula`: This line defines a Ruby class named "Imagemagick" that extends the functionality of the "Formula" class in Homebrew. It represents the formula for the `Imagemagick` package.
- `desc "Tools and libraries to manipulate images in many formats"`: This line provides a brief description of the `Imagemagick` package, stating that it provides tools and libraries for manipulating images in various formats.
- `homepage "https://imagemagick.org/"`: This line specifies the homepage URL for the `Imagemagick` project, which is the official website where users can find more information about the package.
- `url "https://imagemagick.org/download/releases/ImageMagick-7.1.0-3.tar.xz"`: This line indicates the download URL for the Imagemagick source code. The package manager will use this URL to retrieve the source code when installing Imagemagick.
- `sha256 "94d8c2f1b9c04b310aa4e4d4a80bae6a58a6a2b6d23c6a9b6c9b6edec50f9047"`: This line specifies the SHA-256 checksum of the downloaded source code. It ensures the integrity and authenticity of the downloaded file.
- `license "ImageMagick"`: This line states the license under which the `Imagemagick` package is distributed. In this case, the license is simply referred to as "ImageMagick."
- `depends_on lines`: These lines specify the dependencies required by the `Imagemagick` package. Each `depends_on` line indicates a specific package or library that must be installed before `Imagemagick` can be successfully built and used. In the provided example, there are several dependencies listed, such as `jpeg`, `libheif`, `libpng`, and others.

The above code is a Ruby class definition for the `Imagemagick` formula in Homebrew. It describes a package that provides tools and libraries for image manipulation in various formats. The formula specifies the package's homepage URL, download URL, `SHA-256` checksum, and license. It also lists the dependencies required by the package, such as jpeg, `libheif`, `libpng`, and others. The code serves as a blueprint for installing and managing the `Imagemagick` package using Homebrew.

In contrast, Nix packages are defined using a functional programming language called the [Nix Expression Language](https://nixos.org/manual/nix/stable/#chap-writing-nix-expressions). These expressions define the package dependencies, source code, build instructions, and configuration options. The Nix Expression Language allows for the creation of highly reproducible packages, as each package is defined in a determined way. This reproducible packages means that two users who create the same package using the same Nix expression will end up with identical packages.

For example, let's consider the `imagemagick` package in Nix. The expression for `imagemagick` specifies the source URL, dependencies, and build instructions. Here's an excerpt from the expression:

~~~
{ stdenv, libjpeg, libheif, libpng, libtiff, lcms2, openexr, webp }:

stdenv.mkDerivation rec {
  pname = "imagemagick";
  version = "7.1.0-3";

  src = fetchurl {
    url = "https://imagemagick.org/download/releases/ImageMagick-${version}.tar.xz";
    sha256 = "0fg9anxz7brhswprjjf2lz8wcmwcyddyl7s85h1s0f7sy91py37d";
  };
  buildInputs = [ libjpeg libheif libpng libtiff lcms2 openexr webp ];
  …
~~~

The above code is a Nix expression that defines a derivation for the `Imagemagick` package. It specifies a set of dependencies required for the package, including `libjpeg`, `libheif`, `libpng`, `libtiff`, `lcms2`, `openexr`, and `webp`. The `src` attribute specifies the URL and SHA-256 checksum of the package source code. The derivation is created using `stdenv.mkDerivation`, which sets the package's name to `"imagemagick"` and its version to "7.1.0-3". This code serves as a blueprint for building and installing the `Imagemagick` package using the Nix package manager.

In general, both approaches have their strengths and weaknesses. Homebrew's formula system allows for the easy creation and distribution of packages, and its use of Ruby in its formula system has the advantage of making it accessible to a wide range of developers. However, creating a formula can be overly complex for those who are not familiar with the Ruby scripting language.

Nix's functional programming approach provides a high degree of flexibility and reproducibility, making it ideal for managing complex system configurations. However, the learning curve for Nix expression language can be steep for some users, as it requires familiarity with [functional programming](https://en.wikipedia.org/wiki/Functional_programming) concepts. This can be challenging for developers who are used to [imperative programming languages](https://learn.microsoft.com/en-us/dotnet/standard/linq/functional-vs-imperative-programming). This may result in users spending more time learning how to use Nix effectively. Additionally, Nix does not have a centralized package repository like Homebrew, which can make it more difficult to discover and distribute packages. As a result, users may need to spend more time finding the packages they need.

### Package Storage

Both Homebrew and Nix have different approaches to package storage on Mac systems. Homebrew stores packages in the `/usr/local/Cellar` directory and creates [symbolic links](https://en.wikipedia.org/wiki/Symbolic_link) (symlink) in the `/usr/local/bin` directory for easy access. This means that each package has its directory in Cellar, and when you install a package, Homebrew creates a symlink to the package's executable file in `/usr/local/bin`.

On the other hand, Nix uses a content-addressable storage system to manage packages. The content-addressable storage system means that the package's location is unique and predetermined based solely on its contents. When a package is installed, it is stored in a unique directory within the `/nix/store`. This directory is named after the hash of the package contents, which means that the package's location in the file system is predetermined and based solely on its contents. Nix also creates a symlink to the package's executable file in `/nix/var/nix/profiles/default/bin`, which allows you to access the package from anywhere in your system. Nix's approach to package storage provides a more comprehensive solution than Homebrew, providing greater stability, security, and flexibility for Mac users.

While Homebrew's approach to package storage is more straightforward due to how it stores packages in a centralized repository making it easier for users to access and install them, Nix's unique hash-based approach offers some distinct advantages, such as package immutability, meaning that packages cannot be changed once they are installed. This ensures that packages remain in a consistent state and helps to prevent unintentional modifications. Additionally, Nix's management of multiple package versions is more flexible and efficient than Homebrew's. With Nix, each version of a package has its own unique hash and can be installed alongside other versions without conflict. This allows for greater control and organization, making it easier to manage different versions of packages and switch between them as needed. Ultimately, Nix's approach to package storage and version management offers a more comprehensive solution than Homebrew, providing greater stability, security, and flexibility for Mac users.

### Handling Multiple Versions

One of the key features of package managers is the ability to handle multiple versions of the same package. This is particularly important when working with software that has multiple dependencies or is being used by multiple projects.
Homebrew and Nix take different approaches to handling multiple versions of packages. Homebrew uses a [system of "kegs"](https://docs.brew.sh/FAQ#what-does-keg-only-mean) to manage multiple versions of packages.

<div class="notice--info">
A keg is a versioned directory within the Cellar where each package is installed. It has a unique identifier that comprises the package name, version, and Git commits hash. Symbolic links to the package binaries are created in `/usr/local/bin` by Homebrew to enable easy access to the package from the command line.
</div>

The content-addressable approach of NIX discussed earlier makes it easy to have multiple versions of the same package installed side-by-side since each version will have a unique hash and therefore a unique directory in the store. This approach allows for greater control and organization, making it easier to manage different versions of packages and switch between them as needed.

In simpler terms, Homebrew, and Nix have different ways of managing multiple versions of packages. Homebrew uses kegs, which are versioned directories, while Nix uses a content-addressable storage system, which stores packages in unique directories based on their contents. Both methods provide robust mechanisms for handling multiple versions of packages.

It's important to handle multiple versions of packages because different software or projects may require different versions of the same package. For example, one project may require an older version of a package while another may need a newer version. Without the ability to handle multiple versions, it can be difficult to manage dependencies and ensure that each project or software is using the appropriate version of the package.

## Installing Node.js on a Mac: A Comparison of Homebrew and Nix Package Managers

In this section, we'll walk through the step-by-step process of installing Node.js, a popular JavaScript runtime that allows developers to build scalable and efficient web applications, using both Homebrew and Nix package managers on a Mac, highlighting the differences in approach between the two. Whether you're new to package management or looking to switch to a new system, this example will provide valuable insight into the benefits and drawbacks of each package manager.

### Homebrew

1. Install Homebrew by opening the terminal and running the following command:

    ~~~
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ~~~

2. Run `brew -v` to verify that Homebrew is installed correctly. If it is installed correctly, you should see the version number displayed.

    <div class="notice--info">
    If you do not see the version number, here are some troubleshooting tips you can try:

    - Ensure that you have correctly installed Homebrew by running the installation command again.

    - If you still can't see the version number, check your PATH environment variable to make sure that `/usr/local/bin` is included. You can do this by running:

    ~~~
    echo $PATH
    ~~~

    If `/usr/local/bin` is not included in the output, add it to your `PATH` by adding the following line to your shell profile file (e.g. `~/.bash_profile` or `~/.zshrc`):

    ~~~
    export PATH="/usr/local/bin:$PATH"
    ~~~

    - If `/usr/local/bin` is already in your `PATH` but you still can't see the version number, try restarting your terminal or shell session.
    - If you continue to experience issues, you can check the [Homebrew documentation](https://docs.brew.sh/) or ask for help on the [Homebrew GitHub repository or forum](https://github.com/orgs/Homebrew/discussions).

    </div>
3. Once Homebrew is installed, run the following command to install the latest version of Node.js:

    ~~~
    brew install node
    ~~~

4. To install a specific version of Node.js, in this case, version `16.x`, use the following command:

    ~~~
    brew install node@16
    ~~~

5. To switch between installed versions of Node.js, use the following command:

    ~~~
    brew unlink node && brew link node@16
    ~~~

This will unlink the current version of Node.js and link version `16.x` instead.
In the example we just followed, we installed Nodejs using the Homebrew package manager. Throughout the steps, we saw how Homebrew made it easy to install and manage Node.js by using simple commands in the terminal, such as `brew install node` and `brew link node@16`.

### Nix

1. Install Nix by opening the terminal and running the following command:

    ~~~
    sh <(curl -L https://nixos.org/nix/install)
    ~~~

2. Run: `nix-env --version` to ensure that Nix is installed correctly. If it is, you should see the version number displayed.

    <div class="notice--info">
    If you don't see the version number displayed, it could indicate that Nix was not installed correctly. In this case, some troubleshooting tips include:
    - Check if there are any error messages displayed during the installation process and try reinstalling Nix.
    - Ensure that you have installed the prerequisites for Nix, such as a C++ compiler and the Bash shell.
    - Check if there are any issues with your system's network configuration, as Nix requires a stable internet connection to download packages.

    - Check the [Nix documentation](https://nixos.org/learn.html) or [community forums](https://nixos.org/community/) for any known issues or solutions related to your specific operating system or version.
    </div>

3. Once Nix is installed, you can follow the following steps to install the latest version of Node.js:

    ~~~
    nix-env --install --attr nodejs
    ~~~

    You can verify the installation by running `node –version`, this will display
    the latest version of Nodejs installed on your Mac.

4. To install a specific version of Node.js, use the following command:

    ~~~
    nix-env --install --attr nodejs-16
    ~~~

    This will install version `16.x` of Node.js.

5. To switch between different Node.js versions, for example, `node 16.x`, you can run the following command:

    ~~~
    nix-env --switch --use-nodejs-16
    ~~~

In the example we just followed, we installed Node.js using the Nix package manager on a Mac. By using Nix to manage Node.js versions, the user can ensure that their builds are reproducible and can easily switch between different versions of Node.js as needed.

## Using the Nix Package Manager

Now that you have successfully installed Nix on your Mac, this section will focus solely on exploring its powerful features. We will dive into how to use Nix to search for and install packages, handle multiple versions of the same package, upgrade, and remove packages, and effectively use them in your workflow. So let's get started!

### Searching for Packages With Nix

Before you can install a package with Nix, you need to ensure that it is available. To search for available packages on the Nix repository, you can use the `nix-env` command, which is an essential tool for package management using the Nix package manager. Apart from installing and managing packages, `nix-env` also allows you to search for available packages that you may want to install on your system. So, to search for the Node.js package, for example, you would run:

~~~
nix-env -f '<nixpkgs>' -P -A nodejs
~~~

Here is the explanation of the syntax of the above command:

- `nix-env`: This is the command for managing packages with Nix.
- The `-f` flag specifies a file to use as the input for the command. In this case, the `<nixpkgs>` argument specifies the Nixpkgs repository as the source for the package information. Since the Nixpkgs repository is the default source for packages in Nix, the `-f` flag is not strictly necessary. However, it can be useful if you want to use a different source for packages. If you omit the `-f` flag, Nix will assume that you want to use the default source.
- `-P`: This flag is used to displays the full name of the `nodejs` package, including its version number.
- `-A`:  This flag is used to specify the attribute name of the package, which in this case is `nodejs`.
- `nodejs`: This is the name of the package we are searching for.
So, the command searches for the Nodejs package in the "nixpkgs" package set and lists all available versions along with their derivation path.

### Installing Packages With Nix

Once you've found the package you want to install, you can use the `nix-env` command to install it. To install Node.js, for example, you would run:

~~~
nix-env --install --attr nodejs
~~~

This command installs the latest version of the `nodejs` package.

- The `nix-env` command is used to manage packages in Nix.
- The `--install` flag specifies that we want to install a package.
- The `--attr` flag is used to specify the attribute path of the package we want to install. By providing the attribute path, we tell Nix exactly which package we want to install, ensuring that we get the correct version and all of its dependencies.
- `nodejs` is the attribute path for the Node.js package.
Nix will download and install the latest version of the Node.js package along with its dependencies.

### Installing Multiple Versions of the Same Package

Just like we discussed above, Nix allows you to install multiple versions of the same package side-by-side, without conflict. To install both Node.js version `18.14.1` and version `16.13.1`, for example, you would run:

~~~
nix-env -iA nixpkgs.nodejs-18_14_1 nixpkgs.nodejs-16_13_1
~~~

The above command installs two specific versions of Node.js, namely `nodejs-18_14_1` and `nodejs-16_13_1`, from the Nix package repository. Here's what each flag does:

- `nix-env`: This is the command to install or manage packages with the Nix package manager.
- `-iA`: This flag is short for `--install --attr`, which means we want to install the packages that correspond to the specified attributes.
- `nixpkgs.nodejs-18_14_1`: This is the attribute name for the `nodejs` package version `18.14.1` in the Nixpkgs repository. By specifying this attribute, we are telling Nix to install this specific version of Node.js.
- `nixpkgs.nodejs-16_13_1`: This is the attribute name for the `nodejs` package version `16.13.1` in the Nixpkgs repository.
So, the overall effect of this command is to install both versions of Node.js, and you can switch between them using the `nix-env --switch` command, as shown in the section on Installing Node.js with Nix and Homebrew.

### Upgrading Packages With Nix

To upgrade a package to a newer version, you can use the `nix-env --upgrade` command. For example, to upgrade Node.js to the latest version, you would run:

~~~
nix-env --upgrade nodejs
~~~

This command upgrades the `nodejs` package to the latest version available in the Nix package repository.

### Removing Packages With Nix

To remove a package that you no longer need, you can use the `nix-env --uninstall` command. For example, to remove Node.js version `16.13.1`, you would run:

~~~
nix-env --uninstall nodejs-16.13.1
~~~

This command removes the specified version of the `nodejs` package from your Mac.

### Using Packages

Once you've installed a package with Nix, you can use it just like any other program on your system. To use Node.js, for example, you can run:

~~~
node --version
~~~

This command outputs the version of Node.js currently installed on your system.
With Nix, you have a powerful and flexible package manager at your fingertips. Now that you know the basics of using Nix, you can explore the wide range of packages available in the Nix package repository and start building the perfect development environment for your needs.

## Conclusion

Package management on a Mac can be a daunting task, especially with the ever-growing number of tools and packages available. However, Nix offers a comprehensive and powerful package management system that can help users manage their packages with ease.

In this article, we covered the basics of package management on a Mac, with a focus on Homebrew as the most popular package manager. We then introduced the Nix package manager and highlighted its unique features and benefits over Homebrew, including its declarative approach to package management.
We explored the key differences between creating Nix and Homebrew packages, and how each system handles the storage and management of multiple package versions. We also provided specific examples with code to demonstrate these differences.

In the second half of the article, we walked through the steps to install and verify Nix on a Mac system. We then delved into the different functionalities of Nix, including searching for, and installing packages, upgrading, and removing packages, and using packages in your workflow.

In conclusion, Nix offers a powerful and efficient package management solution for Mac users, with unique features and benefits that make it a valuable alternative to Homebrew and other package managers. By learning and utilizing the capabilities of Nix, users can effectively manage their packages, maintain system configurations, and ensure determinism in their workflows. So if you're a Mac user looking for an alternative to Homebrew or other package managers, Nix is definitely worth considering.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
