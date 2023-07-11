---
title: "Using Makefile Wildcards"
categories:
  - Tutorials
toc: true
author: Kasper Siig
sidebar:
  nav: "makefile"
internal-links:
 - Makefiles
 - Wildcard
 - Programming
 - Make
excerpt: |
    Learn how to use wildcards in Makefiles to create flexible and automated build processes. This tutorial provides examples and explanations of common wildcard use, the wildcard function, and rules with wildcards. Whether you're new to Make or looking to enhance your Makefile skills, this article is a must-read.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about using Makefile wildcards. Earthly is a great tool for users of Makefiles who are looking for a modern approach to builds. [Check us out](/).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/z4uPHjxYyPs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Although many of the new modern programming frameworks, like [Node.js](https://nodejs.org/en/) and [.NET](https://en.wikipedia.org/wiki/.NET), come with their own way of packaging and distributing their programs, there's no doubt that [Make](https://www.gnu.org/software/make/) originally created a lot of the founding principles for building and distributing software.

[Make](/blog/using-cmake) provides users with many exciting possibilities, including making packaging software easy and automated. This saves time when building software, and it's a massive aid in creating a streamlined process. Once you get started building [Makefiles](https://www.gnu.org/software/make/manual/html_node/Introduction.html), you'll notice that there are places where you don't want something to be hardcoded. This is where wildcards come into play. They're one of the parts that turn Make into an incredibly flexible tool build tool.

In this article, you'll get a quick introduction to [Make](/blog/makefiles-on-windows), where you'll be shown an example C application. Don't be worried if you're not familiar with C programming; the application is simple to understand, and your familiarity with any language is more than enough. With this application, you'll be guided through various ways to implement wildcards into the build process.

If you want to see all the code from this tutorial in one place, you can find it in [this GitHub repository](https://github.com/KSiig/makefile-wildcards).

## How To Use Make

![How to use make]({{site.images}}{{page.slug}}/how.jpg)\

To begin, define a sample application you can use as an example. As any experienced programmer will know, the best example is that of "Hello, World!" This is what it looks like in C:

~~~{.bash caption=">_"}
#include <stdio.h> // Include the library necessary to print to the terminal

int main() {
   // printf() displays the string inside quotation
   printf("Hello, World!");
   return 0; // Make sure the program terminates after completion
}
~~~

The program is relatively simple, and if any line is confusing, you can look at the accompanying comment.

Copy the contents of the code block and save it in a file called `main.c`. Now create a file called `Makefile` in the same directory as your `main.c` file, and paste the following into it:

~~~{.bash caption=">_"}
main.o: main.c
  gcc -o hello main.c
~~~

> Note: Make is very particular about indentation, so make sure you use a `tab` on the second line.

It's assumed that you are familiar with [Make](/blog/makefiles-on-windows) and its syntax, but you may be unfamiliar with [GCC](https://www.linuxtopia.org/online_books/an_introduction_to_gcc/gccintro_82.html). It's the compiler most commonly used for C programs. In this command, you define that `gcc` should compile the program into a binary called `hello`, and it should do this using the `main.c` file.

Now, the basis of the application is done, and it's time to introduce wildcards.

## Makefile Wildcards

![Makefile Wildcard]({{site.images}}{{page.slug}}/wildcard.png)\

As mentioned in the introduction, when you want your Makefile targets to be flexible, wildcards come into play. Wildcards can be effective in many places but only pick up files matching a pattern. Now, dive deeper into what is possible with wildcards:

### Common Wildcard Use

If you've worked in a terminal before or with [glob patterns](https://en.wikipedia.org/wiki/Glob_(programming)), you may be familiar with an asterisk (`*`) being used to match any character. This is also how wildcards work in Make. For instance, you can use `*.o` to match any files with the extension `.o`.

You'll often use a wildcard character to make a `clean` target. Earlier we generated a main.o file and it's certainly possible to manually remove it and any other generated files, but you'll see almost all projects using Make contain a `clean` target. This target could look something like this:

~~~{.bash caption=">_"}
clean:
  rm -f *.o
~~~

Running `make clean` will ensure that any files ending in `.o` will get deleted, helping you keep a clean directory.

### Wildcard Function

As you can see, the use of wildcards is not as complex as it may seem on the surface. If you've ever worked with [string matching](https://www.topcoder.com/thrive/articles/Introduction%20to%20String%20Searching%20Algorithms), the wildcard function will seem very familiar.

However, an important thing to note is that you can't do wildcard matching everywhere inside a `Makefile`, at least not in the way shown earlier. For instance, take a look at the following example:

~~~{.bash caption=">_"}
files_to_delete = *.o

clean:
  rm -f $(files_to_delete)
~~~

This will work fine because the `rm` command takes the argument `*.o` and can work with it. But it's important to note that the command that's being run is `rm -f *.o` and that `$(files_to_delete)` is *not* replaced with a list of files matching `*.o`. So while many commands invoked in a Makefile may work fine by directly inserting `*.o`, it's important to know the distinction.

For instance, what you see inside a recipe is only evaluated *once*, not recursively. Imagine that `make` is reading every line from left to right. It will encounter the variable `files_to_delete`, and then replace it with the contents of the variable; `*.o`. At the end of that variable, it continues moving to the right. It's not reading over the line again to find out that there's a wildcard that needs to be expanded. This is why you need to define the wildcard directly in the recipe works, as the wildcard is what is now encountered when reading the line.

If you want the variable to contain the actual list of files, you have to make a slight variation and use the `wildcard` function, like so:

~~~{.bash caption=">_"}
files_to_delete = $(wildcard *.o)

clean:
  rm -f $(files_to_delete)
~~~

This is one of the most common pitfalls in `make`. Now `make` will read the variable first and evaluate the `wildcard` function, meaning the variable actually contains the list of files. Then, when the variable is called in the recipe, it's a list of files.

## Rules With Wildcards

![Rules Wildcard]({{site.images}}{{page.slug}}/rules.png)\

You've now seen some examples of how wildcards can be used inside of Makefiles, but it's also possible to use pattern matching when defining your rules. By defining a rule inside your Makefile with the `%` character, you can refer to the pattern inside the target by using the character sequence `$*`. As an example, here's how you can integrate a wildcard into a rule where you want to create a binary from a given `.c` file:

~~~{.bash caption=">_"}
%.out: %.c
  gcc -o $* $*.c
~~~

Now you can run `make main.out`, and it will create the `main` binary from the `main.c` file.

### Associated Functions

You've now learned about most of the uses that are specific to Make, but it's important to note that there are also places inside [Make](/blog/makefiles-on-windows) where you can use wildcards like you would in many other scenarios you're used to, like Bash programming. Here are a few examples:

#### The Patsubst Function

The `patsubst` function inside Make is a useful one, giving you the ability to modify strings based on a pattern. The functionality in itself is very basic; it finds some text and replaces it. The syntax is as follows:

~~~{.bash caption=">_"}
$(patsubst pattern,replacement,text)
~~~

A straightforward example of using this function could be `$(patsubst world,everyone,hello world)`, which would produce the text to "hello everyone". From here, you can search for any pattern using the `%` character and get it replaced, like so:

~~~{.bash caption=">_"}
$(patsubst he%,%x,hello world)
~~~

The previous code produces the text "llox world" because you've dropped `he` and added an `x`. This function is not a string replacement tool; it's a pattern replacement tool.

#### Filter

Just like the `patsubst` function, `filter` is a text-manipulation function. You use the `filter` function when you want to return a list of words that match a given pattern, and the syntax for this command is `$(filter pattern...,text)`.

As you can see, it's possible to specify many different patterns you want to match. Here's an example:

~~~{.bash caption=">_"}
files = foo.c bar.c foo.o bar.o

foo:
  cat $(filter %.c, $(files))
~~~

In this example, the relevant projects files are `foo.c bar.c foo.o bar.o`, but using this rule, you only want to know the contents of the files with the extension `.c`.

## Conclusion

Wildcards are a handy utility when creating your Makefiles. You can use them directly in your rules, however, you have to ensure that you're using them correctly and consider whether you need to use the `wildcard` function. Besides by using the wildcards directly in your targets, you can also use pattern matching in your rules to create more dynamic targets.

{% include_html cta/makefile-cta.html %}

<!-- While Make is a popular tool with many possibilities and some downsides. For a modern approach to builds, check out [Earthly](https://earthly.dev/), a tool that has combined the best parts of Makefiles and [Dockerfiles](https://docs.docker.com/engine/reference/builder/). -->