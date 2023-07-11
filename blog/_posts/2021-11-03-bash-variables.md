---
title: "Understanding Bash Variables"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "bash"
internal-links:
  - environment variables
  - environment variable
excerpt: |
    Learn the basics of bash variables and how they work in the UNIX shell. Discover how to define and access local shell variables, work with arrays, handle command-line arguments, and use environmental variables. Gain a solid understanding of bash variables to enhance your scripting skills.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. Bash variables are used in the UNIX shell to store and manipulate data. There are three types of variables: local shell variables, environment variables, and special variables.

Local shell variables are specific to the current shell session and are not passed to any sub-processes. They can be defined using the syntax `variable_name=value` and accessed using the `$` symbol followed by the variable name. For example:

```
one="1"
two=100
echo $one
echo $two
```

Bash also supports arrays, which can be defined using the syntax `array_name[index]=value` or `array_name=(value1 value2)`. Array elements can be accessed using the `${array_name[index]}` syntax. For example:

```
numbers[0]=0
numbers[1]=1
numbers[2]=2
echo "zero: ${numbers[0]}"
echo "one: ${numbers[1]}"
echo "two: ${numbers[2]}"
```

Bash has built-in special variables that are automatically set to specific values. One example is command-line arguments, which can be accessed using `$1`, `$2`, etc. The total number of arguments can be accessed using `$#`, and the array of arguments can be accessed using `$@`. For example:

```
echo "First argument: $1"
echo "Number of arguments: $#"
echo "All arguments: $@"
```

To unset a variable, you can use the `unset` command followed by the variable name. This removes the variable from the list of defined variables.

These are the basics of bash variables. Understanding how to define, access, and manipulate variables is essential for writing effective bash scripts. Earthly is popular with users of bash as it provides a powerful and flexible build tool for CI/CD workflows. [Check us out](/).**

<div class="narrow-code">

Bash is not just a UNIX shell, it's also a programming language. And like most programming languages, it has variables. You use these shell variables whenever you append to your `PATH` or refer to `$HOME` or set `JAVA_HOME`.

So let me walk you through how variables work in bash, starting with local shell variables and then covering special and environment variables. I think you'll find understanding the basics to be extremely helpful.

First, let's take a look at all the currently defined variables in your current shell session. You can see this at any time by running `set`.

~~~{.output caption=">_"}
> set
'!'=0
'#'=0
0=/bin/bash
ARGC=0
...
~~~

## Local Shell Variables

Local shell variables are local to the current shell session process and do not get carried to any sub-process the shell may start. That is, in Bash I can export variables and variables I don't export are called local. This distinction will make more sense once we get to exporting.

For now, though, let's look at some examples.

You can define shell variables like this:

~~~{.bash caption=">_"}
> one="1"
> two=100
~~~

And access them by using a dollar sign (`$`):

~~~{.bash caption=">_"}
> echo $one
1
> echo $two
100
~~~

You can also refer to them within double-quoted strings:

~~~{.bash caption=">_"}
> test="test value"
> echo "Test Value: $test"
Test Value: test value
~~~

Use single quotes when you don't want variable substitution to happen:

~~~{.bash caption=">_"}
> test="test value"
> echo 'Test Value: $test'
Test Value: $test
~~~

## Bash Arrays

Bash also has arrays. You can define them like this:

``` bash
numbers[0]=0
numbers[1]=1
numbers[2]=2
```

Or like this:

``` bash
moreNumbers=(3 4)
```

And access them like this:

``` bash
#!/bin/bash

numbers[0]=0
numbers[1]=1
numbers[2]=2
echo "zero: ${numbers[0]}"
echo "one: ${numbers[1]}"
echo "two: ${numbers[2]}"
echo "\$numbers: ${numbers[@]}"

moreNumbers=(3 4)
echo "three: ${moreNumbers[0]}"
echo "four: ${moreNumbers[1]}"
echo "\$moreNumbers: ${moreNumbers[@]}"
```

~~~{.output caption="Output"}
zero: 0
one: 1
two: 2
$numbers: 0 1 2
three: 3
four: 4
$moreNumbers: 3 4
~~~

Bash v4 also introduced [associative arrays](https://www.artificialworlds.net/blog/2012/10/17/bash-associative-array-examples/). I won't cover them here but they are powerful and little used feature (little used since even the newest versions of macOS only include bash 3.2).

<div class="notice--info">

### Running Shell Scripts

You can declare bash variables interactively in a bash shell session or in a bash script. I will put a shebang at the top of the scripts (`#!/bin/bash`).

To run these, save the code in a file:

``` bash
#!/bin/bash

echo "This is a bash script bash.sh"
```

Then make the file executable:

~~~{.bash caption=">_"}
> chmod +x bash.sh
~~~

Then run it:

~~~{.bash caption=">_"}
> ./bash.sh
This is a bash script bash.sh
~~~

Often I'm going to skip these steps and just show the output:

~~~{.output caption="Output"}
This is a bash script bash.sh
~~~

This makes the examples more concise but if you need clarification, or would like to learn more about shebangs, check out Earthly's [understanding Bash](/blog/understanding-bash/#use-the-right-shebang) tutorial.
</div>

You can use `unset` to unset a variable. This is nearly equivalent to setting it to a blank value, but unset will also remove it from the `set` list.

~~~{.output caption=">_"}
> s_1=1
> s_2=2
> set | grep "s_"
s_1=1
s_2=2

> s_1=
> unset s_2
> set | grep "s_"
s_1=''
~~~

## Bash Special Variables

Bash has built-in shell variables that are automatically set to specific values. I end up reaching for these primarily inside shell scripts. First up is the built-ins for accessing command-line arguments.

## Bash Command Line Arguments

When writing a shell script that will take arguments, `$1` will contain the first argument's value.

~~~{.bash caption="cli1.sh"}
#!/bin/bash

echo "$1"
~~~

~~~{.output caption=">_"}
> ./cli1.sh one
one
~~~

Arguments continue from there to `$9`:

~~~{.bash caption="cli2.sh"}
#!/bin/bash

echo "$1 $2 $3 $4 $5 $6 $7 $8 $9"
~~~

~~~{.output caption=">_"}
> ./cli2.sh 1 2 3 4 5 6 7 8 9 
1 2 3 4 5 6 7 8 9
~~~

For arguments above nine, you need to use `${}` to delimit them. Otherwise, you get an unforeseen result:

~~~{.bash caption="cli3.sh"}
#!/bin/bash

echo "This is unexpected: $15"
echo "But this works: ${15}"
~~~

~~~{.output caption=">_"}
> ./cli3.sh 1 2 3 4 5 6 7 8 9 10 11 12 13 14 fifteen
This is unexpected: 15
But this works: fifteen
~~~

I am getting `15` for `$15` because bash expands it as the first parameter (`$1`) followed by the literal number five (`5`).  

You can also access an array of command-line arguments using the built-in `$@` and the number of arguments using `$#`.

~~~{.bash caption="args.sh"}
#!/bin/bash

echo "Count : $#"
echo "Args: $@"
~~~

~~~{.output caption=">_"}
> ./args.sh 1 2 
Count : 2
Args: 1 2
~~~

You manipulate that array of command line arguments using a for loop.

~~~{.bash caption="args.sh"}
#!/bin/bash

echo "Count : $#"
echo "Args: $@"
echo "