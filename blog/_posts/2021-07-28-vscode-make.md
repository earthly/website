---
title: "Building in Visual Studio Code with a Makefile"
author: Nicolas Bohorquez
author2: Adam
internal-links:
 - vscode
toc: true
sidebar:
  nav: "makefile"
topic: make
excerpt: |
    Learn how to use Makefiles in Visual Studio Code to simplify the build process for your software projects. This tutorial walks you through setting up a C++ project and demonstrates the power and flexibility of Makefiles.
last_modified_at: 2023-07-24
categories:
  - cli
---
**In this article, you'll discover how the Makefile VSCode extension can simplify your build process in Visual Studio Code. If you manage Makefiles, consider using Earthly to make your workflow more efficient. [Explore it now](https://cloud.earthly.dev/login).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/vAS4R5P0Orc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Microsoft announced [recently](https://devblogs.microsoft.com/cppblog/now-announcing-makefile-support-in-visual-studio-code/) a new Visual Studio Code extension to handle Makefiles. This extension provides a set of commands to the editor that will facilitate working with projects that rely on a Makefile to speed up the build.

In this tutorial, you'll set up a simple C++ project that depends on a well-known Python library to produce some sample charts. This is not a deep tutorial about [make and Makefiles](/blog/g++-makefile/), but to get the most out of the extension you will need to have some concepts clear.

*Make* is one of the most used tools to build software projects, for good reason:

