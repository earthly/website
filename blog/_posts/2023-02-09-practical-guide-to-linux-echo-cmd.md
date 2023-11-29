---
title: "A Practical Guide To Linux Echo Command"
categories:
  - Tutorials
toc: true
author: Ubaydah Abdulwasiu
editor: Bala Priya C
excerpt: |
    Learn how to use the `echo` command in Linux to display text, format output, add and overwrite text in files, display variables, search for files, and more. Discover the various options and practical examples of using the `echo` command, as well as how to change the output colors.
internal-links:
 - Linux
 - Command
 - Echo
last_modified_at: 2023-07-19
---
**This article explains the Linux `echo` command in detail. Earthly improves continuous integration (CI) workflows by optimizing the use of `echo` in shell scripts. [Learn how](/).**

**Linux** is one of the most popular operating systems. It has a powerful command-line interface that allows various commands to be passed as instructions to be executed by the computer. The `echo` command is one of the most commonly used Linux commands.

This tutorial will introduce you to the Linux `echo` command, go over its options and their usage, and show you how you can use it.

## What Is the `echo` Command?

`echo` is a built-in Linux command that is used to display the text passed in as an argument. It is one of the basic Linux commands used in shell scripting and Bash files to display output status text at the command line.  

Just like the Python `print()`function that is used to display texts on the screen, `echo` is used in Linux, Bash, and C shells for the same purpose. It has a simple syntax with various options:

~~~{.bash caption=">_"}
echo  [option] [argument]
~~~

The argument is the text or the message you want to display on the terminal, while the option is used to modify the behavior of the text passed.

For example, to suppress the newline character and display the message "Hello, world!" on a single line, you'll run the following command:

~~~{.bash caption=">_"}
echo -n Hello, world!
~~~

## Understanding the `echo` Command Options and Their Uses

![Understanding]({{site.images}}{{page.slug}}/aZ3raPf.png)\

The `echo` command has a few options that are used to format the string output to the screen. This section will go over some of these options.

### Use `n` to Omit Trailing Newlines

`echo` prints your output on a new line by default. You can omit trailing newlines by using the `n` option.

Here's an example:

~~~{.bash caption=">_"}
echo -n Welcome
~~~

~~~{caption="Output"}
Welcomeubaydah@ubaydah
~~~

You can also print multiple lines of text without adding new lines after each line; use the `n` option with the echo command.

~~~{.bash caption=">_"}
echo -n "Hello World" "This is a test" "This is another test"
~~~

~~~{caption="Output"}
Hello World This is a test This is another testubaydah@ubaydah
~~~

### Use `-e` to Add Various Escape Characters

`-e` character allows you to use the various escape characters to format the output of your argument in different ways. The option allows `echo` to interpret these characters.

The following escape characters are used with `echo`:

#### Use `\a` for Alert

`\a` character allows you to sound an alert like a beep with an `echo` when the output is displayed.

Here's an example:

~~~{.bash caption=">_"}
echo -e "\aWelcome Back"
~~~

~~~{caption="Output"}
Welcome back
~~~

#### Use `\b` for Backspace

The `\b` character is a backspace character. It is used to erase the previous character in the output string. When the `\b` character is encountered in the output string, the terminal emulator will erase the previous character and move the cursor one position to the left.

Consider the following examples:

1. Print a string with a backspace character

~~~{.bash caption=">_"}
echo -e "Learning is\b good"
~~~

~~~{caption="Output"}
Learning i good    
~~~

In the example above, `s` is erased, and the remaining text is in the output.
2. Print a string with a backspace character at the end

~~~{.bash caption=">_"}
echo -e "Learning is  good\b"
~~~

~~~{caption="Output"}
Learning is goo    
~~~

In the example above, the last letter is erased.
3. Print a string with multiple backspace characters.

~~~{.bash caption=">_"}
 echo -e "Learning \bis\b\b\b good"
~~~

~~~{caption="Output"}
Learning good    
~~~

#### Use `\c` to Trim Output

