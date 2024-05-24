---
title: "Makefile Tutorials and Examples to Build From"
toc: true
author: Aniket Bhattacharyea
sidebar:
  nav: "makefile"
internal-links:
 - makefile tutorial
 - make tutorial
excerpt: |
    Learn how to automate the software building process using `make`, a powerful tool that saves time and resources. This article covers the basics of writing a Makefile, important components of `make`, and provides examples of using `make` with different technologies.
last_modified_at: 2023-07-14
categories:
  - cli
---
**In this article, you'll master Makefile automation. If you know `make`, Earthly provides a containerized, reliable way to improve your builds. [Learn more](https://cloud.earthly.dev/login).**

Building software is a multi-step process—installing or updating dependencies, compiling the source code, testing, installing, and so on. In any moderately sized project, you might find it difficult to perform all these steps manually. This is where `make` can help you.

The `make` tool automates compilation of the software from the source code. It won't repeat a step if none of its prerequisites has changed, thus saving you time and resources.

In this article, you will learn how to write a simple Makefile and learn about important components of `make`, including variables, pattern rules, and virtual paths. You will also see some examples of using `make` with different technologies.

## The Makefile

When you run `make`, it looks for a file named `Makefile`, or `makefile` in the same directory. The name `Makefile` is suggested so that it appears near other important files such as `README`.

You can name your Makefile anything, but then you have to explicitly tell `make` which file to read:

<div class="narrow-code">

``` shell
make -f some_other_makefile
```

</div>

The Makefile should consist of one or more rules. Each rule describes a goal or a step in your build process, the prerequisites for that step, and recipes for how to execute it.

The format for each rule is as follows:

<div class="narrow-code">

``` Makefile
target1 [target2 ...]: [pre-req1 pre-req2 pre-req3 ...]
    [recipes
    ...]
```

</div>

The parts in `[]` are optional. Each rule must have one or more targets, zero or more prerequisites, and zero or more recipes. The `target` is the file you want to be created in that rule. The prerequisites can be the name of an existing rule, or the name of a file in the same directory. The recipes are shell commands that need to be run in order to generate the target.

When `make` executes a rule, it looks at the prerequisites. If all the prerequisites are older than the target file, it means that none of them has changed since the last time the rule was executed. So `make` does not execute the rule. If, however, any prerequisite is newer than the target, the recipes are executed.

Here's an example. Create a file named `data.txt` with the text `hello world.` You'll use the `wc` command to calculate the number of characters, words, and lines and store it in a file named `count.txt`. In this simple demonstration, you have a dependency and a target that needs to be built from the dependency.

First, let's do it manually.

``` shell
wc -c data.txt > count.txt # Count characters
wc -w data.txt >> count.txt # Count words
wc -l data.txt >> count.txt # Count lines
```

This should create a file named `count.txt` with the following content:

```
13 data.txt
2 data.txt
0 data.txt
```

Let's write the Makefile to automate this:

``` Makefile
all: count.txt 

count.txt: data.txt
    wc -c data.txt > count.txt # Count characters
    wc -w data.txt >> count.txt # Count words
    wc -l data.txt >> count.txt # Count lines
```

This Makefile has two targets. The first target is `all`, which acts like an overall build target. It is not necessary to have such a target, especially when our build has only one step, but it is a recommended practice.

The `all` target depends on `count.txt` and has no recipe. This means that `all` will be prepared as soon as `count.txt` is prepared.

The target `count.txt` depends on the file `data.txt` and the recipes list contains the commands you ran previously.

Now, run `make` again from the terminal. You should see that `make` executes the commands listed and creates `count.txt`. If you run the `make` command again, you should see the output:

```
make: Nothing to be done for 'all'.
```

Let's break it down. When you run `make` without any argument, it runs the first target, which is `all` in this case. Since `all` depends on `count.txt`, that target is executed. The target `count.txt` depends on `data.txt`, so the commands are run and the file is generated.

The next time you run `make` following the same sequence, `make` looks at `count.txt` and notices that `count.txt` is newer than `data.txt`, meaning the dependency has not been changed since the last time `make` was run, so it doesn't do anything.

Edit the `data.txt` file and change the text to `hi world`. Now when you run `make`, it runs the commands and updates `count.txt`. Since the dependency was changed, it rebuilt the target.

You can also run a target directly by passing its name to the `make` command. Running `make count.txt` will run only the `count.txt` rule.

