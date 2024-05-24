---
title: "Understanding and Using Makefile Flags"
toc: true
author: Aniket Bhattacharyea
sidebar:
  nav: "makefile"
internal-links:
 - makefile flags
topic: make
excerpt: |
    Learn how to use `make` flags in your `Makefile` to customize the behavior of the compilation tools. Discover the benefits of using flags over hard-coded options and explore commonly used flags like `CFLAGS`, `CXXFLAGS`, and more.
last_modified_at: 2023-07-24
categories:
  - cli
---
**In this article, you'll master `make` flags and how to use them. If you already customize builds with `make` flags, discover how Earthly can streamline your build process for reliable and simultaneous builds. [Learn about Earthly's benefits](https://cloud.earthly.dev/login).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/z4uPHjxYyPs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

`make` is a commonplace utility in the development world. It automates the process of generating executables, documentations, and other non-source files from the source code by dividing the build process into separate interrelated steps. Using `make` eliminates the need for typing out long and complex commands to compile the source code. `make` also compiles only the modified files, thereby saving time and processing resources.

Usually, the build process involves invoking various command-line tools, like the compiler or preprocessor. Often you need to pass options to these tools as per your requirements. However, hard-coding these options in your `makefile` can lead to difficulties. As an example, consider the following `makefile` snippet:

<div class="narrow-code">

``` Makefile
main.o: main.c
    gcc -Wall -c main.c
```

</div>

This snippet compiles `main.c` to `main.o` by invoking `gcc` with the `-Wall` option. But let's say that you do not wish to pass the `-Wall` option; instead, you want to pass the `-Werror` option. The only way of doing that is to edit the `makefile` to change the options. There is no convenient way to override the options without modifying the `makefile`. This is where `make` flags come into play.

Flags in `make` are just variables containing options that should be passed to the tools used in the compilation process. Although you can use any variable for this purpose, `make` defines some commonly used flags with default values for some common tools, including C and C++ compiler, C preprocessor, `lex`, and `yacc`. For example, `CFLAGS` is used to pass options to the C compiler, while `CXXFLAGS` is used in conjunction with the C++ compiler.

## Why Should You Use Flags?

There are a few benefits to using flags over hard-coded options.

First, just like any other `makefile` variable, these flags can be overridden when invoking `make` from the command line. This feature offers a way to use any flag the user desires, as well as provides a default. For example, consider the following `makefile`:

``` Makefile
CFLAGS = -g

all: main.o
    gcc -o main $(CFLAGS) main.o
```

When you run `make`, it executes `gcc -o main -g main.o`. The value of `$(CFLAGS)` is substituted when the command is executed. However, you can change the value of `$(CFLAGS)` by providing the new value when invoking `make`:

``` shell
make CFLAGS="-Wall"
```

This time, the command that will be executed is `gcc -o main -Wall main.o`. The value of `$(CFLAGS)` provided in the command line overrides the defined value in the `makefile`.

Since any `make` variable can be overridden by providing its value in the command line, you may wonder why the manual recommends using special names for the variables. The reason is that by using the flags you can make use of the implicit rules provided by `make`. The [implicit rules](https://www.gnu.org/software/make/manual/html_node/Catalogue-of-Rules.html#Catalogue-of-Rules) are a list of built-in rules that utilize the flags. For example, consider the following `makefile`:

``` Makefile
CC = gcc
CFLAGS = -g # Flag to pass to gcc
CPPFLAGS = -I. # Flag to pass to the C preprocessor

all: main.o
```

If you have a `main.c` file in the project directory, running `make` will automatically compile it to `main.o`, even though you did not explicitly add any coding to build `main.o`. This is because `make` uses a built-in rule of the form `$(CC) $(CPPFLAGS) $(CFLAGS) -c -o x.o x.c` to compile any C file `x.c` into `x.o`. Thus, using implicit rules, you don't have to explicitly write the coding.

Another reason is that these flags are standardized and have been used for a long time, so anyone building your software will expect you to use these flags. Using any other variable would force them to go through your `makefile` in order to figure out which variable is being used. Instead, by sticking to the standard, you can save them time.

## How to Use `Make` Flags

You can use `make` flags just like any other `make` variable. Define the flags with default values using the `=` operator, and use the flags using the `$(...)` syntax:

``` Makefile
CC = gcc # It is a recommended practice to define the C compiler with CC
CFLAGS = -Wall # Defines -Wall as default flag

main.o: main.c
    $(CC) $(CFLAGS) -c main.c
```

You can also override the flags when invoking main, as explained earlier:

``` shell
make CFLAGS="-g -Wall"
```

Since `make` already defines these flags with default values (an empty string for most of them), you don't have to define them in the `makefile` explicitly if you don't want to have a default value, and you can use them directly from the command line. For example, the following `makefile` is valid, and `CFLAGS` is set to the empty string, which means no options are passed to the compiler.

``` Makefile
CC = gcc # It is a recommended practice to define the C compiler with CC

main.o: main.c
    $(CC) $(CFLAGS) -c main.c
```

You can still define `CFLAGS` from the command line:

``` shell
make CFLAGS="-Wall"
```

## Some Commonly Used Flags

Here are a few commonly used flags. For a full list of flags, check the [manual](https://www.gnu.org/software/make/manual/make.html#index-ARFLAGS).

### CFLAGS

This flag should contain the options to give to the C compiler. These options can include debug options, optimization level, warning levels, and any extra flags that you want to use.

``` Makefile
CC = gcc

CFLAGS = -g -Wall # Passes -g and -Wall to gcc

main.o: main.c
    $(CC) $(CFLAGS) -c main.c 
```

If you have options that are required for proper compilation, the [manual suggests](https://www.gnu.org/software/make/manual/html_node/Command-Variables.html#Command-Variables) putting the optional ones in `CFLAGS` and adding the required options to `CFLAGS` separately. This way the user can override `CFLAGS` via the command line, but the required options will not be overridden.

``` Makefile
CFLAGS = -g # Optional. Not required for proper compilation
ALL_CFLAGS = -I. $(CFLAGS) # -I. is required for proper compilation
main.o: main.c
        $(CC) -c $(ALL_CFLAGS) main.c
```

### CXXFLAGS

This flag is similar to `CFLAGS`, except that you should use `CXXFLAGS` when invoking a [C++ compiler](/blog/g++-makefile).

``` Makefile
CXX = g++

CXXFLAGS = -g -Wall # Passes -g and -Wall to g++

main.o: main.cpp
    $(CXX) $(CXXFLAGS) -o main.o main.cpp
```

### CPPFLAGS

`CPPFLAGS` is used to pass extra flags to the C preprocessor. These flags are also used by any programs that use the C preprocessor, including the C, C++, and Fortran compilers. You do not need to explicitly call the C preprocessor. Pass `CPPFLAGS` to the compiler, and these will be used when the compiler invokes the preprocessor. The most common use case of `CPPFLAGS` is to include directories to the compiler search path using the `-I` option.

``` Makefile
CC = gcc
CFLAGS = -g -Wall
CPPFLAGS = - I /usr/foo/bar # Search for header files in /usr/foo/bar

main.o: main.c
    $(CC) $(CPPFLAGS) $(CFLAGS) -c main.c 
```

### LDFLAGS

You can use `LDFLAGS` to pass extra flags to the linker `lD`. Similar to `CPPFLAGS`, these flags are automatically passed to the linker when the compiler invokes it. The most common use is to specify directories where the libraries can be found, using the `-L` option. You should not include the names of the libraries in `LDFLAGS`; instead they go into `LDLIBS`.

``` Makefile
LDFLAGS = -L. \ # Search for libraries in the current directory
          -L/usr/foo # Search for libraries in /usr/foo

main.o: main.c
    gcc $(LDFLAGS) -c main.c 
```

### LDLIBS

The `LDLIBS` flag should contain the space-separated list of libraries that are used by your programs. For this flag, the `-l` option followed by the name of the library is used. For example, if your software uses `libm`, the math library, then you need to include the `-lm` option.

``` Makefile
LDFLAGS = -L. \ # Search for libraries in the current directory
          -L/usr/foo # Search for libraries in /usr/foo

LDLIBS = -lm -lfoo # Use libm and libfoo

main.o: main.c
    gcc $(LDFLAGS) -c main.c $(LDLIBS)
```

Keep in mind that `LDLIBS` should be included *after* you have listed all your source files. Otherwise the linker will not be able to link the symbols properly.

### LFLAGS

This flag is used if you are working with `lex`, a tool used to generate lexical analyzers. `Lex` takes a list of token definitions in a `.l` file and generates a C program that can take an input and tokenize it accordingly. You can find a basic introduction to `lex` [on IBM's documentation site](https://www.ibm.com/docs/en/zos/2.4.0?topic=tools-generating-lexical-analyzer-using-lex#genlex).

``` Makefile
LEX = flex # Use flex as the lex program
LFLAGS = -d # enable debug

lexer.c: lexer.l
    $(LEX) $(LFLAGS) lexer.l
```

### YFLAGS

This flag is used to pass options to `yacc`. This is a tool that is often used in conjunction with `lex`. `Yacc` is a parser generator; it converts a grammar definition in a `.y` file into a C program, which can parse the tokenized output of `lex` into a parse tree. [IBM](https://www.ibm.com/docs/en/zos/2.4.0?topic=tools-generating-parser-using-yacc#genyac) has a tutorial if you'd like to find out more about `yacc`.

``` Makefile
YACC = bison # Use bison as the yacc program
YFLAGS = -v \ # Verbose mode
        -g # Generate graph

parser.c: parser.y
    $(YACC) $(YFLAGS) parser.y
```

### MAKEFLAGS

This is an interesting flag that is used in recursive invocation of `make`. If you have modules or subsystems in your project, it is likely that each subsystem will have its own `makefile`. The top-level `makefile` will then recursively call `make` for each of the modules. The `MAKEFLAGS` variable is automatically set up by `make`, and it contains all the flags and command line variables that you passed to the top-level `make`. The `MAKEFLAGS` variables will pass these options and variables down to each sub-`make`.

To test this, create a directory called `subdir` and create a `makefile` in this `subdir` with the following content:

``` Makefile
all:
 echo $(MAKEFLAGS)
```

This will print out the value of the `MAKEFLAGS` variable.

Then in your top-level `makefile`, write the following:

``` Makefile
subsystem:
 cd subdir && $(MAKE)
```

This `makefile` recursively calls `make` in the `subdir` subdirectory.

Now you can run `make` from your project root with options:

``` shell
$  make -sk CFLAGS="-g"
ks -- CFLAGS=-g
```

As you can see, the options `-k` and `-s` were passed to the sub-`make`, as well as the variables.

Note that the options `-C`, `-f`, `-o`, and `-W` are not put into `MAKEFLAGS` and not passed down. You can read more about `MAKEFLAGS` [on GNU.org](https://www.gnu.org/software/make/manual/html_node/Options_002fRecursion.html#Options_002fRecursion).

## Conclusion

Using `make` flags ensures your `makefile` follows the standard and offers an easy and powerful way to customize the behaviors of the compilation tools by providing them options. However, `make` flags are limited and require a deep understanding of the right tools to use.

{% include_html cta/makefile-cta.html %}

<!-- If you are looking for a powerful alternative to `make`, [Earthly](https://cloud.earthly.dev/login) may be the right choice for you. It is a modern take on the `make` utility. Tailored for the container era, [Earthly](https://cloud.earthly.dev/login) provides reproducible and understandable builds with minimal effort.

{% include_html cta/bottom-cta.html %} -->
