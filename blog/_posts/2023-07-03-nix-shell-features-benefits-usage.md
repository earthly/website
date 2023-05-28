---
title: "Demystifying Nix-shell: A Deep Dive into its Features, Benefits, and Usage"
categories:
  - Tutorials
toc: true
author: Eze Sunday Eze
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Nix
 - Features
 - Package Manager
 - Shell
 - Builds
---

**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster – like Dockerfile and Makefile had a baby. This article explores the features, benefits usage of Nix-Shell**

Ever had a situation where a project works on your computer but doesn't work on another computer? It's a mess, I know. Nix-shell is a robust package manager that can help you fix that problem. But what is a package manager?

Before we proceed, to follow along with this article, you should have a basic understanding of [Python's virtualenv](https://virtualenv.pypa.io/en/latest/), [bash](https://www.freecodecamp.org/news/bash-scripting-tutorial-linux-shell-script-and-command-line-for-beginners/), or [docker](https://www.docker.com/) and how they work. You don't need to know anything about Nix, yes, you are welcome even if today is your first day of hearing the word Nix.

So, let's continue.

In the context of software development, a package manager is a tool that allows you to install, upgrade, configure, and remove dependencies, libraries, frameworks, etc from your project.

Package managers are available for almost every programming language, such as `[npm](https://www.npmjs.com/)`, `[pnpm](https://pnpm.io/)`, and `[yarn](https://yarnpkg.com/)` for NodeJS, `[maven](https://maven.apache.org/)` for Java, `[pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)` for Python, `[cargo](https://doc.rust-lang.org/cargo/)` for Rust, and so on.

Furthermore, each operating system has its package manager. For instance, MacOS has `[brew](https://brew.sh/)` and `[port](https://www.macports.org/)`, Windows has `[Winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)`, and Linux has [apt](https://linuxize.com/post/how-to-use-apt-command/), `[dpkg](https://www.digitalocean.com/community/tutorials/dpkg-command-in-linux)`, `[snap](https://snapcraft.io/)`, etc., depending on the specific Linux distribution.

Although these tools are quite useful, developers often face a common issue while managing projects and packages across teams, which is the lack of reproducibility. Many developers can relate to the frustrating experience of their project working fine on their own machine but not on a colleague's machine or the server. This is where [Nix](https://nixos.org/) comes in to address the problem.

Nix is a package manager and programming language used for building and managing software environments, with a focus on providing predictable and reproducible builds and support for multiple platforms.

It simplifies the process of managing software dependencies, reduces the risk of configuration errors, and makes it easier to build and deploy complex software systems.

In short, with Nix, you can isolate and bundle all the dependencies your application needs to work properly. Anyone can pick it up and run it, and everything will work exactly the same way it did work on your system.

You might ask, isn't that what Docker does already?

Well, I'd argue that Nix does what Docker was supposed to do and does it better, but that's a conversation for another day.

Nix and Docker differ in their focus and approach in the sense that Nix concentrates on package management, while Docker focuses on containerization. Nix ensures consistent package and dependency installation and management across multiple systems, providing isolation at the package level. Docker isolates applications and their dependencies from the underlying host system, providing isolation at the container level.

<div class="wide">
![Diagram of a simple high-level overview of Nix and Docker]({{site.images}}{{page.slug}}/XHx7tUh.png)
</div>

If you have done any bit of Python, you would most likely be familiar with the concept of [Python Environment](https://docs.python-guide.org/dev/virtualenvs/). With the Python environment, you can create a virtual environment and install packages that will exist only in that environment. This concept is similar to what we have in Nix only that it's more advance as Nix is not just a package manager but also has its own programming language which is usually referred to as an [expression language.](https://nixos.wiki/wiki/Overview_of_the_Nix_Language)
Let's take a brief look at the Expression language, store, and content-addressable storage.

## Nix Expression Language, Store, and Content-addressable Storage

Nix expression language is the language used in Nix projects for describing packages and their configurations, and for managing the variability within packages. However, It's not a general-purpose programming language like your Python, Javascript, etc. Nix expression language utilizes a distinctive identifier based on the data's contents to interact with the Nix store. More on the Nix store in a bit.

When you use the Nix expression language to define a package or configuration, you are essentially writing a script that specifies the dependencies, build steps, and installation instructions for that package or configuration — think of it like the [DockerFile](https://docs.docker.com/engine/reference/builder/).

The expression language allows you to define complex configurations, including multiple packages and dependencies, and to specify how those packages should be built and installed.

Here is an example of what the Nix expression language looks like, it should be saved with a `.nix` file extension :

~~~{.nix caption=".nix"}
{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  name = "my-app";
  src = ./.;
  requirements = [ pkgs.requests ];
  modEnvAttrs = [ "PYTHONPATH" ];
}
~~~

The instruction in the piece of code above defines a Python application and its dependencies and builds it.

The resulting build environment will be isolated from the host system and contain all necessary dependencies to run the application.

Let's talk about the Nix store; the [Nix store](https://nixos.org/manual/nix/stable/command-ref/nix-store.html) is a directory on your system that contains all of the packages and dependencies that have been built using the Nix package manager. The Nix store uses a content-addressable storage system— a storage system that identifies data based on its content, rather than its name or location. Each package and dependency is stored as an immutable object with a unique [cryptographic](https://www.hypr.com/security-encyclopedia/cryptographic-hash-function) hash, based on its contents. By default, the Nix store is located at `/nix/store` in the root directory of the file system.

When you install a package or configuration, the Nix package manager computes the hash of the package or configuration and uses it to retrieve the object from the Nix store. This means that even if the same package is built multiple times, only one copy of it will be stored in the Nix store since its hash value will be the same.

Lastly, the content-addressable storage is a critical component of the Nix store, as it enables packages and dependencies to be stored and retrieved based solely on their content, rather than their location.

That means you would never have to download a package twice and avoid unnecessary recompilation of packages and dependencies which of course will enable efficient [deduplication](https://www.netapp.com/data-management/what-is-data-deduplication/) of packages and dependencies, which can help save disk space and reduce download times.

This package and environment management is made possible by leveraging the Nix-shell command line tool. Let's start by setting up Nix on our computer so that we can further explore the Nix-shell command.

## Setting Up Nix

To do anything with Nix-shell, we'll need to first install Nix on our computer. If you are on a *nix operating system* you can run the following command to install it

~~~{.bash caption=">_"}
curl --proto '=https' --tlsv1.2 -sSf -L \
https://install.determinate.systems/nix | sh -s -- install
~~~

Otherwise, go to the [official website and download](https://nixos.org/download) the right version for your operating system. Once the installation is complete run `nix --version` to verify that it's all good. It should return the version of Nix you just installed as shown below:

~~~{.bash caption=">_"}
nix --version
~~~

Now that you have the `Nix` package manager install in your computer, let's explore what `nix-shell` command is and how we can use it.

## The `nix-shell`

Nix has several commands for different purposes. The `nix-shell` command is one of them and it's one of the most important nix commands as it allows you to create the environment that sets up, install and run your nix project. When you run the `nix-shell` command in a project that contains a `shell.nix` file, it creates a new shell session with all the dependencies specified in that file. The `shell.nix` file contains a Nix expression that specifies the environment, including packages, tools, environment variables, and more.

To see what the `nix-shell` command can do, you can run a nix expression in the terminal that sets up a nix-shell environment, installs, `vim`  and `stdenv` packages and then opens the vim in the terminal.

~~~{.bash caption=">_"}
nix-shell --pure -p stdenv -p vim 
~~~

The command above will install [Vim editor](https://www.vim.org/) in a new shell environment and `vim` will exist there alone. The `--pure` flag ensures the shell environment is clean and doesn't inherit any packages or configurations from the user's current environment. Also, the `-p` flag is used to specify the packages to install in the nix shell environment. So, essentially, we are making `stdenv` and vim available using the `-p` flag.

Here is how the output will look:

<div class="wide">
![Example of how running a nix-shell command looks like]({{site.images}}{{page.slug}}/DRYEeQx.png)
</div>

You'll notice that when the command is completed the Terminal was prefixed with `nix-shell`, that is how you know you are in the nix-shell environment. You can now open vim by running the command `vim` on your terminal:

<div class="wide">
![A screenshot of the Vim Editor from Nix-shell environment]({{site.images}}{{page.slug}}/3Ab74HC.png)
</div>

To get a better understanding of how the `nix-shell` works, let's create a basic Python project in the `nix-shell` environment.

### Create a Python Project in the `nix-shell` Environment

Let's build a project that contains two functions. The first function will read a CSV file, converts the contents into a two-dimensional NumPy array of floating-point numbers, excluding the header row, and finally returns the resulting array as a nested list of Python floats. The second function will multiply two numbers and returns the result. We'll use Nix-shell to ensure that all our developers are able to run this code regardless of their operating system.

We'll also write tests for these two functions.

For the two functions, create an `app.py` file and add the following content to it:

~~~{.python caption="app.py"}
# app.py

import csv
import numpy as np

def read_file(filePath):
   with open(filePath, 'r') as f:
       wines = list(csv.reader(f, delimiter=";"))

   wines = np.array(wines[1:], dtype=np.float64)
   return wines.tolist()


def multiply(a, b):
   """
   Multiplies two numbers and returns the result
   """
   return a * b
~~~

For the tests, create an `app_unit_tests.py` file and add the test code below into it:

~~~{.python caption="app_unit_tests.py"}
# app_unit_tests.py

import unittest
from app import multiply, read_file

class TestMultiply(unittest.TestCase):
   def test_multiply(self):
       self.assertEqual(multiply(2, 3), 6)
       self.assertEqual(multiply(0, 5), 0)
       self.assertEqual(multiply(-2, 3), -6)

   def test_read_file(self):
       filePath = 'thequality.csv'
       expected_output = [[6.2, 0.31, 0.23, 8.1, 0.053, 49.0, 92.0,  0.9989, 3.45, 0.36, 8.6, 5.0], [8.0, 0.42, 0.28, 4.7, 0.06,                                                                               15.0, 60.0, 0.9983, 3.24, 0.53, 9.7, 6.0], [7.4, 0.49, 0.33, 7.3, 0.061, 21.0, 83.0, 0.9972, 3.24, 0.7, 9.9, 6.0]]
       result = read_file(filePath)
       self.assertEqual(result, expected_output)

if __name__ == '__main__':
   unittest.main()
~~~

The piece of code above is the unit test for the function that reads from a CSV file and the other function that multiplies two numbers.
Now that our project is ready, let's create a Nix environment with nix-shell to run it.

### Creating and Managing Nix-Shell Environments

Before we run the nix-shell command, create a `shell.nix`file and add the following Nix expression that defines all the dependencies and how to run the program:

~~~{.nix caption="shell.nix"}
{ pkgs ? import <nixpkgs> {} }:

let
python = pkgs.python38;
in

pkgs.mkShell {
buildInputs = [ python ];
shellHook = ''
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python -m unittest unit_test.py
'';
}
~~~

If you have lots of dependencies, you can create a `requirement.txt` to manage them in your project, add `numpy` as the only dependency for this exercise:

~~~{.bash caption=">_"}
numpy
~~~

Run the command the `nix-shell` on your terminal.

When you run the `nix-shell` command in the directory that has the `shell.nix` file above, it will activate a nix environment, install python3 in it, install all the python packages defined in the `requirements.txt` file, in our case the [numpy](https://numpy.org/) package and then run the unit test. The output will look like below:

~~~{ caption="Output"}
------------------------------------------
Ran 2 tests in 0.002s

OK
(venv) 
[nix-shell:~/Development/apps/python-app]$ 
~~~

As you can see, it ran the test.

Let's take a closer look at some important elements in the `shell.nix` file. At the beginning of the nix-shell script, we come across a function called `{ pkgs ? import <nixpkgs> {} }:`

This function serves a significant purpose in accessing the default package set — a collection of public nix packages—called Nixpkgs. Interestingly, it also allows us to specify a custom package set using the pkgs argument if desired.

To understand it better, let's break it down:

`<nixpkgs>`: This is a special attribute referring to the Nixpkgs channel, which represents a specific version of Nixpkgs. It's like a repository of packages, configurations, and build instructions maintained by the Nix community. In the next section, we'll discuss more about the Nixpkgs repository.

`pkgs`: This is an optional argument defined within the function. It acts as a placeholder, allowing us to either use a custom package set or fall back to the default package set if no value is provided. Essentially, while the default Nixpkgs package set offers an extensive collection of packages, sometimes you may require additional or modified packages specific to your project or environment this is where custom packages come to play. But if you don't need to import a custom package, you can easily use the with statement which just imports the packages concisely by their name like so:

~~~{.nix caption="shell.nix"}
with import <nixpkgs> {};
~~~

`?:` The question mark symbol (?) indicates that the pkgs argument is optional. You can choose to include it or not when using the function.

`import:` This is a Nix expression that helps import external files or evaluate expressions from a specific location. In our case, it imports the Nixpkgs package set from the `<nixpkgs>` channel.

`{}:` The empty set ({}) is passed as an argument to the import statement, specifying that we want to import the complete package set from Nixpkgs.

Now that we have all the components of the function demistified, let's move on to the next part of the script. In our code notice we are using the`pkgs` attribute to import the python3.8 collection and assign it to the `python` variable. We are assigning it because we want to use the keyword python later instead of `pkgs.python38`:

~~~{.nix caption="shell.nix"}
let
python = pkgs.python38;
In
~~~

Next, we use the `pkgs.mkShell {}`  block to create a Nix shell environment:

~~~{.nix caption="shell.nix"}
pkgs.mkShell {
 buildInputs = [ python ];
 shellHook = ''
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m unittest unit_test.py
 '';
}
~~~

Inside the shell we define our `buildInputs`. The `buildInputs` contain all the packages we want to install. In this case, we want to install Python3.8 that is referenced by the `python` variable:

~~~{.nix caption="shell.nix"}
buildInputs = [ python ];
~~~

We also define a `shell-hook` inside the block:

~~~{.nix caption="shell.nix"}
 shellHook = ''
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -m unittest unit_test.py
 '';
~~~

The  `shellHook` is a mechanism that allows you to execute arbitrary shell code when you enter a Nix shell environment. This can be useful for setting environment variables, configuring aliases or functions, or any other shell-related tasks that you need to perform when you enter the Nix shell environment.

In our example, we created a Python virtual environment, activated it, installed all the required packages, and then ran our test script in the `shellHook`.
There is more to the nix expression language. To learn more about the language, you should check the [docs](https://nixos.org/manual/nix/stable/quick-start.html).

### Using Nix-Shell in Your Ci/Cd Pipeline With Github Action

Let's integrate the sample code into our CI pipeline with GitHub Actions and Nix-shell. With Nix-shell, we can be sure that our builds will be reliable and predictable. Of course, Nix-shell will ensure that the same environment and package versions we used during development will be the exact same environment the tests and deployment will run on.

Here is an example `yaml` file that runs our python test in a CI pipeline using GitHub action — it runs when there is a new pull request or push on an Ubuntu machine, installs Nix from Cachix, and then runs a Nix shell which will execute the Python test.

~~~{.yaml caption="test.yml"}
name: "Test"
on:
 pull_request:
 push:
jobs:
 tests:
   runs-on: ubuntu-latest
   steps:
   - uses: actions/checkout@v3
   - uses: cachix/install-nix-action@v18
     with:
       nix_path: nixpkgs=channel:nixos-unstable
   - uses: workflow/nix-shell-action@v3
     with:
       script: |
         nix-shell
~~~

Use the `cachix/install-nix-action@v18` action to install nix and then run the nix-shell script as shown in the configuration above.

There is also a dedicated Nix continuous integration project [Hydra](https://github.com/NixOS/hydra), but it's only supported on [NixOS](https://nixos.org/). You should check it out.

Nix-shell is mostly powered by a lot of community-driven contributions. Every `nix-shell` package you download was added by someone, including all the ones we have used in this project. They are added to a dedicated [Nix GitHub repository](https://github.com/NixOS/nixpkgs) known as the Nixpkgs repository. Let's take a look at it.

### The Nixpkgs Repository

The [Nixpkgs repository](https://search.nixos.org/) is a collection of thousands of pre-built packages and libraries that can be easily installed and managed using the Nix package manager. It is maintained by the NixOS community and is continually updated with new and updated packages on GitHub.

#### Downloading Packages From the Nixpkgs Repository

Downloading packages from the Nixpkgs repository is easy and they are various paths to it. You can use the `nix-shell` command. For example, to install the [Emacs editor](https://www.gnu.org/software/emacs/), you can run `nix-shell -p emacs` or you can add it in your `shell.nix` file in the `buildInputs` section like so:

~~~{.nix caption="shell.nix"}
 buildInputs = [ python pkgs.emacs ];
~~~

You may also add it to the NixOS configuration file if you run the NixOS. The configuration file is located here in nixos directory `/etc/nixos/configuration.nix`.

~~~{.nix caption="configuration.nix"}
 environment.systemPackages = [
    pkgs.emacs
  ];
~~~

#### Add Your Own Packages

Since Nix is an Open Source project, if you find a package that you believe should be in the Nix repository but is not yet there — ensure you search the repository — you can fork the [Nix package repository](https://github.com/NixOS/nixpkgs), add your own, create a pull request with your change, once your changes are merged, your package can now be easily downloaded and used with the nix expression language.

## The Nix Daemon

The (Nix daemon](<https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-daemon.html>) is a long-running background process that is responsible for managing the Nix store, which is the directory where Nix packages are installed and stored.

When you use Nix to install packages, the daemon retrieves the packages from the Nix binary cache — a prebuilt Nix package — or builds them locally and stores them in the Nix store. Additionally, the Nix daemon also performs other useful tasks like removing unused packages and automatically sharing pre-built packages among different Nix installations, which can save time and disk space as well.

### How to Start and Stop the Daemon

![Start]({{site.images}}{{page.slug}}/start.png)\

In most cases, you might not need to start the daemon as it's always started when your computer starts up. However, if you do come to a point where you need to start it, simply run the command `nix-daemon` in the terminal. This will start the daemon in the background, and it will continue to run until it is stopped.

To stop the daemon, run the command `nix-daemon --stop`. This will stop the daemon and any running builds, you can do this for any reason. One reason could be that you figured it's taking too much memory or you don't want it anymore but it's refusing to uninstall, even though this is not something I've seen happen but of course, you should be prepared for surprises.

## Nix Channels vs Nix Flakes

[Nix Channels](https://nixos.wiki/wiki/Nix_channels) and Nix Flakes(<https://nixos.wiki/wiki/Flakes>) are two different ways of managing Nix package collections.

In the context of Nixpkgs, a "channel" refers to a specific set of "verified" git commits. The definition of what constitutes a "verified" commit may differ between channels, however, generally a verified commit is one that has been digitally signed by the author, ensuring the integrity and authenticity of the commit. When a new commit is verified, the channel that declared the verification gets updated to include it.

Using a channel provides advantages over using the git master branch because, in addition to having access to the verified commits, a channel user can benefit from pre-built binary packages that are available in the binary cache.

[Nix Channels](https://nixos.wiki/wiki/Nix_channels) are updated regularly and can be updated using the `nix-channel` command.

A **flake** is a self-contained and reproducible package configuration that can be shared and reused

[Nix Flakes](https://nixos.wiki/wiki/Flakes) is a newer feature of Nix that provide a more flexible way of managing package collections. You can easily specify your app's dependencies in the `flake.nix` file by simply listing them as inputs as we have done by adding home-manager as a dependency in the code below:

~~~{.nix caption="flake.nix"}
{
  inputs = {
    home-manager.url = "github:nix-community/home-manager";
  };
}
~~~

A nix flakes project consists of a `flake.nix` file, which defines the package configuration, and an optional flake.lock file, which pins the dependencies of the configuration to specific versions. The flake.lock file is similar to the [npm lock](https://docs.npmjs.com/cli/v9/configuring-npm/package-lock-json) and [cargo lock](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html) files.

The `flake.lock` file ensures that your package configuration is reproducible across different machines and environments consistently. You can also use `nix flake show` — much like `pip list` in Python — to preview the packages that will be built before actually building them.

If you have gotten to this part of the article, congratulations. Nix-shell is an amazing project, the best part is that if for any reason you want to share your environment with others, it's as simple as committing the `shell.nix` file to your Git history and pushing it or copying and sharing the shell.nix file with them. The shell.nix file is everything you need to do the magic.

## Conclusion

Nix and `nix-shell` are very powerful tools every development team needs in every stage of the product development, testing, and deployment circle. There is so much about Nix, we have just scratched the surface yet.

Here is a summary of what we've learned so far:

- Nix-shell allows you to create a reproducible environment for your project: We have learned that `nix-shell` creates a consistent environment with specific dependencies, ensuring it builds and runs the same way on different machines and systems. No more "it works on my system and not on the server" problem. This will greatly improve the development team onboarding process and allow you to focus on writing code that solves real-life problems.

- Nix-shell creates isolated environments for your projects: Also, we've learned that with `nix-shell`, your project operates in a separate environment, preventing changes from affecting other projects or the system itself, which is useful when managing conflicting dependencies or versions.

- `Nix-shell` automates dependency management by installing dependencies into the environment, saving time and effort. You can also customize your nix-shell environment with configuration files or command-line options which is pretty convenient.

I hope this article gives you a clear understanding of what `nix-shell` is and how you can leverage it to make your builds reproducible. If you are looking to explore the code further, you can find the entire code used in this tutorial on [GitHub](https://github.com/ezesundayeze/nix-python)

{% include_html cta/bottom-cta.html %}
