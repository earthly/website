---
title: "Navigating Directories Like a Pro with Bash pushd and popd"
categories:
  - Tutorials
toc: true
author: Christoph Berger
editor: Bala Priya C

internal-links:
 - Directories
 - Bash
 - Navigation
 - Terminal
 - Commands
excerpt: |
    Learn how to navigate directories like a pro with the bash commands pushd and popd. These commands allow you to easily switch between directories and keep track of your navigation history, making your terminal workflow more efficient.
last_modified_at: 2023-07-19
---
**The article provides a detailed guide on Bash directory commands. Earthly strengthens Bash scripting by adding powerful build automation features. [Learn more about Earthly](/).**

Do you get lost in path navigation? Do you have more terminal windows open than browser tabs because you worry about not finding your way back to the previous working directory?

If you answered yes, then it's the perfect time to learn two more bash commands: `pushd` and `popd`. In this article, you'll learn how `pushd` and `popd` work, as well as a couple of alternative commands. By the end of this article, you'll have added two more useful commands to your repertoire.

## How `pushd` and `popd` Work

![How]({{site.images}}{{page.slug}}/how.png)\

The `pushd` command works like [`cd`](https://www.educative.io/answers/what-is-cd-in-linux) since it changes the current directory. However, it also pushes the current directory to an internal stack before changing to the target directory.

A stack is a storage structure that works like a physical stack of items. For example, imagine a stack of books on a table. New entries are put on top of the stack (push), and only the top entry can be removed from the stack (pop).

The stack structure allows you to easily return to the directory that was pushed to the stack last. All you have to do is call `popd`. This call removes the most recent directory from the stack and `cd`s to that directory.

<div class="wide">
![`pushd` and `popd` courtesy of Christoph Berger]({{site.images}}{{page.slug}}/Mv9GXQX.png)
</div>

### Basic Syntax

So how do we use the `pushd` and `popd` commands? Take a look at the basic syntax for these commands. You'll also learn about a useful supplementary tool named `dirs`.

#### `pushd`

The basic form of `pushd` takes a single argument—the path to `cd` to. This can be a relative or absolute path:

~~~{.bash caption=">_"}
pushd <path>  
~~~

After executing the command, your new working directory is `<path>`. The previous directory is saved in an internal stack (*ie* the directory stack).

Additionally, `pushd` prints the current directory stack to the console so that you can see the directories you can return to. The stack is printed in a horizontal layout, so the most recently added directory (the top of the stack) is the leftmost entry.

Here's an example. The following sequence moves from `$HOME` to `/etc`, then to `/var/log`, and finally, to `/tmp`; it pushes the previous directory to the directory stack each time and prints the resulting stack. Take a look at how the stack grows with each `pushd`:

~~~{.bash caption=">_"}
~$ pushd /etc
/etc ~
/etc$ pushd /var/log
/var/log /etc ~
/var/log$ pushd /tmp
/tmp /var/log /etc ~
/tmp$
~~~

#### `popd`

`popd` takes no arguments:

~~~{.bash caption=">_"}
popd
~~~

If the directory stack contains at least one directory, `popd` removes the most recent stack entry and `cd`s to this directory. If the stack is empty, `popd` prints a message and exits with no further action.

Here is how `popd` moves back through the stack of directories that was created with the previous `popd` sequence:

~~~{.bash caption=">_"}
/tmp$ popd
/var/log /etc ~
/var/log$ popd
/etc ~
/etc$ popd
~
~$ popd
bash: popd: directory stack empty
~$
~~~

> **Please note:** The stack print still includes one directory after the third `popd` (the current one, which is the home directory or `~` in the example), but the fourth `popd` claims that the stack is already empty. If the current directory is the *only* directory on the stack, you can't pop out of it because there is no directory that `popd` can move you to.

#### `dirs` To Print the Stack

Sometimes, it can be useful to print out the current stack of directories.  

It's possible that the last use of `pushd` or `popd` has already scrolled out of sight. Perhaps, you're using `pushd` or `popd` inside a script that suppresses command output.

To print the stack, you can use the `dirs` command:

~~~{.bash caption=">_"}
/tmp$ dirs
/tmp /var/log /etc ~
~~~

And since a single-line horizontal stack can be difficult to read, `dirs` has the option `-v` to print the stack vertically and with numbering:

~~~{.bash caption=">_"}
/tmp$ dirs -v
 0  /tmp
 1  /var/log
 2  /etc
 3  ~
~~~

### Options for `pushd` and `popd`

`pushd` and `popd` have several command-line flags available that are useful if you only want to manipulate the stack without actually `cd`-ing anywhere.

Take a look at some of your `pushd` options first:

#### `-n` for `pushd`

The `-n` flag adds the current directory to the stack *without* making the actual change to the target directory. The most recent directory on the directory stack will be the one that you're currently in:

~~~{.bash caption=">_"}
pushd -n <path>
~~~

#### `+N` and `-N` for `pushd`

The flags `+N` and `-N` have different meanings for `pushd` and `popd`.

When used with `pushd`, the flag `+N` rotates the directory to the left so that the `N`th directory (counting from the left, starting at zero) becomes the top of the stack.

When talking about left or right here, remember that `pushd` prints the stack in a horizontal layout. The top of the stack is the leftmost stack entry in the printed list.

The actual directory changes to the directory that became the new top of the stack. (Or in the printed stack, the leftmost stack entry.)

The `-N` flag rotates the stack to the right so that the `N`th directory (counting from the right, starting with zero) becomes the top entry.

> **Important:** The count starts at `0` for both rotation directions, but the result is different.

`pushd +0` changes nothing. The leftmost entry (the zeroth entry counting from the left) is already at the top of the stack before, and it will remain the top entry.

`pushd -0` makes the rightmost entry (the oldest one) the top of the stack.

For example, the current directory stack is `/tmp /var/log /etc ~`, and the `pushd` command rotates to the left, making the second entry from the left (*ie* `/var/log`) the top of the stack. Then the `pushd` command rotates to the right, making the rightmost entry (*ie* `/tmp`) the top of the stack:

~~~{.bash caption=">_"}
/tmp$ dirs
/tmp /var/log /etc ~
/tmp$ pushd +1
/var/log /etc ~ /tmp
/var/log$ pushd -0
/tmp /var/log /etc ~
/tmp$
~~~

> **Tip:** Use `dirs -v` to get a numbered stack. `pushd +N` then rotates the stack to the entry with the number `N`.

For example, you can rotate to entry number 2, which is `/etc`:

~~~{.bash caption=">_"}
/tmp$ dirs -v
 0  /tmp
 1  /var/log
 2  /etc
 3  ~
/tmp$ pushd +2
/etc ~ /tmp /var/log
/etc$ dirs -v
 0  /etc
 1  ~
 2  /tmp
 3  /var/log
~~~

#### `+N` and `-N` for `popd`

For `popd`, `+N` and `-N` trigger different actions than for `pushd`. `popd +N` removes the `N`th entry counting from the left (or the entry with the number `N` in the output of `dirs -v`). Again, counting from zero, `popd +0` removes the first directory and `popd +2` the third one.

Likewise, `popd -0` removes the last (*ie* oldest) directory, and `popd -1` removes the next-to-last one.

In the following example, `popd -1` removes the second directory counting from the right (`/var/log`), and a subsequent `popd +0` removes the top of the stack (`~`):

~~~{.bash caption=">_"}
/etc$ dirs
~ /tmp /var/log /etc
~$ popd -1
~ /tmp /etc
~$ popd +0
/tmp /etc
/tmp$
~~~

## Use Cases for `popd` and `pushd`

You might wonder what the use cases for `pushd` and `popd` are. After all, `cd` works just fine in most situations. But there are certain navigation patterns that `pushd` and `popd` can accelerate.

### Temporarily Switch to a Different Directory

To temporarily switch to another directory and back, you can use `cd` and `cd -`. However, in most cases, once you `cd` to the target directory, you will also `cd` through one or more subdirectories of the target directory. That means you can't use `cd -` anymore to get back to the original directory.

If you use `pushd` instead of `cd` to switch to the target directory, you can `cd` into as many subdirectories as you like, and `popd` will always get you back to the original directory.

### Frequently Switch between Two or More Directories

Imagine you have a code project set up with a frontend and backend code in different parts of the project and work on both simultaneously. You may also have a documentation directory that you frequently visit.

Then you can switch between these directories conveniently in the following way:

1. Start in one directory, and `pushd` to the other directories, one by one.
2. Once you've established the complete directory stack, you can move back and forth between them:

* `pushd +1` to move to the next directory in the stack
* `pushd -0` to move to the previous one

## Useful Aliases

When you work with `pushd` and `popd` long enough, you might observe new usage patterns where you use the same commands over and over again. To save repetitive keystrokes, set up aliases for these commands. Here are two examples:

### Cycle Through the Directory Stack With `next` and `prev`

Once you start using the `pushd +1` and `pushd -0` commands regularly, you want to create handy aliases for these commands, like this:

~~~{.bash caption=">_"}
alias next='pushd +1'
alias prev='pushd -0'
~~~

With these commands, you can simply call `next` and `prev` to cycle through the directory stack.

### Use `pushd` and `popd` With No Output

`pushd` and `popd` print the current call stack at every invocation. If you find this is too noisy, use aliases for redirecting the output into the void:

~~~{.bash caption=">_"}
alias pu='pushd >/dev/null'
alias po='popd >/dev/null'
~~~

## Alternatives To `popd` and `pushd`

![Alternate]({{site.images}}{{page.slug}}/alternates.png)\

As useful as `popd` and `pushd` are, they induce a (slight) mental load, as you need to keep track of the directory stack when navigating between the directories. Many scenarios are simple enough to use two easier techniques based on a tool that you already know: `cd`.

### Alternating Between Two Directories

If you find yourself constantly switching between two directories without navigating elsewhere or if you visit a fixed set of directories over and over again, you only need the `cd` command.

#### Toggling Between Two Directories

Whenever you `cd` to another directory, `cd` keeps track of the last directory you visited. Once your work in the current directory is done, you can go back to the last visited directory by calling the following:

~~~{.bash caption=">_"}
$ cd -
~~~

This is the poor man's `popd`.

The fun starts when you want to go back again. Just type `cd -` again, and you'll be back in the directory before the first call to `cd -`. This way, you can conveniently toggle between two working directories by calling `cd -` whenever you wish to switch to the other directory.

This, however, only works if you do not `cd` anywhere else.

#### Switching between a Fixed Set of Directories

Chances are that you have a few directories that you frequently `cd` into. For example, `~/dev/repos/github/yourname`, `~/dev/docs`, and `~/documents/notes/scratchpad`.

Sooner or later, you'll be tired of typing these paths over and over again when `cd`-ing there. To get rid of this excessive and repetitive typing, you can set shell variables for these directories in your `.bashrc`:

~~~{.bash caption=">_"}
export mygh=$HOME/dev/repos/github/yourname
export docs=$HOME/dev/docs
export scratch=$HOME/documents/notes/scratchpad
~~~

With these variables sourced into your environment, you can reach your favorite directories from whatever directory you are currently in by typing the following, for example:

~~~{.bash caption=">_"}
$ cd $mygh
~~~

Or alternatively, type the following:

~~~{.bash caption=">_"}
$ cd $docs
~~~

#### Using More Than One Terminal Window or Tab

Last but not least, you can also opt for keeping multiple Bash sessions open in separate windows or tabs. This way, you don't need any Bash commands for switching directories.

But be careful! If you end up with dozens of open Bash sessions, consider using `pushd` and `popd` instead.

## `pushd` Help

Getting stuck? These commands got you covered with handy help texts:

~~~
$ pushd --help
$ popd --help
$ dirs --help
~~~

## Conclusion

`pushd` and `popd` can be real game-changers for working in Bash or any other compatible shell. Understand the stack concept and you'll zip through your directory trees like a breeze.

But why stop there? If you've just mastered directory navigation, you can level up even more with by checking out [Earthly](https://www.earthly.dev/) for efficient build automation.

For more on Bash, do check out our [Bash series](https://earthly.dev/blog/series/bash/). Catch you there!

{% include_html cta/bottom-cta.html %}