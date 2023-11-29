---
title: 'Understanding Bash'
categories:
  - Tutorials
toc: true
author: Kasper Siig
sidebar:
  nav: "bash"
internal-links:
  - shellcheck
  - bash script
  - shebang

excerpt: |
    Learn the ins and outs of bash scripting and how it can make your life easier. From understanding shebangs to error handling and variable naming, this article covers all the essentials for writing efficient and effective bash scripts.
last_modified_at: 2023-07-19
---
**In this article, you'll learn the best practices for bash scripting. If you enjoy crafting efficient bash scripts, Earthly's containerized build approach can streamline your build processes. [Discover how Earthly can assist you](/).**

<div class="narrow-code">

Bash scripts give you the ability to turn a tedious series of commands into an easily runnable and repeatable script. With many real-world use cases, like using a bash script to run a continuous deployment process, create a series of files in a folder, or download the contents of several URLs, it's worth your time to make sure bash scripting is in your programming toolbox.

When you're done with this article, you'll not only be able to write bash scripts, but you'll be able to write them using today's accepted best practices.

## Use the Right Shebang

The very first thing you'll see at the top of every (well-written) bash script is what's called a [_shebang_](https://www.in-ulm.de/~mascheck/various/shebang/). I'll walk you through a couple of them here.

### `#!/bin/bash`

The most common shebang is the one referring to the `bash` executable:

```bash
#!/bin/bash
```

Essentially it tells your terminal that when you run the script it should use `bash` to execute it. It can be vital since you may be using a different shell in your machine (`zsh`, `fish`, `sh`, etc.), but you designed the script to work specifically with bash. In many cases, it doesn't matter what shell you're using, but there can be some very noteworthy differences in how they work, leading a script to work in `bash` but not `sh`, for example.

### `#!/user/bin/env bash`

If you use the previous shebang, it's crucial that you give the executable's absolute path. You should be aware of this since there is an alternative, where you use the `bash` executable found in the `$PATH`. You can do so by writing:

```bash
#!/user/bin/env bash
```

Some people like to customize their systems, either their personal system or production servers, resulting in the `bash` executable not being located in `/bin/bash` every time. Use the above line if you can't be sure that the `bash` executable will be located in the same path when this script is run.
</div>

## Understand Common Sets

When you run a bash script, it will always run in a new _subshell_. This means that any unique configurations you have in your current setup will not be used within the script execution. It also means that you can customize the environment that the script is running in without worrying about how your terminal will be affected.

One way to change this environment is to use the `set` command. I'll go over the four most common ones and where they're useful. I'll show the short form for these sets in the examples throughout this article, but keep in mind that there are also long-form versions. I'll mention those briefly.

### `set -u`

By default, bash doesn't do a lot of error handling. That's left up to you. So if you want to have your script exit at a certain point, you have to define it. For example, you may have the following script:

```bash
#!/bin/bash
echo $TEST
echo Hello World
```

If you run the script as shown above, it'll give you the following output:

```bash
Hello World
```

See how it doesn't complain that the `$TEST` variable is not set? You can change that. Setting the `set -u` (short form of `set -o nounset`) command initially, you're telling bash that you want it to fail if a variable is not set.

**Script:**

```bash
#!/bin/bash
set -u
echo $TEST
echo Hello World
```

**Output:**

```bash
line 3: TEST: unbound variable
```

Without `set -u`, bash will use an empty string instead of the unset variable. When running `echo $TEST`, that isn't too dangerous. However, you may be running a command like `rm -rf /$TEST` to define a path you want to delete. In this case, without `set -u`, you would end up deleting your entire file system (which there's no way to recover by default).

### `set -x`

You'll likely at some point have a big script where it's tough to keep track of not just which commands are running what, but also which commands are outputting what. This is where `set -x` comes to the rescue. Alternatively, you can write this as its long form, `set -o xtrace`.

When using `set -x`, you get the following script and output.

**Script:**

