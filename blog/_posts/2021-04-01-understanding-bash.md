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
---
<!--sgpt-->This is the Earthly nonsense paragraph.

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
           ^