The 'c' character in the echo command suppresses the trailing newline that is automatically added to the end of the output. This is useful when printing a string of text that another command or string of text must immediately follow without a line break in between.

Here's an example:

~~~{.bash caption=">_"}
echo -e "Learning is\c good"
~~~

~~~{caption="Output"}
Learning is    
~~~

Here, "good" is truncated, and everything before the `\c` is printed out.

You can also print a string with `\c` and a custom delimiter:

~~~{.bash caption=">_"}
echo -e "Hello World:\c"
~~~

~~~{caption="Output"}
Hello World:%
~~~

#### Use `\f` for Form Feed

`\f`: This means the [form feed](https://en.wikipedia.org/wiki/Page_break) character, and it lets the printer advance to the next page.

You can use the form feed character `\f` with the `echo` command to insert a page break in a text file. For example, the following command will insert a page break in a text file named "newfile.txt":

~~~{.bash caption=">_"}
echo -e "This is the first page\fThis is the second page" > newfile.txt 
~~~

The second example of using the form feed character `\f` in an `echo` command is to print multiple pages of text on a single line. Here's an example:

~~~{.bash caption=">_"}
echo -e "Page 1\fPage 2\fPage 3"
~~~

~~~{caption="Output"}
Page 1
      Page 2
            Page 3
~~~

This will print the text on separate pages.

#### Use `\n` To Add Newline

The `\n` character allows you to add a new line to your output. Here's an example:

~~~{.bash caption=">_"}
echo -e "Learning is\ngood"
~~~

~~~{caption="Output"}
Learning is
good
~~~

The `\n` character can also be used in combination with other escape characters,
such as `\t` for a tab, to create more formatted output.

Here's an example:

~~~{.bash caption=">_"}
echo -e "Hello\n\tWorld"
~~~

~~~{caption="Output"}
Hello
    World
~~~

#### Use `\t` for Horizontal Tab Space

The `\t` character gives you the behavior of horizontal tab spaces.

Here's an example:

~~~{.bash caption=">_"}
echo -e "Learning\tis\tgood"
~~~

~~~{caption="Output"}
Learning        is      good
~~~

Here, the character adds horizontal tab spaces between the texts.

#### Use `\v` for Vertical Tab Space

The `\v` character gives you the behavior of vertical tab spaces, as shown:

~~~{.bash caption=">_"}
echo -e "Learning\vis\vgood"
~~~

~~~{caption="Output"}
Learning
             is
                good
~~~

Here, the character adds vertical tab spaces between the texts.

#### Use `\\` to Display Backslash

The `\\` character allows you to display the backslash `\` character.

Here's an example:

~~~{.bash caption=">_"}
echo -e "Learning\\good"
~~~

~~~{caption="Output"}
Learning\good
~~~

### Use `-E` to Ignore Escape Characters

Unlike the `-e` option which lets you interpret escape characters, the `E` option ignores all the escape characters in an argument.

~~~{.bash caption=">_"}
echo -E "Learning\n is \tgood"
~~~

~~~{caption="Output"}
Learning\n is \tgood
~~~

Here, the texts are printed as they are passed in, and the escape characters are ignored.

## The Echo Command: Some Practical Examples

![The Echo Command]({{site.images}}{{page.slug}}/VLv16lI.png)\

### Adding and Overwriting Texts in a File

The `echo` command can be used to add new text to a file or overwrite the previous texts in a file. This operation is carried out using the `>` or `>>` operators. The `>` operator is used for overwriting the file content, while the `>>` operator is used for adding new texts to the file.

Here's an example:

~~~{.bash caption=">_"}
echo Hello world >> test.txt
~~~

This creates a new file named 'test.txt' and adds the text if the file doesn't exist, or simply adds the new text to the file if it already exists.

To check the content of the file:

~~~{.bash caption=">_"}
cat test.txt
~~~

~~~{caption="Output"}
Hello world
~~~

You can overwrite the text in the file above.

~~~{.bash caption=">_"}
echo Learning is Good > test.txt
~~~

The file text changes to the following:

~~~{.bash caption=">_"}
cat test.txt
~~~

~~~{.bash caption="Output"}
Learning is Good
~~~

### Displaying Variables in the Terminal

Using the `echo` command, you can display the different variables you declared as well as [environment variables](/blog/bash-variables) on your terminal. Here's an example:

~~~{.bash caption=">_"}
ubay=good
~~~

~~~{.bash caption=">_"}
echo "the value of ubay is $ubay"
~~~

~~~{caption="Output"}
the value of ubay is good
~~~

Here, you declared a new variable called `ubay` and assigned `good` to it. Its value is printed out by adding the `$` sign in front of the variable, which tells `echo` that it is a variable and not a text.

You can also use the echo command to display the value of multiple variables at once by separating them with a space. For example, if you have a second variable `new` that contains the value "hello", you can display both `ubay` and `new` by running the following command:

~~~{.bash caption=">_"}
echo $ubay $new
~~~

~~~{caption="Output"}
good hello
~~~

### Printing Files of a Specific Kind

You may sometimes want to look for a specific file type in a specific directory. In this case, the `echo` command will come in handy, as it can be used to display files of a specific type that exist in a directory.

Consider the following example where you display all the `png` files in your Desktop directory:

~~~{.bash caption=">_"}
echo *.png
~~~

~~~{caption="Output"}

Screenshot 2022-10-19 at 12.25.13.png \
Screenshot 2022-10-27 at 14.44.38.png \
Screenshot 2022-10-29 at 08.23.36.png \
Screenshot 2022-10-29 at 08.23.59.png \
Screenshot 2022-10-29 at 08.24.16.png \
Screenshot 2022-10-29 at 08.25.02.png \
Screenshot 2022-10-29 at 08.28.01.png 
~~~

This displays all of the files with the extension `png`  in your current directory. When searching for documents in your folders, this can be helpful because you can easily filter out if that document type exists. You can also display all `.txt` files in your directory.

Here's an example:

~~~{.bash caption=">_"}
echo  *.txt
~~~

~~~{ caption="Output"}
myfile.txt output.txt test.txt
~~~

You can also search for a specific file type in your directory by piping the`echo` command to the `grep` command.

Here is an example of how you can do this:

~~~{.bash caption=">_"}
echo "myfile.txt" | grep -r myfile.txt 
~~~

In this example, the `echo` command is used to specify the text "myfile.txt", which is then piped to the `grep` command using the pipe operator `|`. The `grep` command is used with the `-r` option, which tells it to search *recursively* through all directories and subdirectories for the specified text.

This command will search for the file named "myfile.txt" within the current directory and all of its subdirectories, and output the results of the search to the terminal.

### Using `echo` as an Alternative to the `ls` Command

The `echo` command can also be used in place of the [ls](https://www.digitalocean.com/community/tutorials/ls-command-in-linux-unix) command to list all the contents of a directory.

Here's an example:

~~~{.bash caption=">_"}
 echo *
~~~

~~~{ caption="Output"}

Screenshot 2022-11-07 at 13.40.11.png \
Screenshot 2022-11-07 at 13.43.53.png
crud-nestjs dashmart digitise_market first-angular-app \
flask-app flexpay go-auth iac-with-azure mizala-task nipe \
nipe-portal-backend pennybit platr-marketplace-api \
platr-notifications-api project_hoobank recipes-api \
redis-todo-cli-app server test.txt thrift_monkey \
ubaydah-abdulwasiu-assignment-02 url-shortener
~~~

Here, you listed all the contents in the desktop directory.

You can also list only the directories and exclude files:

~~~{.bash caption=">_"}
echo */
~~~

~~~{ caption="Output"}

First Semester 300L/ DSA in Golang/ DSA/ GO-API/ Go-path/ \
backend/ bank-modern-app/ blog-fast-api/ bookly-jamstack-hack/ \
cd0039-Identity-and-Access-Management/ \
cd0157-Server-Deployment-and-Containerization/ cisco-starter-repo/ \
crud-nestjs/ dashmart/ digitise_market/ first-angular-app/ \
flask-app/ flexpay/ go-auth/ iac-with-azure/ mizala-task/ \
nipe-portal-backend/ nipe/ pennybit/ platr-marketplace-api/ \
platr-notifications-api/ 

~~~

This list only contains folders and does not include files in the desktop directory, which is useful when searching for folders in your directory.

To print the names of only the files in the current directory, you can use the following:

~~~{.bash caption=">_"}
echo *[^/]
~~~

This will only print the names of files that do not end in a forward slash (/), indicating that they are files and not directories.

### Piping `echo` With Other Commands

The echo command can be piped with other commands to perform various actions using the pipe operator `|`. Some examples of piping the echo command with other commands are:

#### Using `echo` With the `tee` Command

To output the result of a command and save it to a file, the echo command can be piped with the tee command:

~~~{.bash caption=">_"}

echo "Hello World" | tee output.txt

~~~

To append the output of a command to an existing file, the `echo` command can be piped with the `tee` command and the -a flag:

~~~{.bash caption=">_"}
echo "Hello World" | tee -a output.txt
~~~

#### Using `echo` With the `tr` Command

To pass the output of a command as input to another command, the `echo` command can be piped with the desired command:

~~~{.bash caption=">_"}
echo "Hello World" | tr '[:lower:]' '[:upper:]'
~~~

#### Using `echo` With the `grep` Command

To search for a specific string in the output of a command, the `echo` command can be piped with the `grep` command:

~~~{.bash caption=">_"}
echo "Hello World" | grep "World"
~~~

This would search for the text "world" within the output of the echo command, which in this case is the string "Hello World". The `grep` command will return the string "World" since it matches the search pattern.

You can use the `-n` option with `grep` to include the line number in the output:

~~~{.bash caption=">_"}
echo "Hello world" | grep -n "world"
~~~

This would return "1:world", indicating that the string "world" was found on line 1 of the output.

### Changing Output Colors

By default, the color of the output of the `echo` command matches the terminal theme. You might be in a situation where you need to change the colors, such as when writing a script and you need to show whether a step was successful, which is usually displayed in green, or warn them about a step in which red is used.

The color output is changed by formatting them using the [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)  for each color.

Here's an example:

~~~{.bash caption=">_"}
echo -e "\033[0;31mThis is Red"
~~~

~~~{.bash caption="Output"}
This is Red
~~~

Here, you used `\033[` which represents  `ESC[`, followed by the ANSI escape color code for Red `0;31`, and then an `m` to change the color of the output.

You can also write a [Bash script](/blog/understanding-bash) to perform an action and change color. Here's an example:

~~~{.bash caption="myscript.sh"}

#!/bin/bash

# Set the Number to Find the Square Root Of

number=9


# Calculate the Square Root of the Number

result=$(echo "sqrt($number)" | bc)


# Display the Result

echo -e "The square root of $number is \033[0;32m$result"
~~~

In this script, we first set a variable called `number` to the value we want to find the square root of. Then, we use the `echo` command to pass the `sqrt` function and the value of `number` to the `bc` command, which calculates the square root and stores the result in a variable called `result`. Finally, we use the echo command to display the result in the terminal and change its color to green.

Save this script to a file , say, myscript.sh, [make](/blog/makefiles-on-windows) it executable with the `chmod` command: `chmod +x myscript.sh`, and then run it with the `./ command`: `./myscript.sh` to see the green message in the terminal.

Here are the ANSI escape color codes for some colors:

|Colors|Codes|
|-------|----|
|Red | 0;31|
|Yellow|1;33|
|Green|0;32|
|Blue|0;34|
|White|1;37|

## Conclusion

This tutorial equipped you with the know-how of using the `echo` command and its various options like `-n`, `-e`, and `-E`. We explored its uses in different scenarios including text manipulation, outputting variables, and filtering files. Also, we saw how it can be integrated with other commands using the pipe operator for customized output colors.

As you continue to explore and enhance your command line skills, you might be interested in powering up your Linux build automation. If so, give [Earthly](https://www.earthly.dev/) a shot. It's a tool that can significantly simplify and optimize your build processes.

{% include_html cta/bottom-cta.html %}