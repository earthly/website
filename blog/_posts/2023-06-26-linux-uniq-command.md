---
title: "A Practical Guide to the Linux Uniq Command"
categories:
  - Tutorials
toc: true
author: Thinus Swart
editor: Bala Priya C

internal-links:
 - Linux
 - Uniq
 - Guide
 - Files
excerpt: |
    
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about using the `uniq` command for text processing. If you're interested in a different approach to building and packaging software, then [check us out](/).**

The `uniq` command is a useful tool in Linux that helps you find unique lines of text inside a file or from standard output. It filters out all repeated lines, leaving only the unique lines of text in an output. This can be helpful when you're working with large text files and need to quickly identify distinct lines of text and easily eliminate duplicates to streamline your text-processing tasks.

The aim of this guide is to help you discover the different applications and choices offered by the `uniq` command, with the goal of incorporating it into your daily toolset.

## Basic Syntax of the uniq Command

There are two main ways to use the `uniq` command. You can either interact directly with a file or interact with [stdout](https://linuxhint.com/bash_stdin_stderr_stdout/).

### Interacting Directly With a File

The syntax for using `uniq` directly with a file is simple:

~~~{.bash caption=">_"}
uniq <optional-arguments> <filename>
~~~

This runs the `uniq` command with any of your chosen arguments on a specified file. These arguments allow you to change the behavior and the output of the `uniq` command. That output is then sent to stdout, which means you can manipulate the output further with other text-processing commands if you want to.

### Interacting With `stdout`

If you have a file that you want to process using other commands before you run the `uniq` command on the output, your syntax might look like this:

~~~{.bash caption=">_"}
cat <filename> | grep -oP '<regular-expression>' | sort | uniq
~~~

Linux (and other Unix-based operating systems) introduce the concept of [piping](https://linuxhint.com/linux-pipe-command-examples/), which takes the output from one command and pipes it as an input to the next command in the pipeline.

The previous code snippet does the following:

* `cat` is used to display the contents of a file to stdout.
* That output is sent to `grep`, which is a command that can extract certain parts of the output based on a pattern (a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) in this case).
* The extracted lines that matched the pattern are sent to `sort`, which by default, sorts the output alphabetically.
* Finally, the `uniq` command removes all duplicate lines from the output and displays the result to the user.

This example may look advanced to you, but in the next section, you'll review a few more code samples so you can become more comfortable processing and analyzing data using the `uniq` command as well as other Linux commands.

## Using the `uniq` Command on a File

Now that you understand the basic syntax of the `uniq` command, try to use `uniq` on a file on your system.

If you want to follow along, create a file called `lyrics.txt` somewhere on your system and add the lyrics to one of your favorite songs. The example in this guide uses the lyrics for the song "Happy Birthday":

~~~{.bash caption=">_"}
user@localhost:~$ cat lyrics.txt
Happy birthday to you
Happy birthday to you
Happy birthday, dear person
Happy birthday to you
~~~

### Removing Duplicate Lines

To remove duplicate lines, run the `uniq` command on your `lyrics.txt` file to see the output:

~~~{.bash caption=">_"}
user@localhost:~$ uniq lyrics.txt 
Happy birthday to you
Happy birthday, dear person
Happy birthday to you
~~~

The `uniq` command removes any duplicate lines that follow one after the other. In this example, even though the fourth line is the same as the first and second lines, it's not removed from the output because the fourth line is *not* a duplicate of the preceding line.

If you don't specify any optional arguments for the command, this is the *default* mode of operation for the `uniq` command.

### Counting Duplicate Lines

You can also count the number of duplicate lines in a file by providing the `-c` argument to your command:

~~~{.bash caption=">_"}
user@localhost:~$ uniq -c lyrics.txt 
      2 Happy birthday to you
      1 Happy birthday, dear person
      1 Happy birthday to you
~~~

As you can see, the count isn't perfect. The first, and last lines are actually duplicates of one another, but that's because the default operation of `uniq` is to look for duplicates in preceding lines.

### Sorting Text Before Counting

You can sort the file before using `uniq` to count the unique lines. For instance, take a look at what the sort command does to the `lyrics.txt` file:

~~~{.bash caption=">_"}
user@localhost:~$ sort lyrics.txt 
Happy birthday, dear person
Happy birthday to you
Happy birthday to you
Happy birthday to you
~~~

`sort` has many other options for sorting including, numerically, or alphabetically, ascending, or descending but for this example, the default sorting method works just fine as our file contains only alphabetic characters. If there are white spaces and other special characters, sorting is according to a particular precedence of characters.

You can process the results from `sort` by piping the results of that command to the `uniq` command:

~~~{.bash caption=">_"}
thinus@devnull:~$ sort lyrics.txt | uniq -c
      1 Happy birthday, dear person
      3 Happy birthday to you
~~~

This time around, `uniq` is correctly counting the number of duplicate lines because the lines have already been sorted.

## Running the `uniq` Command with Arguments and Flags

So far, you've been introduced to the `-c` argument for the `uniq` command. However, the `uniq` command is capable of a lot more.

As with almost any command in Linux, you can run the `--help` or `-h` parameter to find out what arguments are available to you for any particular command:

~~~{.bash caption=">_"}
user@localhost:~$ uniq --help
Usage: uniq [OPTION]... [INPUT [OUTPUT]]
Filter adjacent matching lines from INPUT (or standard input),
writing to OUTPUT (or standard output).

With no options, matching lines are merged to the first occurrence.

Mandatory arguments to long options are mandatory for short options too.
  -c, --count           prefix lines by the number of occurrences
  -d, --repeated        only print duplicate lines, one for each group
  -D                    print all duplicate lines
      --all-repeated[=METHOD]  like -D, but allow separating groups
                                 with an empty line;
                                 METHOD={none(default),prepend,separate}
  -f, --skip-fields=N   avoid comparing the first N fields
      --group[=METHOD]  show all items, separating groups with an empty line;
                          METHOD={separate(default),prepend,append,both}
  -i, --ignore-case     ignore differences in case when comparing
  -s, --skip-chars=N    avoid comparing the first N characters
  -u, --unique          only print unique lines
  -z, --zero-terminated     line delimiter is NUL, not newline
  -w, --check-chars=N   compare no more than N characters in lines
      --help     display this help and exit
      --version  output version information and exit

A field is a run of blanks (usually spaces and/or TABs), then non-blank
characters. Fields are skipped before chars.

Note: 'uniq' does not detect repeated lines unless they are adjacent.
You may want to sort the input first, or use 'sort -u' without 'uniq'.

GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
Full documentation <https://www.gnu.org/software/coreutils/uniq>
or available locally via: info '(coreutils) uniq invocation'
~~~

Don't be alarmed at this wall of text. This guide goes through a few advanced examples with you and uses some of the other available arguments to show them in action.

## Advanced Techniques to Use the `uniq` Command

If you have a more structured data file, like a CSV, you can also use `uniq` to count duplicate values of a specific field. The example used here is pretty specific for the purpose of this guide, but you can create your own example to experiment with.

Suppose you have a CSV file that tracks meteorite landings around the world with the following format: `day, time, country`:

~~~{.bash caption=">_"}
user@localhost:~$ cat meteorites.csv 
day,time,country
2022-01-08,13:47:05,Germany
2022-01-11,11:49:15,Australia
2022-03-02,09:23:27,Germany
2022-04-21,01:11:00,United States
2022-07-14,14:09:32,Canada
2022-08-08,13:37:34,Canada
2023-02-03,21:25:53,Japan
2023-03-05,23:59:09,Finland
2023-04-07,02:23:01,United States
2023-04-11,09:17:00,United States
~~~

You may want to see how many times each country has experienced a meteorite strike since you've started tracking them.

### Skipping a Few Characters

As you can see, this file has a very specific character count, so you can use the `--skip-chars=N` option to skip a specified number of characters on each line so that you only compare the values of the `country` field. This is only possible because the file has a rigid structure and a precise number of characters preceding the `country` field:

~~~{.bash caption=">_"}
user@localhost:~$ cat meteorites.csv | uniq --skip-chars=20 -c
      1 date,time,country
      1 2022-01-08,13:47:05,Germany
      1 2022-01-11,11:49:15,Australia
      1 2022-03-02,09:23:27,Germany
      1 2022-04-21,01:11:00,United States
      2 2022-07-14,14:09:32,Canada
      1 2023-02-03,21:25:53,Japan
      1 2023-03-05,23:59:09,Finland
      2 2023-04-07,02:23:01,United States
~~~

Unfortunately, you can see that it didn't work as expected. It did count duplicates correctly where the `country` values were adjacent, so you know the `--skip-chars` option is working. This means that you're running into the same problem as before: `uniq` is only counting a duplicate if the values being compared are adjacent to each other.

At this point, you're probably realizing that the `uniq` command has some limitations. It's highly unlikely that you can use the `uniq` command on its own without first modifying or extracting specific bits of data that you want to count with `uniq`. You're going to need to use other commands to help you achieve that.

Sort the file and then count the output with `uniq` again:

~~~{.bash caption=">_"}
user@localhost:~$ cat meteorites.csv | sort -t, -k3 | \
uniq --skip-chars=20 -c
      1 2022-01-11,11:49:15,Australia
      2 2022-07-14,14:09:32,Canada
      1 date,time,country
      1 2023-03-05,23:59:09,Finland
      2 2022-01-08,13:47:05,Germany
      1 2023-02-03,21:25:53,Japan
      3 2022-04-21,01:11:00,United States
~~~

This time, you're telling `sort` that you're using commas for your value delimiter (`-t,`) and that you want to sort the third column (`-k3`).

Now, the `uniq` command can properly check for duplicates because the sorted column makes sure that all duplicate values are adjacent to one another. However, the output isn't very clean. You can fix that by using [`tail`](https://www.geeksforgeeks.org/tail-command-linux-examples/) instead of `cat` and displaying everything except the CSV header line:

~~~{.bash caption=">_"}
user@localhost:~$ tail -n +2 meteorites.csv | sort -t, -k3 | \
uniq --skip-chars=20 -c
      1 2022-01-11,11:49:15,Australia
      2 2022-07-14,14:09:32,Canada
      1 2023-03-05,23:59:09,Finland
      2 2022-01-08,13:47:05,Germany
      1 2023-02-03,21:25:53,Japan
      3 2022-04-21,01:11:00,United States
~~~

### Skipping a Few Fields

You can tell `uniq` to compare specific fields first. However, the `uniq` command expects fields to be space-delimited. That means you have to replace the commas with spaces after sorting the output:

~~~{.bash caption=">_"}
user@localhost:~$ tail -n +2 meteorites.csv | sort -t, -k3 | \
sed "s/,/ /g" | \
uniq --skip-fields=2 -c
      1 2022-01-11 11:49:15 Australia
      2 2022-07-14 14:09:32 Canada
      1 2023-03-05 23:59:09 Finland
      2 2022-01-08 13:47:05 Germany
      1 2023-02-03 21:25:53 Japan
      3 2022-04-21 01:11:00 United States
~~~

As before, you're first using the `tail` command to display everything except the first line, then sorting the third column with the `sort` command.

Then the [`sed`](https://earthly.dev/blog/sed-find-replace/) command is replacing all commas with a space character, and the `uniq` command can look for duplicates in the third column because you specified that you want to skip the first two fields when you're comparing values.

### Implementing a Cleaner Output

Suppose you only want to display the country names and their distinct value counts. You're going to need the help of the [`cut`](https://www.tutorialspoint.com/unix_commands/cut.htm) command. The `cut` command in Linux allows you to extract specific sections or columns of text from files or command output:

~~~{.bash caption=">_"}
user@localhost:~$ tail -n +2 meteorites.csv | cut -d"," -f3 | \
sort | uniq -c
      1 Australia
      2 Canada
      1 Finland
      2 Germany
      1 Japan
      3 United States
~~~

Now you can even sort the count column to display the results in descending order:

~~~{.bash caption=">_"}
thinus@devnull:~$ tail -n +2 meteorites.csv | cut -d"," -f3 | sort | \
uniq -c | sort -nr
      3 United States
      2 Germany
      2 Canada
      1 Japan
      1 Finland
      1 Australia
~~~

The `-nr` option for the `sort` command instructs `sort` to sort using *numeric* values in *reverse* order.

## Alternatives to the `uniq` Command

As you may have noticed, there are many ways to accomplish the same thing in Linux. You replaced `cat` with `tail` to remove the first line of the file and inserted `cut` into your pipeline to only grab specific fields from the file.

In that same spirit, there are many other commands in the Linux ecosystem that can achieve what the `uniq` command achieves in more or less the same fashion.

### `awk`

[`awk`](https://earthly.dev/blog/awk-examples/) is basically a mini-scripting language that is commonly used for manipulating data and producing usable output.

It's a lot more complex to use than `uniq` and requires you to learn a separate scripting language. However, it doesn't suffer from the same limitations that `uniq` does. For example, `awk` does not need a file to be sorted first.

Let's use [`awk` with our sample CSV file](https://earthly.dev/blog/awk-csv/):

~~~{.bash caption=">_"}
user@localhost:~$ awk -F, 'NR!=1;{A[$3]++}END{for(i in A)print i,A[i]}' \
meteorites.csv 
2022-01-08,13:47:05,Germany
2022-01-11,11:49:15,Australia
2022-03-02,09:23:27,Germany
2022-04-21,01:11:00,United States
2022-07-14,14:09:32,Canada
2022-08-08,13:37:34,Canada
2023-02-03,21:25:53,Japan
2023-03-05,23:59:09,Finland
2023-04-07,02:23:01,United States
2023-04-11,09:17:00,United States
Germany 2
country 1
Japan 1
Canada 2
Finland 1
Australia 1
United States 3
~~~

The `-F,` specifies that your file is comma-delimited. Then inside the scripting portion, the `NR!=1` tells `awk` to ignore the first line, and the `{A[$3]++}` tells `awk` to count unique values for the third column (*$3*) and store it in an array called `A`. Finally, it prints all the values for A with their counted values using a for loop (*ie* `{for(i in A)print i,A[i]}`).

The biggest change here is that you used *only* the `awk` command to achieve this, and you didn't need to sort the file at all. However, for novice Linux users, acquiring proficiency in the `awk` scripting language may pose a more significant challenge.

### `sort`

You can also use the `sort` command to remove duplicates:

~~~{.bash caption=">_"}
user@localhost:~$ tail -n +2 meteorites.csv | sort -t, -k3 -u 
2022-01-11,11:49:15,Australia
2022-07-14,14:09:32,Canada
2023-03-05,23:59:09,Finland
2022-01-08,13:47:05,Germany
2023-02-03,21:25:53,Japan
2022-04-21,01:11:00,United States
~~~

Here, you've added the `-u` flag to sort. It now only displays the first occurrence of a distinct value in the specified column (*ie* `-k3`).

Again, you can see that there are differences between `sort` and `uniq`. While `sort` correctly removes the duplicates, you can't display a count of the distinct values.

## Conclusion

In this tutorial, you've learned how to use `uniq` to count distinct values in a file, and the importance of sorting and cleaning the file beforehand. We covered how `uniq` works best on well-structured, clean inputs. There are numerous Linux commands to help you tailor your output.

For further exploration, refer to the additional resources linked in this guide, and [**Text Processing Commands** page](https://tldp.org/LDP/abs/html/textproc.html) from [The Linux Documentation Project](https://tldp.org).

And after you've mastered `uniq` and are ready for more Linux tools, why not give [Earthly](https://www.earthly.dev/) a try? It's a fantastic tool for build tool that works great at the command line.

Keep experimenting and overcoming challenges that come your way!

{% include_html cta/bottom-cta.html %}
