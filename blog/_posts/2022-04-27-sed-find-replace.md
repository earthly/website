---
title: "Using sed for Find and Replace"
categories:
  - Tutorials
toc: true
author: Zara Cooper
internal-links:
 - sed
topic: cli
last_modified_at: 2023-04-17
excerpt: Learn how to use the `sed` command in the command line to search and manipulate text. Discover the benefits of using `sed` and explore various commands and techniques for find and replace operations.
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster. This article is about `sed` and the best ways to use it. If you doing things at command line you might like [Earthly](https://earthly.dev/). It's a pretty great open-source build tool.**

You need the ability to search and manipulate text on the command line, especially when performing repetitive tasks. This is what makes `sed`, or **s**tream **ed**itor, so valuable. `sed` is a Unix text processing and manipulation CLI tool. A stream editor takes in text from an input stream and transforms it into a specified output according to instructions. The input stream could be from [pipelines](https://en.wikipedia.org/wiki/Pipeline_(Unix)) or files.

`sed` reads input text from files or [stdin](https://en.wikipedia.org/wiki/Standard_streams#Standard_input_(stdin)), then edits the text line by line according to the provided conditions and commands. After `sed` performs the specified operation on each line, it outputs the processed text to stdout or a file, then moves on to the next line.

## Why `sed`?

Using `sed` has its benefits. Since it's not interactive and doesn't require much time for the editing process, it works quickly. To get output, you just supply commands and conditions, then run it. `sed` offers an extensive set of robust commands and other features, including addresses for precise edit targeting, backups, and external script processing, that supercharge your text editing.

`sed` is also easily accessible from the command line, so it's helpful for regular tasks, like searching and filtering text files and streams. It's flexible enough to work with other CLI tools using pipelines. And it's efficient since you only have to run it once to process a file compared to other GUI-based text processing tools.

`sed` has a variety of use cases. It's a powerful tool for text processing tasks, like filtering, search, and substitutions, and works well in situations where high precision is needed. With `sed`, you can target a portion of input text using line addresses and regular expressions. It's also great for automation-like build processes. `sed` commands and conditions can be supplied in a script file or through arguments to the CLI command, then run automatically.

Finally, it is appropriate for use cases in which text is provided as an input stream from other CLI tools, which may need to read the output stream that `sed` returns.

In this article, you'll learn more about how this powerful tool can help you, from simple find and replace commands to more complex use cases.

<div class="notice--info">
## A Note for `macOS` Users

The `sed` on macOS is a BSD `sed`. This version of `sed` has some variations from GNU `sed` on Linux distros. You can learn more about [the differences between the two versions in this breakdown](https://riptutorial.com/sed/topic/9436/bsd-macos-sed-vs--gnu-sed-vs--the-posix-sed-specification).

This tutorial was created using GNU `sed` v4.7 on Ubuntu 20.04. To follow along, you will need to install GNU `sed` on your Mac using [brew](https://brew.sh/). You can do this by running the following:

~~~{.bash caption=">_"}
brew install gnu-sed
~~~

GNU `sed` will now be available as `gsed` on your command line after the installation. You can replace all occurrences of `sed` in this tutorial with `gsed`. If you'd like the `sed` command to point to `gsed` instead, [follow these instructions to add it to your path](https://medium.com/@bramblexu/install-gnu-sed-on-mac-os-and-set-it-as-default-7c17ef1b8f64).

</div>

## How `sed` Works

Following is a summary of the sed CLI command:

~~~{.bash caption=">_"}
sed [OPTION]... {script} [input-file]...
~~~

sed is called using the `sed` command. The options that follow are flags that indicate, for instance, how the editor should be run or how scripts should be received. Providing the `--debug` option indicates that `sed` should be run in the debug mode, where its execution is annotated. When the `--silent`, `--quiet`, or `-n` flags are provided, `sed` suppresses output printing.

The script is a collection of commands, addresses, and regular expressions. A command is an instruction that dictates what operation should be performed—`p` prints text, `a` appends text, `i` inserts text, `c` changes text, and `d` deletes text.

An address details what lines of the input text to target with the commands. You can direct the commands to operate on specific lines or on a range of them. The commands will only perform editing operations on the lines specified in the address and will not process lines not specified. If no address is given, the command will be applied to all lines of the text. Addresses can be numbers, multiples, or regular expressions. They are usually placed before a command.

The following command, for instance, will print `third line`, which is the third line of the text. The `3` before the `p` command is an address. Here's the command:

~~~{.bash caption=">_"}
$ echo "first line
second line
third line" |\
sed -n 3p
~~~

~~~{.bash caption="Output"}

third line
~~~

<div class="notice--info">
Note that sed counts lines starting at 1, not 0 as common in many programming languages.
</div>

Take this next example:

~~~{.bash caption=">_"}
echo "first line
second line
third line
fourth line
fifth line" |\
sed -n 1,+2p
~~~

~~~{caption="Output"}

first line
second line
third line
~~~

The `1,+2` address indicates that `sed` should start performing the print operation at line 1 and continue to the next two lines that follow, then stop.

## Input File

The input file contains the text you'd like to process. Running the following command would read the contents of the `sample.txt` file and print it out:

~~~{.bash caption=">_"}
$ echo "This is some sample text. 
This is another line of sample text." > sample.txt && sed -n p sample.txt
~~~

sed works by processing a text file or input stream line by line in cycles; each cycle corresponds to the processing of one line. sed reads a line and places it in an internal buffer called a pattern space. Per the commands specified, sed processes the text in the pattern space. It outputs the processed line text to [stdout](https://en.wikipedia.org/wiki/Standard_streams#Standard_output_(stdout)), and the cycle begins anew.

The pattern space does not persist text from previously processed lines, but some sed commands may require this kind of functionality. sed uses another buffer called a hold space for this purpose. It holds text and can accumulate more in between the sed cycles.

## Find and Replace With `sed`

To find and replace words in input text with sed, you use the `s` command. It takes this form:

~~~
s/regexp/replacement/
~~~

`s` takes a regular expression (`regexp`) and searches the text for any matches. Once a match is found, it substitutes the matching text with the replacement text specified (`replacement`). The forward slashes, `/`, are delimiters. They are changeable and can be replaced with other characters if needed. Note that `s` by default only works on the first match in a line.

In the following example, the `s` command substitutes `cat` with `dog` in the input text:

~~~{.bash caption=">_"}
$ echo 'We adopted a cat yesterday.
The cat is pretty playful. 
We love our cat.
You should adopt a cat from a shelter. 
There are so many cats there.' | sed s/cat/dog/
~~~

You'd get this output:

~~~{caption="Output"}
We adopted a dog yesterday.
The dog is pretty playful.
We love our dog.
You should adopt a dog from a shelter.
There are so many dogs there.
~~~

Remember the `s` command only substitutes the first match in a line. If you wanted to replace `shirt` with `coat` in the following text, only the first `shirt` match would be changed:

~~~{.bash caption=">_"}
$ echo 'Black shirts. Pink shirts. Yellow shirts. Blue shirts.' | sed s/shirt/coat/ 
~~~

This is the output:

~~~{caption="Output"}
Black coats. Pink shirts. Yellow shirts. Blue shirts.
~~~

To make replacements on more than one match, you can specify what match to change with a number or `g` character after the last delimiter. Adding a `2` would change the second match, `3` would change the third match, and so on. Using `g` would make global changes for all the matches. Here's an example:

~~~{.bash caption=">_"}
$ echo 'Black shirts. Pink shirts. Yellow shirts. Blue shirts.' | sed s/shirt/coat/g 

~~~

~~~{caption="Output"}
Black coats. Pink coats. Yellow coats. Blue coats.
~~~

You can use the special escape characters `\1` to `\9` and `&` to refer to matches. `\1` would represent the first match, `\2` the second, and so on. `&` refers to the first match, unless otherwise specified after the last delimiter. To find all instances of the word `cat` or `cats` in the example text, run the subsequent command:

~~~{.bash caption=">_"}
$ echo 'We adopted a cat yesterday. The cat is pretty playful.
We love our cat. You should adopt a cat from a shelter.
There are so many cats there.' | sed 's/cats\?\b/(&)/g'
~~~

It returns this output:

~~~{caption="Output"}
We adopted a (cat) yesterday. The (cat) is pretty playful.
We love our (cat). You should adopt a (cat) from a shelter.
There are so many (cats) there.
~~~

Using parentheses around the `&` character can be useful for searching text without making replacements.

The `\1` through `\9` special escape characters help refer to specific matches on a line. Say you want to reverse the order of this sequence of numbers: `1 2 3 4`. Following is an example of how you'd use the special escape characters:

~~~{.bash caption=">_"}
$ echo '1 2 3 4' | sed -E 's/(\w\d*) (\w\d*) (\w\d*) (\w\d*)/\4 \3 \2 \1/'
~~~

Here's the output of this command:

~~~{caption="Output"}
4 3 2 1
~~~

The first match, `\1`, is placed last, and the fourth match, `\4`, is placed first.

## Other `sed` Commands

sed provides about twenty-five commands, including the `s` command covered earlier. A commonly used one is `p`, which prints the contents of the pattern space. Since sed by default outputs the processed text after a cycle, there will be duplicate entries when printing with `p`. Hence, you must use the `-n`, `--quiet`, or `--silent` flags to prevent sed from writing to stdout. Following is this command in action:

~~~{.bash caption=">_"}
$ echo 'This text will be printed as output.' | sed --quiet p
~~~

This is its output:

~~~{caption="Output"}
This text will be printed as output.
~~~

The `a` command appends text to the end of the pattern space on a new line. For example, to add a missing `tac` word in the following sequence, run this:

~~~{.bash caption=">_"}
$ echo 'tic
toe' | sed '1a tac'
~~~

This command appends `tac` after line 1, `tic`. This is the output:

~~~{caption="Output"}
tic
tac
toe
~~~

The `i` command inserts text at the start of the pattern space on a new line. Take the previous example. To add a missing `tac` word in the following sequence, run this:

~~~{.bash caption=">_"}
echo 'tic
toe' | sed '2i tac'
~~~

This command appends `tac` at the start of line 2, `toe`. This is the output:

~~~{caption="Output"}
tic
tac
toe
~~~

The `d` command deletes the contents of the pattern space and then starts a new processing cycle. Using the `-i` or `--in-place` flags, you can edit files in place to make sure the deletions persist in the file you're editing. However, since deletions can't be undone, it's prudent to create a backup of the original file. To make a backup, provide a `bak` suffix to the `-i` or `--in-place` flags, as `-i.bak` or `--in-place=.bak`. To delete empty lines from a file, run this:

~~~{.bash caption=">_"}
$ echo -e '\n\ntic\n\ntac\n\ntoe\n\n' > sample.txt && \
sed --in-place=.bak '/^ *$/d' sample.txt 
~~~

A `sample.txt.bak` file will be created as a backup for `sample.txt`. These are the contents of the original file and `sample.txt.bak`:

~~~{.bash caption=">_"}
$ cat sample.txt.bak

tic

tac

toe
~~~

These are the new contents of `sample.txt` after running the `d` command to delete empty lines:

~~~{.bash caption=">_"}
$ cat sample.txt
tic
tac
toe
~~~

The `/^ *$/` address matches empty lines that are then deleted.

The `w` command writes the contents of the pattern space to a file. And if the file specified does not exist, sed creates it. Following is an example of text being written to `new-file.txt`:

~~~{.bash caption=">_"}
echo 'This is the first sentence of the new file.' | sed 'w new-file.txt'
~~~

The `r` command appends text to the pattern space after reading it from the specified file. To read the contents of `new-file.txt`, run this:

~~~{.bash caption=">_"}
echo 'These are the contents of new-file.txt:' | sed 'r new-file.txt'
~~~

This would be the output:

~~~{caption="Output"}
These are the contents of new-file.txt:
This is the first sentence of the new file.
~~~

Use the `c` command to completely change the contents of the pattern space. For example, to change `toothpaste` to `mouthwash` and `apples` to `oranges` in a shopping list, run this:

~~~{.bash caption=">_"}
$ echo 'toothpaste
cereal
apples
bleach
bread
milk' | sed -e '1c mouthwash' -e '3c oranges'
~~~

This would be the output:

~~~{caption="Output"}
mouthwash
cereal
oranges
bleach
bread
milk
~~~

These are just a few of the twenty-five sed commands. You can check the rest in the sed manual by running `man sed`.

## Using `sed` With `awk`

`awk` is another Unix text processing tool similar to sed. However, it's mostly used for data record extraction, processing, and reporting. Like sed, it processes text input line by line, it can take input from files or input streams, and it applies operations on the text based on supplied instructions.

It is possible to use [awk](/blog/awk-examples) and sed together through pipelines. Say you want to create mail-merged text messages from a list of customers in a [CSV](/blog/awk-csv) format. You'd use this command:

~~~{.bash caption=">_"}
$ echo 'First Name,Last Name,Bill Amount,Paid
Jane,Smith,$250,false
Alex,Boyde,$113,true
Casey,Newton,$90,false' | \
awk -F ',' '$4 == "false" {print $1 " " $2 " " $3}' |\
sed -E -e 's/([a-zA-Z]*) ([a-zA-Z]*) (\$[0-9]*)/\nHi \1 \2.\nYour current bill is \3. Please settle it as soon as possible.\n/' 
~~~

The command would output this:

~~~{caption="Output"}
Hi Jane Smith.
Your current bill is $250. Please settle it as soon as possible.


Hi Casey Newton.
Your current bill is $90. Please settle it as soon as possible.
~~~

`awk` reads the records from the input streams, checks that the condition is met (`Paid == false`), and outputs the matching records to a pipeline. `sed` reads these records from awk and creates messages with them.

You could also pipe output from sed to awk. For example, instead of using `true` or `false` to indicate whether a bill has been paid, you can use emojis:

~~~{.bash caption=">_"}
$ echo 'First Name,Last Name,Bill Amount,Paid
Jane,Smith,$250,false
Alex,Boyde,$113,true
Casey,Newton,$90,false' | \
sed -e 's/true/✅/' -e 's/false/❌/' | \
awk -F ',' '{print $1 "," $2 "," $4}' | \
column -s "," -t
~~~

This outputs:

~~~{caption="Output"}
First Name  Last Name  Paid
Jane        Smith      ❌
Alex        Boyde      ✅
Casey       Newton     ❌
~~~

## Using `sed` in Bash Scripts

To use sed in a bash script, you just need to place sed commands in the script and run the script. You can create a `hello-world.bash` script by running the following command:

~~~{.bash caption="hello-world.bash"}
echo "echo 'Hello, world! This is sed printing from a bash script.' | \
sed -n p" > hello-world.bash
~~~

To run the script, you'd use this command:

~~~{.bash caption=">_"}
$ bash hello-world.bash
~~~

This prints the following output:

~~~{caption="Output"}
Hello, world! This is sed printing from a bash script.
~~~

## Using `sed` Scripts in Files vs. as Arguments

When running `sed`, you can provide the command scripts as arguments or put them in a file. The `-e` or `--expression` flags add scripts specified directly as CLI arguments to the `sed` command. The `-f` or `--file` flags are used to input the contents of a script file to the `sed` command. sed script files usually have the `.sed` extension. If neither of the previous flags is used, sed takes the first non-flag argument passed to it as the script it will execute.

The following example specifies the script to be run using the `-e` flag:

~~~{.bash caption=">_"}
$ echo 'Hello, world!' | sed -n -e 'p'
~~~

This example reads the contents of a `hello-world.sed` script file and passes it to the sed command:

~~~{.bash caption=">_"}
$ echo 'p' > hello-world.sed && \
  echo 'Hello, world!' | sed -n -f hello-world.sed
~~~

Both of the previous commands would output this:

~~~{caption="Output"}
Hello, world!
~~~

## Using `sed` with Other CLI Tools

`sed` can be used with other CLI tools through pipelines. Since `sed` can read an input stream, CLI tools can pipe data to it. Similarly, since `sed` writes to stdout, it can pipe its output to other commands. The `sed` and `awk` examples illustrate this.

## Conclusion

`sed` gives you a lot of power over your text processing. It offers flexibility when performing repetitive tasks, and it has a robust command and feature set. It can even be coupled with other command line tools to further enrich your text processing tasks.

Another tool for defining repeatable builds is [Earthly](https://earthly.dev/), a Git-aware syntax that you can use with your current build system. All Earthly builds are language-agnostic and containerized, meaning they can run anywhere, and they can be used to reproduce CI failures, automatically cache build steps, and automatically execute targets in parallel.

To learn more about Earthly, check out its [documentation](https://docs.earthly.dev/).

{% include_html cta/bottom-cta.html %}
