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
last_modified_at: 2023-07-14
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster. If you're deep into bash scripting, know that Earthly can take care of the complex build automation, allowing you to focus more on your scripts. [Check it out](/).**

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
echo "----------------"
i=1
for arg in "$@" 
do
  echo "Arg $i:$arg"
  i=$((i+1))
done
~~~

~~~{.output caption=">_"}
> ./args.sh 1 2 
Count : 2
Args: 1 2
----------------
Arg 1: 1
Arg 2: 2
~~~

## Passing Variables as Arguments in Bash

If you need to send in arguments that contain spaces, you want to use quotes (double or single).

~~~{.bash caption=">_"}
> ./args.sh "a b" 'c d' 
Scr : 2
Args: 2
----------------
Arg 1: a b
Arg 2: c d
~~~

Command-line arguments follow the same rules as local variables, so I can use double quotes when I want to expand a variable inside of the string or single quotes when I don't want to.

~~~{.bash caption=">_"}
> test='this is not a test'
> ./args.sh "$test" '$test'  
Scr : 2
Args: 2
----------------
Arg 1: this is not a test
Arg 2: $test
~~~

## Prepending a Variable in Bash

Another way you can pass variables to a subshell is by including the definition before the call to your executable:

~~~{.bash caption="prepend.sh"}
#!/bin/bash

echo "test1: $test1"
echo "test2: $test2"
~~~

~~~{.output caption=">_"}
> test1="test1" test2="test2" ./preprend.sh
test1: test1
test2: test2
~~~

To `prepend.sh` these look like global environmental variables, which we will be covering next. But in fact, they are only scoped to the specific process this is running this script.

## Exit Codes

Where programs finish executing they can pass an exit code to the parent process which can be read using `$?`:

~~~{.bash caption=">_"}
> bash -c 'exit 255'
> echo $?
255
~~~

A return code of zero indicates success and if you don't indicate otherwise, zero is returned by default.

~~~{.bash caption=">_"}
> echo "what will I echo?"
what will I echo?
> echo $?
0
~~~

You can assign this exit status a variable use it later.

~~~{.bash caption=">_"}
> bash -c 'exit 1'
> exitCode=$?
> echo $exitCode
1
~~~

## Environmental Variables

Environmental variables work exactly like other variables except for their scope. By convention, environmental variables are named all in upper-case.
You list them with `env` and view the value of specific vars using `printenv`.

~~~{.bash caption=">_"}
> env
HOSTNAME=46ae620081da
PWD=/
HOME=/root
TERM=xterm
SHLVL=2
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env
> printenv HOME
/root
~~~

 You can use them directly in the terminal:

~~~{.bash caption=">_"}
$ echo $HOME
/root
$ echo "$HOME"
/root
$ echo '$HOME'
$HOME
~~~

And just like local shell variables, you can change their value:

~~~{.bash caption=">_"}
$ echo $HOME
/root
$ HOME="hello"
$ echo '$HOME'
hello
~~~

And use them in a bash scripts:

~~~{.bash caption="args.sh"}
#!/bin/bash

echo "PWD: $PWD"
echo "PATH: $PATH"
~~~

~~~{.output caption="Output"}
PWD: /
PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
~~~

## Bash Export Variable

The local variables I started with never leave the current shell process. If I declare a variable and then start a new bash process, it won't be set.

~~~{.bash caption=">_"}
> name="adam"
> echo $name
adam
> bash -c 'echo $name' 

~~~

You can pass these variables in one by one using the prepend syntax i showed earlier (`name="name" bash -c 'echo $name'`) but there is another way and that is using `export`.

~~~{.bash caption=">_"}
> export name="adam"
> echo $name
adam
> bash -c 'echo $name' 
adam
~~~

When I use `export` to define a variable, I'm telling bash to pass it along to any child process created, thus creating a global environmental variable.

~~~{.bash caption=">_"}
> export name="adam"
> env | grep name
name=adam
~~~

This is a one-way street, though. Exporting from a child process does not make the shell variable accessible to the parent.

~~~{.output caption=">_"}
> bash -c 'export name1="adam"'
> echo name1
~~~

Also, these variables are not persistent. If I start a new shell session, the variables I exported in a previous session won't be present. To get that behavior, I need to export them from my `.bashrc`.

~~~{.bash caption=".bashrc"}
...
export NAME="Adam"
~~~

~~~{.output caption=">_"}
> echo $NAME
Adam
~~~

`.bashrc` is a bash script found at `~/.bashrc`. It runs whenever a new interactive bash shell starts. So, by adding an export there, I am ensuring that it will present in all shell sessions started after that point. I have to start a new shell session or `source ~/.bashrc` to see this change, though.

(Using `.bashrc` is how you can configure your bash prompt, using the variable `$PS1`, and many other things, but that is a topic for a different article.)

## Conclusion

Those are the basics of bash shell variables. There is much that I haven't covered, but this is the basics. I hope this overview gave you enough depth to understand most use-cases you encounter in your day-to-day work.

Also, if you're the type of person who's not afraid to solve problems in bash, then take a look at Earthly. It's a excellent tool for creating repeatable builds in an approachable syntax.

{% include_html cta/bottom-cta.html %}

<div class="no_toc_section">
## Feedback
</div>

If you have any tips or tricks about variables in bash or spot any problems with my examples, let me know on Twitter [`@AdamGordonBell`](https://twitter.com/adamgordonbell).

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Bash is not just a UNIX shell, it's also a programming language. And like most programming languages, it has variables. You probably already knew that. <br><br>But ... do you know all its quirks?<br><br>Here is a refresher, just in case:</p>&mdash; Earthly Technologies (@EarthlyTech) <a href="https://twitter.com/EarthlyTech/status/1458449376624341005?ref_src=twsrc%5Etfw">November 10, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

</div>