Let's add a rule to clean the project files. It is a recommended practice to have a `clean` rule to delete any generated files, effectively returning the project to the initial state. Add the following rule to your Makefile:

``` Makefile
clean:
    rm count.txt
```

The `clean` rule doesn't have a prerequisite. The targets without a prerequisite are considered to be older than their dependencies, and so they're always run.

## Components of Makefile

Here are some important components that can help you write more concise and simpler Makefiles.

### Comments

You can have comments in Makefile that start with a `#` and last till the end of the line.

``` Makefile
all: count.txt # This is a comment
...
```

### Variables

Just like regular programming languages, `make` supports using variables to avoid repetitions and keep the Makefile clean. Another advantage of variables is that the user can override them without needing to edit the Makefile manually.

A variable in Makefile starts with a $ and is enclosed in parentheses () or braces {}, unless it's a single character variable. To set a variable, write a line starting with a variable name followed by `=`, `:=` or `::=`, followed by the value of the variable:

``` Makefile
TARGET = count.txt
SOURCE = data.txt
```

The variables defined with `=` are called "recursively expanded variables," and those defined with `:=` and `::=` are called "simply expanded variables." There is a subtle difference between these two, which you can read about in the [manual](https://www.gnu.org/software/make/manual/make.html#Flavors).

You can reference these values in any of the targets, prerequisites, or recipes:

``` Makefile
TARGET = count.txt
SOURCE = data.txt

all: $(TARGET) 

$(TARGET): $(SOURCE)
    wc -c $(SOURCE) >  $(TARGET) # Count characters
    wc -w $(SOURCE) >> $(TARGET) # Count words
    wc -l $(SOURCE) >> $(TARGET) # Count lines

clean:
   rm $(TARGET)
```

Here instead of hard-coding the target and source file names, we have used two variables, with default values of `count.txt` and `data.txt`. If you run the `make` command, it should work just like before. However, if you want to change the name of the target to, for example, `newcount.txt`, you can do so without changing the Makefile:

``` shell
make TARGET=newcount.txt
```

Passing `TARGET=newcount.txt` overrides the default value of `$(TARGET)` in the Makefile and so, instead of `count.txt`, the file `newcount.txt` is generated. Similarly, you can run `make TARGET=newcount.txt clean` to clean this new file.

When `make` is run, it also converts all available environment variables into make variables. So you can freely use any environment variable.

#### Automatic Variables

There are some special variables called automatic variables. Their values are computed each time for every rule and are based on the target and prerequisite file names. Here are some of the most important automatic variables:

1. **$@**: This is the target file name. If there is more than one target, this is whichever target caused the recipe to run.
2. **$***: This is the target file name without the extension.
3. **$<**: This is the name of the first prerequisite.
4. **$?**: The names of all the prerequisites that are newer than the target, with spaces between them. If the target does not exist, all prerequisites will be included.
5. **$^**: The names of all the prerequisites, with spaces between them and duplicates removed.
6. **$+**: Same as \$^, except it includes duplicates.

There are other automatic variables. For a full list, see [the manual](https://www.gnu.org/software/make/manual/make.html#Automatic-Variables).

Using the automatic variables, we can simplify our Makefile a bit more:

``` Makefile
TARGET = count.txt
SOURCE = data.txt

all: $(TARGET) 

$(TARGET): $(SOURCE)
   wc -c $< >  $@ # $< matches the source file name, $@ matches the target file name 
   wc -w $< >> $@
   wc -l $< >> $@

clean:
   rm $(TARGET)
```

### Virtual Paths

Often you have files organized into directories. It is not always possible to write the entire file name every time. You can use `VPATH` to specify where `make` should search for targets and prerequisites.

For example:

``` Makefile
VPATH = src include

foo.o: foo.cpp
```

Here `make` will search for `foo.o` and `foo.cpp` first in the current directory, and if not found will look inside the directories listed in `VPATH`. Thus if you have `src/foo.cpp`, instead of writing the whole path every time, you can use `VPATH` to tell `make` where to search for it.

However, there is a slight issue. Usually the `cpp` files are stored under `src`, while the header files are stored under `include`. But in our previous example, `make` searches for `foo.cpp` in both of those directories. You can tell `make` that `cpp` files should be searched in `src` and headers should be searched in `include`. For that, `vpath` (note: lowercase) is used:

``` Makefile
vpath %.cpp src
vpath %.h include
```

The `%` is like `*` of regex. It matches anything. The previous rule tells `make` to search for files ending in `.cpp` in `src` and files ending in `.h` in `include`.

### Pattern Rules

A pattern rule contains the character `%` exactly once. The `%` matches any character. For example, `%.cpp` matches any files ending in `.cpp`, while `a%b` matches any file starting in `a` and ending in `b` and having anything in between, like `axb` or `axyzb`, but not `ab`. There should be at least one character to match `%`. The part that matches the `%` is called the stem.

When used in a prerequisite, the `%` stands for the same stem that was matched by the `%` in the target. For example:

``` Makefile
%.o: %.cpp
    ...
```

This tells how to make `x.o` from `x.cpp` where `x` stands for anything, provided `x.cpp` should exist or can be made. So if you have `a.cpp` and `b.cpp`, that single rule can make both `a.o` and `b.o`.

### Phony Target

In our Makefile, there are two "special" targets—`all` and `clean`. Since they do not have any prerequisite, and there are no files named `all` or `clean` in the project, they are always considered to be older than their dependencies and always executed.

But if you create a file called `all` or `clean` in the directory, `make` will get confused. Since the `all` or `clean` file is there, and the targets have no prerequisites, they will be considered newer than their prerequisites. Therefore, the recipes will never be run. To fix this, you can declare the targets to be "phony":  

``` Makefile
.PHONY: all clean

...
```

For the full manual of `make`, read the [`make` documentation](https://www.gnu.org/software/make/manual/make.html).

## Examples of Using `Make`

Here are some tutorials and examples of using `make` for various languages and frameworks.

### [Creating a G++ Makefile](https://earthly.dev/blog/g++-makefile/)

This tutorial shows how to use `make` with `g++` to compile C++. It also introduces variables and phony targets.

### [Creating a Python Makefile](https://earthly.dev/blog/python-makefile/)

This article explains how to use `make` with Python. Even though Python does not require compilation, you can use `make` to automate the installation of dependencies and for testing and managing virtual environments.

### [Creating a Golang Makefile](https://earthly.dev/blog/golang-makefile/)

This tutorial explains using `make` with Golang—including automation for installing dependencies, running tests, and building binaries for different platforms.

### [Makefile Support in Visual Studio Code](https://earthly.dev/blog/vscode-make/)

This tutorial introduces official Makefile support for Visual Studio Code and explains how to install, activate, and configure the extension. The tutorial also demonstrates how to debug and build `make` targets straight from VS Code.

### [Automation With Makefiles](https://monashbioinformaticsplatform.github.io/2017-11-16-open-science-training/topics/automation.html)

This blog post demonstrates using [R Markdown](https://rmarkdown.rstudio.com/) to create web pages from Markdown files in an R project. The post explains how to set up the Makefile and use variables, pattern rules, and phony targets.

### [Using Make With Node.JS](https://lithic.tech/blog/2020-05/makefile-and-node)

In this tutorial, the author has explained the usage of `make` to automate the building, serving, and testing of a Node.js project.

### [Using Make With TypeScript](https://blog.quenk.com/using-gnu-make-to-build-a-typescript-project/)

This article explains the basic mechanisms of `make` and shows how to write a Makefile to transpile TypeScript into JavaScript.

### [Makefiles for Frontend](https://medium.com/finn-no/makefiles-for-frontend-1779be46461b)

This is a tutorial on how to configure `make` for a frontend project. The author explains how to use `make` to automate the compilation of SCSS files and bundle JavaScript with Rollup.

### [Taming Large Makefiles](https://earthly.dev/blog/repeatable-builds-every-time/#tips-for-taming-makefiles-in-large-teams)

Makefiles are hard to scale to large files and large teams. This article has have tips for making this process easier.

### [Makefiles for Java](https://dev.to/deciduously/quick-and-dirty-java-makefile-4njo)

The author demonstrates a simple Makefile that can be used in a Java project for compiling Java files to JAR files.

### [Using Autotools to Configure, Make, and Install a Program](https://earthly.dev/blog/autoconf/)

This tutorial shows how to automate the writing of Makefiles by using Autotools.

## Conclusion

The `make` tool is a valuable one to master in software development. Using it can speed up your development and ensure an easier process overall. However, due to its feature-rich nature, `make` can be hard to master.

{% include_html cta/makefile-cta.html %}

<!-- If you're familiar with Docker, consider using [Earthly](https://cloud.earthly.dev/login). Earthly combines the best aspects of `make` and Docker to give you an easy-to-understand and reproducible build with minimal effort. -->