- You can get an implementation for almost any major operating system (POSIX/Windows/MacOS)
- It's technology agnostic. You can use it to build projects on any programming language (here's an example for [JavaScript](https://medium.com/lithictech/makefile-javascript-26731fb26867).
- Its task runner capabilities provide a multipurpose tool for almost any task.

A *Makefile* is a simple text file that defines rules to be executed. The usual purpose for Makefile in C++ projects is to recompile and link necessary files based on the modifications done to dependencies. However, Makefile and make are far more useful than that. The rules defined in a Makefile combine concepts like:

- Shell scripting
- Regular expressions
- Target notation
- Project structure

To illustrate this power, the [sample project](https://github.com/nickmancol/vscode_makefile) contains a single C++ source code file. The source code for the example is pretty simple —- it flips a coin as many times as the `iters` argument is passed, and then prints the number of heads and tails counted from each flip.

~~~
#include <cstdio>
#include <cstdlib>
#include <stdlib.h>
#include <assert.h>
#include <time.h>  

int flip_coins(int iters) {
  srand (time(NULL));
  int tails = 0;
  int heads = 0;

  for(int i=0;i < iters;i++){
      int coin = rand() % 2;
      if(coin == 1) {
          printf("heads\n");
          heads++;
      } else {
          printf("tails\n");
          tails++;
      }
  }
  printf("%d Heads, %d Tails\n",heads, tails);
  return abs(tails-heads);
}

int main(int argc,char* argv[]) { 
    int iters =100;
    int diff = flip_coins(iters);
    if(100 < iters) {
        printf("With enough trials Heads should be close to Tails\n");
    }
}
~~~

This code will be compiled and linked with a simple Makefile that also will provide a couple of other standard rules for cleaning the compiled code and run a simple test.

## Creating C++ Projects with VS Code

The [VS Code extension **Makefile Tools**](https://marketplace.visualstudio.com/items?itemName=ms-vscode.makefile-tools) is still in preview but is actively developed. The installation process is similar to any other extension in VS Code:

![Makefile VSCode extension]({{site.images}}{{page.slug}}/9360.png)

After installing the extension, verify the availability of the `make` command in the system.

The most common implementation is [GNU Make](https://www.gnu.org/software/make/), which includes some non-standard extensions. If your installation of `make` is not available in the default path, you can configure it in VS Code at **File > Preferences > Settings > Extensions makefile**.

![Make path]({{site.images}}{{page.slug}}/9380.png)

To compile and link the project, you can add a Makefile to the root of the project folder. It will be detected automatically by the extension. If you have a different structure, with a Makefile in another location, you can configure it at **File > Preferences > Settings > Extensions > makefile**.

![Makefile path]({{site.images}}{{page.slug}}/9450.png)

This sample Makefile defines five simple rules:

- `all`: Cleans the compiled files from the target folder, then compiles and run the test code.
- `default`: Delegates to `CoinFlipper.cpp`.
- `CoinFlipper.cpp`: Compiles the single source file.
- `test`: Delegates to `CoinFlipper.cpp`, then runs the output main function passing an argument.
- `clean`: Deletes compiled files.

~~~
#
# A simple makefile for compiling a c++ project
#
.DEFAULT_GOAL := CoinFlipper.cpp

all: clean test

CoinFlipper.cpp: 
    gcc -o ./target/CoinFlipper.out ./src/main/CoinFlipper.cpp

run: CoinFlipper.cpp
    ./target/CoinFlipper.out 10

test: CoinFlipper.cpp
    ./target/CoinFlipper.out 10000

clean: 
    rm -rf ./target/*.out
~~~

The Makefile Tools Extension provides a new "perspective" to the Visual Studio Code IDE. This contains three different commands and three different project configurations to run the Makefile:

![Makefile tools perspective]({{site.images}}{{page.slug}}/9480.png)

The `Configuration:[Default]` refers to the make command configurations defined in the `.vscode/settings.json` file. This configuration is used to pass arguments to the make utility.

In the following example, two configurations are defined:

- `Default`
- `Print make version`

`Print make versions` adds the `--version` argument to the make utility every time the project is built using the Makefile extension. This argument is not especially useful but you can explore different arguments to fit your case.

~~~
{
 "makefile.configurations": [
     {
         "name": "Default",
         "makeArgs": []
     },
     {
         "name": "Print make version",
         "makeArgs": ["--version"]
     }
 ]
}
~~~

The second configuration is the default build target rule for the make utility, which is equivalent to running `make [target]` directly. The IDE will let show you a list of target rules defined in the Makefile configured for the project:

![config build target]({{site.images}}{{page.slug}}/9540.png)

Finally, the third configuration available in the perspective is the `Launch target`. This shows you a list of compiled files that can be run from the perspective using the commands `Debug` and `Run`. This is useful if you want to debug your source code with GDB or LLDB debuggers.

In this example, the only file runnable is `CoinFlipper.out`, compiled from the source code.

![make launch target]({{site.images}}{{page.slug}}/9560.png)

The commands in the Makefile are self-explanatory:

- `Build` runs make with the target configured previously.
- `all` instead of `default` passes no arguments to the make utility.
- `Debug` and `Run in terminal` commands launch the target (`CoinFlipper.out` in the example) with/without the debug support.

Once you build the project, the terminal view shows the result of the execution:

~~~
Building target "all" with command: "make all"
rm -rf ./target/*.out
g++ -o ./target/CoinFlipper.out ./src/main/CoinFlipper.cpp
./target/CoinFlipper.out 101
50 Heads, 51 Tails
With enough trials Heads should be equal to Tails
Target all built successfully.
~~~

As you can see from the previous image, the target was built successfully after cleaning, compiling, and running the compiled program. The extension also provides commands to run other targets easily without changing the configurations in the perspective.

The following image shows the commands available for the Makefile in the sample project:

![The makefile commands palette.]({{site.images}}{{page.slug}}/9630.png)

## Building Complex Projects

Makefiles are more complex than this. Many projects have several levels of dependencies, configurations, and quirks that make supports easily. For example, the [FFmpeg](https://github.com/FFmpeg/FFmpeg) project is a collection of libraries to work with audio, video, and subtitles among other utilities. To build it, you can download the source from GitHub and examine the Makefile:

![The makefile for FFmpeg.]({{site.images}}{{page.slug}}/9680.png)

The [developer documentation](https://trac.ffmpeg.org/wiki/CompilationGuide/Generic) for the project states that before building the source code with the provided Makefile, you need to run the [`configure`](/blog/autoconf/) script located at the root of the project's source code. Fortunately, the Makefile Tools Extension provides a setting to define the preconfiguration files required to run before executing the make commands, again in  **File > Preferences > Settings**.

![The makefile preconfiguration.]({{site.images}}{{page.slug}}/9730.png)

In the **Commands** section of the Makefile Tools Extension perspective, you can run the preconfigure command. This will run the configure script, and then you're ready to experiment with the Makefile through the extension.

## Conclusion

Large codebases need a build system to keep them under the development team's control, and Makefiles are one the most ubiquitous and flexible ways to define building these complex software projects.

With the new Makefile Tools Extension, Visual Studio Code greatly simplifies access for new developers.

{% include_html cta/makefile-cta.html %}

<!-- If you want to learn about the power of make and Makefiles, consider checking out our [Makefile Series](/blog/series/makefile/), and if you want the simplicity of a Makefile with the isolation of containers take a look at [Earthly](https://cloud.earthly.dev/login). -->
