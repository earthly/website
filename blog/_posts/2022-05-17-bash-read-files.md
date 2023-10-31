---
title: "Using Bash to Read Files"
categories:
  - Tutorials
toc: true
author: Sundeep Teki

internal-links:
 - nchar
 - read files
 - nl 
topic: cli
excerpt: |
    Learn how to use Bash to read files line by line, use custom delimiters, assign variables, and more. This article provides step-by-step instructions and examples to help you efficiently search for keywords, process text, automate tasks, and more using Bash scripts.
last_modified_at: 2023-07-14
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about IO and file reading in bash. If you are looking for to move beyond bash scripts for building and deploying software then [check us out](/).**

[Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) (bourne again shell) scripts give you the ability to turn series of manual commands into an easily [runnable and repeatable script](https://earthly.dev/blog/understanding-bash/). This can be especially useful when working with files.

For programmers, Bash enables you to efficiently search for particular keywords or phrases by reading each line separately. Bash can also be used for reading files for a variety of reasons, like shell scripting, searching, text processing, building processes, logging data, and automating administrative tasks. When you're done with this article, you'll be able to use Bash to read files line by line, use custom delimiters, assign variables, and more.

## How to Read Files Using Bash

Below, you'll learn about various reading operations with Bash, including reading a file line by line with the `read` command that loops over the contents of a file using a `while` loop, using custom delimiters, caching, and more.

### Reading a File Line by Line with `read` and `while` in Bash

The following code illustrates how to use the `while` conditional loop to read a file:

~~~{.bash caption="bash"}
while read -r line; 
do
    echo "$line";
done < "filename.txt"
~~~

The `while` loop reads each line from the specified filename, `filename.txt`, and stores the content of each line in the specified variable, `$line`. This content is also printed out on the terminal.

If you were to deconstruct the previous reading operations even further, you would start by creating a text file:

~~~{.bash caption=">_"}
$ touch filename.txt
~~~

Then you would use your preferred text editor, like [vim](https://www.vim.org) or [GNU Emacs](https://www.gnu.org/software/emacs/), to add pseudo input:

~~~{.bash caption="filename.txt"}
The
quick
brown
fox
jumped
over
the
lazy
dog.
~~~

After that, you need to execute the `while` loop, just like the first code snippet, that reads and prints the contents of `filename.txt` to the console:

~~~{.bash caption="bash"}
while read -r line;
do;
echo "$line";
done < "filename.txt"
~~~

This code can be converted to a [Bash script](/blog/understanding-bash), like `read_bash.sh`, and can be executed any number of times.

Similarly, the following code shows the output for executing the `while` command to read a file but now using an executable shell script, `read_bash.sh`:

~~~{.bash caption=">_"}
$ chmod +x read_bash.sh
$ sh read_bash.sh
~~~

### Using Custom Delimiters When Reading Files in Bash

[Delimiters](https://techieroop.com/how-to-split-string-with-a-delimiter-in-shell-script/) are a sequence of one or more characters that specify the boundary between distinct parts of a file, including plain text, math, or other types of data streams.

The [Internal Field Separator (IFS)] is a special shell variable that acts as the delimiter in Bash. The value of IFS dictates how Bash will split the string. The default value of IFS consists of the space, tab, and newline characters. If you run `echo "$IFS"`, you'll just see an empty output, because all the three aforementioned characters are "non-printing". To "see" them, you can use the `cat` command with the `-e` and `-t` flag:

~~~{.bash caption=">_"}
$ echo "$IFS" | cat -et
~~~

You'll see the following output:

~~~{.bash caption="Output"}
 ^I$
$
~~~

There's a space at the beginning, the `^I` represents the tab character, and the `$` stand for the newline character.

You can set the IFS variable to your custom delimiter to change the default string splitting behaviour. In the following example, to read a CSV file, IFS is set to `,`:

~~~{.bash caption="ifs.sh"}
#! /bin/bash
while IFS="," read -r column1 column2
do
 echo "Name: $column1"
 echo "Age: $column2"
 echo ""
done < input.csv
~~~

The content of `input.csv` is the following:

~~~{.bash caption="input.csv"}
john,23
robert,55
max,35
~~~

And the output of the script is the following:

~~~{.bash caption="Output"}
Name: john
Age: 23

Name: robert
Age: 55

Name: max
Age: 35
~~~

To revert IFS back to the default value, you can simply unset it:

~~~{.bash caption=""}
unset IFS
~~~

### Using `nchar`

In some cases, for instance, where the relevant information in the file is contained in the first few characters, like login details or file version, reading an entire file is not prudent. Bash can be used to read a specific number of characters rather than a full line.

Or:

~~~{.bash caption="nchar.sh"}
#! /bin/bash
while read -r line;
do;
echo "$line";
done < "filename.txt"

#Number of characters to read:
n=5

#Code to read first 'n' characters:
echo ${input:0:$n}
~~~

Running the script:

~~~{.bash caption="Output"}
The q
~~~

### Reading User Prompts

In many instances, user inputs are required as part of the process. Bash can also read user prompts via the command line and pass them to a variable for further processing. In the following example, a Bash script `login.sh` prompts the user to enter the username and password for an application:

~~~{.bash caption="login.sh"}
#! /bin/bash
read -p 'Username: ' uservar
read -sp 'Password: ' passvar
echo
echo Thank you $uservar for your login details
~~~

Following is the output of this code block:

~~~{.bash caption=">_"}
Username: Sundeep
Password: 
Thank you Sundeep for your login details
~~~

### Assigning Variables

Working with variables is important for scaling a lot of file and data processing operations. It's possible to read a whole file into a variable using the following code snippet:

~~~{.bash caption=">_"}
#Reading a file, filename.txt from the first example into a variable, var:
var=$(<filename.txt)
echo "$value"
~~~

~~~{.ini .merge-code caption="Output"}
The
quick
brown
fox
jumped
over
the
lazy
dog.
~~~

### Piping to Other Programs

[Pipe](https://www.baeldung.com/linux/pipe-output-to-function) is a versatile Bash utility. Typically, it's used to take standard output from one process and pass it as standard input to another program.

Below, is an example where you read a file being piped to a Bash script, `cat_read.sh`:

~~~{.bash caption="cat_read.sh"}
#!/bin/bash

if [ -t 0 ]
then
  # Read from file
  data=$(cat $1)
else
  # Read from stdin
  data=$(cat)
fi
echo $data
~~~

In this example, the script will read from a file if provided with a file name. If it doesn't have a file name, it will read from `stdin`.

~~~{.bash caption=">_"}
$ chmod +x cat_read.sh

$ # Create the test file
$ echo "Hello, World" > file.txt

$ #Example1
$ ./cat_read.sh file.txt
~~~

~~~{.bash .merge-code caption="Output"}

Hello, World
~~~

Another Example:

~~~{.bash caption=">_"}
$ cat file.txt | ./cat_read.sh
~~~

~~~{.bash .merge-code caption="Output"}
Hello, World
~~~

### Working With Empty Lines

Most files include empty lines and escape characters, which are sometimes problematic and need to be ignored when reading a file.

~~~{.bash caption="filename.txt"}
The

quick

brown

fox
~~~

You can make this possible using the following code:

~~~{.bash caption=">_"}

while read -r line; do
   [[ -n "$line" && "$line" != [[:blank:]#]* ]] && echo "$line"
done < "filename.txt"
~~~

~~~{.bash .merge-code caption="Ouput"}
The
quick
brown
Fox
~~~

## Other File-Reading Options in Bash

In addition to the file-reading operations described earlier, there are some other methods in Bash whose primary job is not related to reading input but is used for reading files.

### Using the `cat` Command

The [`cat` command](https://linuxhint.com/cat-command-bash/) (short for "concatenate") is a method used to view the contents of a file, create single or multiple files, or concatenate files.

In the following example, `cat` is being used to read a file:

~~~{.bash caption=">_"}
$ cat filename.txt
~~~

### Using the `nl` Command

The `nl` command in Bash is used for numbering lines and can take input from a file or from the standard input (stdin). The most basic `nl` operation is depicted here:

~~~{.bash caption=">_"}
$ nl filename.txt
~~~

In this example, the `nl` operation adds a line number to each line in `filename.txt` and saves it into a new filename, `nl_filename.txt`, whose output can be viewed using the `cat` command.

~~~{.bash caption=">_"}
$ nl filename.txt > nl_filename.txt
$ cat nl_filename.txt
~~~

### Using the `head` Command

The `head` command is used to print the top N number of data in a given file. By default, it prints the first ten lines of the specified files:

~~~{.bash caption=">_"}
$ head -n 5 filename.txt
  The
  quick
  brown
  fox
~~~

### Using the `tail` Command

The `tail` command in Bash is the complement of the `head` command and is used to print the last N number of data in a given file. By default, it prints the last ten lines of the specified files:

~~~{.bash caption=">_"}
$ tail -n 5 filename.txt
jumped
over
the
lazy
dog.
~~~

### Side Note: Caching

Caching or memoization of long-running Bash functions is useful for caching the results of expensive commands for display in the terminal. This functionality is provided by libraries, like [Bash Cache](https://github.com/dimo414/bash-cache) and [`bkt`](https://github.com/dimo414/bkt).

## Conclusion

Bash is an extremely versatile command language that can be efficiently used for a number of file-processing operations, including reading, writing, printing, and porting to different programs. It's a staple of the Unix operating system, so knowledge of Bash is very helpful when working with command line interfaces on cloud instances, GPUs, and more.

In this article, you learned how to use Bash for reading files and reviewed use cases and examples for each approach.

If you use Bash or tools like Make or Docker to automate the process of building software then you should take a look at Earthly. [Earthly](https://earthly.dev/) provides a simple and familiar syntax for defining cacheable, parallelizable, and Git-aware builds for any system that can be run anywhere. You can head to their [blog](https://earthly.dev/blog/) to learn more.

{% include_html cta/bottom-cta.html %}