```bash
#!/bin/bash
set -x
echo Hi
echo Hello World
```

**Output:**

```bash
+ echo Hi
Hi
+ echo Hello World
Hello World
```

### `set -e`

Sometimes you want to make sure that the entire script fails if one of the commands fails. This is not the default behavior in bash. You can see [in the manual](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) that without any set options, bash is running without much error handling.

To make sure the script fails, you should use `set -e` (also known as `set -o errexit`), probably the most common one.

**Script:**

```bash
#!/bin/bash
set -e
foo
echo Hello World
```

**Output:**

```bash
line 3: foo: command not found
```

### `set -eo pipefail`

Finally, we can make the script fail if a command in a pipeline fails. Usually, bash only looks for the exit code from the last command in a pipeline. If that's 0, it'll continue just fine. Exit code 0 is what we want, since in bash that means success.

Let's use the following script as an example:

```bash
#!/bin/bash
foo | echo Hello World
echo Hi
```

`set -eo pipefail` will turn the output from:

```bash
Hello World
line 2: foo: command not found
Hi
```

into:

```bash
Hello World
line 2: foo: command not found
```

The reason you may want the script to fail if a pipeline fails is the same as earlier with `set -u`. Let's modify the scenario a bit. You have the following in your script:

```bash
FILE_PATH=$(cat /tmp/path.txt | sed 's/_/-/g)
rm -rf /$FILE_PATH
```

_Note: `sed` is a search-and-replace command. In this case it replaces underscores with dashes._

The intention is that `/tmp/path.txt` contains `tmp_file.txt`. Assume that the file `/tmp-file.txt` exists on the system. In this case the script will work perfectly and delete `/tmp-file.txt`. But what if `/tmp/path.txt` doesn't exist? `cat /tmp/path.txt` will fail, but the script won't. Now you've deleted your entire filesystem, but `set -eo pipefail` will prevent this.

### Sets in Summary

<!-- vale HouseStyle.Spelling = NO -->
| Set | Long form | Description |
|-|-|-|
| set -u | set -o nounset | Exits script on undefined variables |
| set -x | set -o xtrace | Shows command currently executing |
| set -e | set -o errexit | Exits script on error |
| set -eo pipefail | set -eo pipefail | Exits script on pipeline fail |
<!-- vale HouseStyle.Spelling = YES -->

## Use Error Checking Tools

