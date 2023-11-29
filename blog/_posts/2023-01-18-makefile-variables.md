---
title: "Understanding and Using Makefile Variables"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea
editor: Bala Priya C
sidebar:
  nav: "makefile"
internal-links:
 - Makefile
 - Variables
 - Assignment
excerpt: |
    Learn all about Makefile variables and how to use them to automate complex processes in your code. Find out how to set variables, append to them, and use special variables like automatic and implicit variables.
last_modified_at: 2023-07-19
---
**The article simplifies the intricacies of Makefile variables. Earthly improves Makefile performance by introducing sophisticated caching and concurrent execution. [Learn more about Earthly](/).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/z4uPHjxYyPs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Since its appearance in 1976, [Make](https://www.make.com/en) has been helping developers automate complex processes for compiling code, building executables, and generating documentation.

Like other programming languages, Make lets you define and use variables that facilitate [reusability](/blog/achieving-repeatability) of values.

Have you found yourself using the same value in multiple places? This is both repetitive and prone to errors. If you'd like to change this value, you'll have to change it everywhere. This process is tedious, but it can be solved with variables, and Make offers powerful variable manipulation techniques that can [make](/blog/using-cmake) your life easier.

In this article, you'll learn all about `make` variables and how to use them.

## What Are Make Variables?

A variable is a named construct that can hold a value that can be reused in the program. It is defined by writing a name followed by `=`, `:=`, or `::=`, and then a value. The name of a variable can be any sequence of characters except ":", "#", "=", or white space. In addition, variable names in [Make](/blog/using-cmake) are case sensitive, like many other programming languages.

The following is an example of a variable definition:

~~~{.makefile caption=""}
foo = World
~~~

Any white space before the variable's value is stripped away, but white spaces at the end are preserved. Using a `$` inside the value of the variable is permitted, but `make` will assume that a string starting with the `$` sign is referring to another variable and will substitute the variable's value:

~~~{.makefile caption=""}
foo = one$two
# foo becomes onewo
~~~

As you'll soon learn, `make` assumes that `$t` refers to another variable named `t` and substitutes it. Since `t` doesn't exist, it's empty, and therefore, `foo` becomes `onewo`. If you want to include a `$` verbatim, you must escape it with another `$`:

~~~{.makefile caption=""}
foo = one$$two
~~~

## How to Use Make Variables

Once defined, a variable can be used in any target, prerequisite, or recipe. To substitute a variable's value, you need to use a dollar sign (`$`) followed by the variable's name in parentheses or curly braces. For instance, you can refer to the  `foo` variable using both `${foo}` and `$(foo)`.

Here's an example of a variable reference in a recipe:

~~~{.makefile caption=""}
foo = World
all:
    echo "Hello, $(foo)!"
~~~

Running `make` with the earlier `makefile` will print "Hello, World!".

Another common example of variable usage is in compiling a C program where you can define an `objects` variable to hold the list of all object files:

~~~{.makefile caption=""}
objects = main.o foo.o bar.o
program : $(objects) # objects used in prerequisite
    cc -o program $(objects) # objects used in recipe

$(objects) : foo.h # objects used in target
~~~

Here, the `objects` variable has been used in a target, prerequisite, and recipe.

Unlike many other programming languages, using a variable that you have not set explicitly will *not* result in an error; rather, the variable will have an empty string as its default value. However, some special variables have built-in non-empty values, and several other variables have different default values set for each different rule (more on this later).

## How to Set Variables

![How to Set Variables]({{site.images}}{{page.slug}}/9NzlT6N.png)\

Setting a variable refers to defining a variable with an initial value as well as changing its value later in the program. You can either set a value explicitly in the `makefile` or pass it as an environment variable or a command-line argument.

### Variables in the Makefile

There are four different ways you can define a variable in the Makefile:

* Recursive assignment
* Simple assignment
* Immediate assignment
* Conditional assignment

#### Recursive and Simple Assignment

As you may remember, you can define a variable with `=`, `:=`, and `::=`. There's a subtle difference in how variables are expanded based on what operator is used to define them.

* The variables defined using `=` are called [recursively expanded variables](https://www.gnu.org/software/make/manual/make.html#Recursive-Assignment), and
* Those defined with `:=` and `::=` are called [simply expanded variables](https://www.gnu.org/software/make/manual/make.html#Recursive-Assignment).

When a recursively expanded variable is expanded, its value is substituted verbatim. If the substituted text contains references to other variables, they are also substituted until no further variable reference is encountered. Consider the following example where `foo` expands to `Hello $(bar)`:

~~~{.makefile caption=""}
foo = Hello $(bar)
bar = World

all:
    @echo "$(foo)"
~~~

Since `foo` is a recursively expanded variable, `$(bar)` is also expanded, and "Hello World" is printed. This **recursive expansion** process is performed every time the variable is expanded, using the *current values* of any referenced variables:

~~~{.makefile caption=""}
bar = World
foo = Hello $(bar)

bar = Make
# foo now expands to "Hello Make"

all:
    @echo ${foo} # prints Hello Make
~~~

The biggest advantage of recursively expanded variables is that they make it easy to construct new variables piecewise: you can define separate pieces of the variable and string them together. You can define more granular variables and join them together, which gives you finer control over how `make` is executed.

For example, consider the following snippet that is often used in compiling C programs:

~~~{.makefile caption=""}
CFLAGS = -g
ALL_CFLAGS = -I. $(CFLAGS)
main.o: main.c
    $(CC) -c $(ALL_CFLAGS) main.c
~~~

Here, `ALL_CFLAGS` is a recursively expanded variable that expands to include the contents of `CFLAGS` along with the `-I.` option. This lets you override the `CFLAGS` variable if you wish to pass other options while retaining the mandatory `-I.` option:

~~~{.makefile caption=""}
CFLAGS="-g -Wall" # ALL_CFLAGS expands to "-I. -g -Wall"
~~~

A disadvantage of recursively expanded variables is that it's not possible to append something to the end of the variable:

~~~{.makefile caption=""}
CFLAGS = $(CFLAGS) -I. # Causes infinite recursion
~~~

To overcome this issue, [GNU Make](https://www.gnu.org/software/make/) supports another flavor of variable known as **simply expanded variables**, which are defined with `:=` or `::=`. A simply expanded variable, when defined, is scanned for further variable references, and they are substituted once and for all.

Unlike recursively expanded variables, where referenced variables are expanded to their current values, in a simply expanded variable, referenced variables are expanded to their values at the time the variable is defined:

~~~{.makefile caption=""}
bar := World
foo := Hello $(bar)

bar = Make

all:
    @echo ${foo} # Prints Hello World
~~~

With a simply expanded variable, the following is possible:

~~~{.makefile caption=""}
CFLAGS = $(CFLAGS) -I.
~~~

<div class="notice--info">
GNU Make supports simply and recursively expanded variables. However, other versions of `make` usually only support recursively expanded variables. The support for simply expanded variables was added to the Portable Operating System Interface (POSIX) standard in 2012 with only the `::=` operator.
</div>

#### Immediate Assignment

A variable defined with `:::=` is called an **immediately expanded variable**. Like a simply expanded variable, its value is expanded immediately when it's defined. But like a recursively expanded variable, it will be re-expanded every time it's used. After the value is immediately expanded, it will automatically be quoted, and all instances of `$` in the value after expansion will be converted into `$$`.

In the following code, the immediately expanded variable `foo` behaves similarly to a simply expanded variable:

~~~{.makefile caption=""}
bar := World
foo :::= Hello $(bar)

bar = Make

all:
    @echo ${foo} # Prints Hello World
~~~

However, if there are references to other variables, things get interesting:

~~~{.makefile caption=""}
var = one$$two
OUT :::= $(var)
var = three$$four
~~~

Here, `OUT` will have the value `one$$two`. This is because `$(var)` is immediately expanded to `one$two`, which is quoted to get `one$$two`. But `OUT` is a recursive variable, so when it's used, `$two` will be expanded:

~~~{.makefile caption=""}
two = two

all:
    @echo ${OUT} # onetwo
~~~

<div class="notice--info">
The `:::=` operator is supported in POSIX Make, but GNU Make includes this operator from version 4.4 onward.
</div>

#### Conditional Assignment

The conditional assignment operator `?=` can be used to set a variable only if it hasn't already been defined:

~~~{.makefile caption=""}
foo = World

foo ?= Make # foo will not change
bar ?= Make # bar will change

all:
    @echo Hello ${foo}
    @echo Hello ${bar}
~~~

An equivalent way of defining variables conditionally is to use the [`origin` function](https://www.gnu.org/software/make/manual/make.html#Origin-Function):

~~~{.makefile caption=""}
foo ?= Make

# is equivalent to

ifeq ($(origin foo), undefined)
foo = Make
endif
~~~

These four types of assignments can be used in some specific situations:

### Shell Assignment

You may sometimes need to run a shell command and assign its output to a variable. You can do that with the `shell` function:

~~~{.makefile caption=""}
files = $(shell ls) # Runs the `ls` command & assigns its output to `files`
~~~

A shorthand for this is the shell assignment operator `!=`. With this operator, the right-hand side must be the shell command whose result will be assigned to the left-hand side:

~~~{.makefile caption=""}
files != ls
~~~

### Variables With Spaces

Trailing spaces at the end of a variable definition are preserved in the variable value, but spaces at the beginning are stripped away:

~~~{.makefile caption=""}
foo = xyz   # There are spaces at the beginning and at the end

# Prints "startxyz   end"
all:
    @echo "start${foo}end"
~~~

It's possible to preserve spaces at the beginning by using a second variable to store the space character:

~~~{.makefile caption=""}
nullstring =
foo = ${nullstring} xyz   # Spaces at the end

# Prints "start xyz   end"
all:
    @echo "start${foo}end"
~~~

### Target-Specific Variables

It's possible to limit the scope of a variable to specific targets only. The syntax for this is as follows:

~~~{.makefile caption=""}
target … : variable-assignment
~~~

Here's an example:

~~~{.makefile caption=""}
target-one: foo = World
target-two: foo = Make

target-one:
    @echo Hello ${foo}

target-two:
    @echo Hello ${foo}
~~~

Here, the variable `foo` will have different values based on which target `make` is currently evaluating:

~~~{.makefile caption=""}
$ make target-one
Hello World

$ make target-two
Hello Make
~~~

### Pattern-Specific Variables

![Pattern-Specific Variables]({{site.images}}{{page.slug}}/BZHNTkc.png)\

Pattern-specific variables make it possible to limit the scope of a variable to targets that match a particular [pattern](https://www.gnu.org/software/make/manual/make.html#Pattern-Intro). The syntax is similar to target-specific variables:

~~~{.makefile caption=""}
pattern … : variable-assignment
~~~

For example, the following line sets the variable `foo` to `World` for any target that ends in `.c`:

~~~{.makefile caption=""}
%.c: foo = World
~~~

Pattern-specific variables are commonly used when you want to set the variable for **multiple targets that share a common pattern**, such as setting the same compiler options for all C files.

### Environment Variables

The real power of `make` variables starts to show when you pair them with [environment variables](/blog/bash-variables). When `make` is run in a shell, any environment variable present in the shell is transformed into a `make` variable with the same name and value. This means you don't have to set them in the `makefile` explicitly:

~~~{.makefile caption=""}
all:
    @echo ${USER}
~~~

When you run the earlier `makefile`, it should print your username since the `USER` environment variable is present in the shell.

This feature is most commonly used with [flags](https://earthly.dev/blog/make-flags). For example, if you set the `CFLAGS` environment variable with your preferred C compiler options, they will be used by most `makefiles` to compile C code since, conventionally, the `CFLAGS` variable is only used for this purpose. However, this is only sometimes guaranteed, as you'll see next.

If there's an explicit assignment in the `makefile` to a variable, it overrides any environment variable with the same name:

~~~{.makefile caption=""}
USER = Bob

all:
    @echo ${USER}
~~~

The earlier `makefile` will always print `Bob` since the assignment overrides the `$USER` environment variable. You can pass the `-e` flag to `make` so environment variables override assignments instead, but this is not recommended, as it can lead to unexpected results.

### Command-Line Arguments

You can pass variable values to the `make` command as command-line variables. Unlike environment variables, command-line arguments will always override assignments in the `makefile` unless the `override` directive is used:

~~~{.makefile caption=""}
override FOO = Hello
BAR = World

all:
    @echo "${FOO} ${BAR}"
~~~

You can simply run `make`, and the default values will be used:

~~~{.makefile caption=""}
$ make
Hello World
~~~

You can pass a new value for `BAR` by passing it as a command-line argument:

~~~{.makefile caption=""}
$ make BAR=Make
Hello Make
~~~

However, since the `override` directive is used with `FOO`, it cannot be changed via command-line arguments:

~~~{.makefile caption=""}
$ make FOO=Hi
Hello World
~~~

This feature is handy since it lets you change a variable's value without editing the `makefile`. This is most commonly used to pass configuration options that may vary from system to system or used to customize the software. As a practical example, [Vim uses command-line arguments to override configuration options](https://github.com/vim/vim/blob/f8ea10677d007befbb6f24cd20f35c3bf71c1296/src/INSTALL#L192), like the runtime directory and location of the default configuration.

## How To Append To a Variable

![How to Append to a Variable]({{site.images}}{{page.slug}}/RGuT43G.png)\

You can use the previous value of a simply expanded variable to add more text to it:

~~~{.makefile caption=""}
foo := Hello
foo := ${foo} World

# prints "Hello World"
all:
    @echo ${foo}
~~~

As mentioned before, this syntax will produce an **infinite recursion error** with a recursively expanded variable. In this case, you can use the `+=` operator, which appends text to a variable, and it can be used for both recursively expanded and simply expanded variables:

~~~{.makefile caption=""}
foo = Hello
foo += World

bar := Hello
bar += World

# Both print "Hello World"
all:
    @echo ${foo}
    @echo ${bar}
~~~

However, there's a subtle difference in the way it works for the two different flavors of variables, which you can read about in the [docs](https://www.gnu.org/software/make/manual/make.html#Appending).

## How To Use Special Variables

In Make, any variable that is not defined is assigned an *empty string* as the default value. There are, however, a few special variables that are exceptions:

### Automatic Variables

Automatic variables are special variables whose value is set up automatically per rule based on the target and prerequisites of that particular rule. The following are several commonly used automatic variables:

* **`$@`** is the file name of the target of the rule.
* **`$<`** is the name of the first prerequisite.
* **`$?`** is the name of all the prerequisites that are newer than the target, with spaces between them. If the target does not exist, all prerequisites will be included.
* **`$^`** is the name of all the prerequisites, with spaces between them.

Here's an example that shows automatic variables in action:

~~~{.makefile caption=""}
hello: one two
    @echo $@
    @echo $<
    @echo $?
    @echo $^

    @touch hello

one:
    @touch one

two:
    @touch two

clean:
    @rm -f hello one two
~~~

Running `make` with the earlier `makefile` prints the following:

~~~{.makefile caption=""}
hello
one
one two
one two
~~~

If you run `touch one` to modify `one` and run `make` again, you'll get a different output:

~~~{.makefile caption=""}
hello
one
one
one two
~~~

Since `one` is newer than the target `hello`, `$?` contains only `one`.

There exist variants of these automatic variables that can extract the directory and file-within-directory name from the matched expression. You can find a list of all automatic variables in the [official docs](https://www.gnu.org/software/make/manual/make.html#Automatic-Variables).

**Automatic variables are often used where the target and prerequisite names dictate how the recipe executes**. A very common practical example is the following rule that compiles a C file of the form `x.c` into `x.o`:

~~~{.makefile caption=""}
%.o:%.c
    $(CC) -c $(CPPFLAGS) $(CFLAGS) $^ -o $@
~~~

### Implicit Variables

Make ships with certain predefined rules for some commonly performed operations. These rules include the following:

* Compiling `x.c` to `x.o` with a rule of the form `$(CC) -c $(CPPFLAGS) $(CFLAGS) $^ -o $@`
* Compiling `x.cc` or `x.cpp` with a rule of the form `$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $^ -o $@`
* Linking a static object file `x.o` to create `x` with a rule of the form `$(CC) $(LDFLAGS) n.o $(LOADLIBES) $(LDLIBS)`
* And [many more](https://www.gnu.org/software/make/manual/make.html#Catalogue-of-Rules)

These implicit rules make use of certain predefined variables known as implicit variables. Some of these are as follows:

* **`CC`** is a program for compiling C programs. The default is `cc`.
* **`CXX`** is a program for compiling C++ programs. The default is `g++`.
* **`CPP`** is a program for running the C preprocessor. The default is `$(CC) -E`.
* **`LEX`** is a program to compile Lex grammars into source code. The default is `lex`.
* **`YACC`** is a program to compile Yacc grammars into source code. The default is `yacc`.

You can find the full list of implicit variables in [GNU Make's docs](https://www.gnu.org/software/make/manual/make.html#Implicit-Variables).

Just like standard variables, you can explicitly define an implicit variable:

~~~{.makefile caption=""}
CC = clang

# This implicit rule will use clang as compiler
foo.o:foo.c
~~~

Or you can define them with command line arguments:

~~~{.makefile caption=""}
make CC=clang
~~~

### Flags

Flags are special variables commonly used to pass options to various command-line tools, like compilers or preprocessors. Compilers and preprocessors are implicitly defined variables for some commonly used tools, including the following:

* **`CFLAGS`** is passed to `CC` for compiling C.
* **`CPPFLAGS`** is passed to `CPP` for preprocessing C programs.
* **`CXXFLAGS`** is passed to `CXX` for compiling C++.

Learn more about [Makefile flags](https://earthly.dev/blog/make-flags/).

## Conclusion

Make variables are akin to variables in other languages with unique features that make them effective yet somewhat complex. Learning them can be a handy addition to your programming toolkit. If you've enjoyed diving into the intricacies of Makefile variables, you might want to explore [Earthly](https://www.earthly.dev/) for a fresh take on builds!

{% include_html cta/makefile-cta.html %}