Although you may be familiar with all the best practices, it can be tough to remember them all when your script is coming to life. Luckily there are tools available to help, like [ShellCheck](https://www.shellcheck.net/#). ShellCheck has both a browser version and a command-line tool, but for this article, let's work with the command-line version. You can find [installation instructions on GitHub](https://github.com/koalaman/shellcheck#installing).

We'll use the following script as an example:

```bash
echo "What's your name?"
read NAME
echo Hello $NAME
```

By saving this in a script in a file called `greeting.sh` and running `shellcheck greeting.sh`, you get the following output in your terminal:

```
In greeting.sh line 1:
echo "What's your name?"
^-- SC2148: Tips depend on target shell and yours is unknown. Add a shebang or a 'shell' directive.


In greeting.sh line 2:
read NAME
^--^ SC2162: read without -r will mangle backslashes.


In greeting.sh line 3:
echo Hello $NAME
           ^---^ SC2086: Double quote to prevent globbing and word splitting.

```

As you can see, `shellcheck` doesn't just tell you what you need to change, but also why it needs to be changed. This is a valuable resource, not just for improving your scripts, but also to get better at writing them in the first place.

With these tips, you'll end up with the following script:

```bash
#!/bin/bash
echo "What's your name?"
read -r NAME
echo Hello "$NAME"
```

## Understand Variable Naming and Declaration

As you saw earlier, we tried to use the `$TEST` variable. Variables can open up a whole world of opportunities, but they can also be tricky to work with. Let's go over some of the common scenarios for working with variables.

### Assigning Variables

Assigning a variable in bash is reasonably straightforward, using the `=` symbol. Here's an example of assigning "Hello World" to a `$TEST` variable:

```bash
$ MSG="Hello world!"
$ echo $MSG
Hello world!
```

### Using Variables Inside Strings

There are multiple ways to use a variable that you've assigned a value. As an example, we've assigned `foo=uname`.

#### Double Quotes

If you want to echo the contents of a variable, then use double quotes. It will expand what's inside the variable and print that to the screen.

```bash
$ foo="uname"
$ echo "$foo"
uname
```

#### Single Quotes

In some cases, you don't want to output a variable's contents, but maybe write an explanation of what that variable is used for. To avoid expansion, use single quotes:

```bash
$ foo="uname"
$ echo '$foo'
$foo
```

This also means that you don't have to manually escape the `$` symbol, which you otherwise would need to in the case of double quotes.

#### Backticks

The third option for using a variable is backticks. Use this when you want the contents of the variable to be run as a shell command:

```bash
$ foo="uname"
$ echo `$foo`
Linux
```

### Using Curly Brackets

You can get away with merely referring to a variable by writing `$FOO`. However, you may want to refer to a variable inside a string or concatenate it with another. Take a look at the following example:

<!-- markdownlint-disable MD014 -->
```bash
$ FOO="Hel"
$ echo "$FOOlo World"
Hello World
```

In this case, bash would try to find the variable `$FOOlo`, but we just wanted to print "Hello world." To make this work, you will have to do the following:

```bash
$ FOO="Hel"
$ echo "${FOO}lo World"
Hello World
```

This is most likely useful when you want to use a variable to define a path, like `/opt/${ENVIRONMENT}_build.txt`. Without curly brackets, the script would try to look up `$ENVIRONMENT_build`.

## Properly Set Permissions

One of the pitfalls that I remember running into time and time again when I started making bash scripts was remembering that [permissions](https://www.guru99.com/file-permissions.html) had to be set right. See, when you make a file with, for example, `touch`, it gives read/write permissions to the owner and read rights to everyone else. This means that you'll get a `permission denied` error when you try to run the script.

Luckily this is easily fixed. Run `chmod +x script.sh`, and now everyone is allowed to run the script.

However, do be aware that changing permissions can impose security risks. Read more about [Linux file permissions](https://www.linux.com/training-tutorials/understanding-linux-file-permissions/) before you start changing permissions blindly.

## Ensure Readability

One of the biggest pitfalls that newcomers run into is forgetting about readability. It's easy to get caught up in wanting to have a working script, and maybe you're even used to running everything manually in the terminal, where you want to type as little as possible.

When it comes to scripts, you want to make sure that you can still easily remember what's happening six months down the line. An easy way to do this is by using more extended options (`--quiet` instead of `-q`), using longer variable names (`MESSAGE` instead of `MSG`), and writing comments.

You can write commands using a hash mark, after which you can write your comment, like so:

```
# Below line will echo "Hello World!"
echo "Hello World!"
```

## Understand Your Script in Relation to CLI

When reading this article, you may have noticed that many code examples are being run straight in the terminal rather than written as a bash script. There's a good reason for that! You can write everything you write in a bash script directly in the terminal.

There is one significant difference between executing a script and typing the commands in your terminal. When you run a script, it'll start up a new, clean shell in which the script will run. This means that no variables set in your terminal will interfere with your script.

For example, if you set `TEST="hello"` in your shell and run `echo $TEST` inside a script, it will print nothing to your screen.

<div class="no_toc_section">

## Conclusion

You're now equipped to dive into bash scripting. With knowledge of common shebangs, functions of `set`, improved error handling, and common developer pitfalls, you're armed and ready. Use your newfound skills to automate daily commands, parse the remote git URL, or batch rename files. With bash scripting, the possibilities are endless.

And once you've mastered bash scripting and are ready to level up your automation game, check out [Earthly](https://www.earthly.dev/). It's a tool designed for easier, more efficient builds, and it could be the next step in your development journey.
