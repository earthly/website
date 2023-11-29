---
title: "Using Conditionals in Bash"
categories:
  - Tutorials
toc: true
author: Mdu Sibisi
sidebar:
  nav: "bash"
internal-links:
 - bash test
 - bash tests
 - flow control
excerpt: |
    Learn how to use conditionals in Bash to improve your scripting skills and automate tasks. This comprehensive guide covers everything from test commands and operators to conditional statements and case statements. Whether you're a beginner or an experienced Bash user, this article will help you level up your Bash programming skills.
last_modified_at: 2023-07-14
---
**"Understand Bash conditionals with our new article. Earthly ensures consistent builds in different environments. [Learn more about Earthly](/)."**

[Bash (bourne again shell)](https://www.gnu.org/software/bash/manual/html_node/What-is-Bash_003f.html) has been around since 1989 and owes its longevity to its usefulness and flexibility. While it's the default login and command shell for most [Linux](https://www.linux.org) distros, its value extends beyond that.

[Bash](/blog/understanding-bash/) can be used as a fully-fledged programming language and as a tool to automate repetitive and complex computational tasks. However, as with any other programming language, you need to understand how to manage Bash's control flow to truly get the most out of it.

Whether you're a power user writing simple scripts to help organize your files or a data scientist curating large sets of data, efficiently performing these tasks is nearly impossible without a conditional statement or two.

The following guide will introduce you to Bash's collection of conditionals and will teach you how to become proficient in their uses.

## What Are Bash Conditionals

Bash conditionals let you write code that performs different tasks based on specified checks. These checks can be based on a simple assessment that results in a true or false result. Alternatively, a conditional may be in the form of a multiple case check where a number of values are assessed before an operation is performed.

Conditionals make programmers' lives easier and help prevent and handle errors and failures. Without them, you'd have to manually perform checks before running a script or program. However, to build functioning conditionals and test expressions in Bash, you need a working knowledge of its test commands and operators. Before you review all the conditionals available, you need to learn how to build proper tests, starting with Bash's test commands.

### Bash Test Commands

Bash can be a very loose and flexible language. Many concrete concepts you'd find in other programming languages are absent, and you have to use conventional design patterns to make Bash work the same way other programming languages do.

For instance, conditionals assess the exit status of a command. If you want Bash to mimic Boolean evaluations, you'll need to use a specialized command. There are three ways you can test an expression in Bash:

- **`test`:** takes an expression as its argument and evaluates it (*ie* it exits with a status code dictated by the expression). It returns `0` to indicate that an expression is true. A value other than `0` (*ie* `1`) would indicate that it's false. For instance, `test $n -gt 5` evaluates if the value of the variable `$n`, is greater than five, and returns an exit code of `0` if true.

> You can use the `$?` variable to see the return value of the last executed command (*ie* to see if the test command evaluated its expression to true or false).

- **`[`:** is a shorthand alternative version of the `test` command. It does exactly what the test command does but with a slightly different syntax: `[ $n -gt 5 ]`.

> Note: The `[` built-in requires at least a single space after the opening bracket and one before the closing bracket.

- **`[[`:** is an improved version of the `[` built-in. It also evaluates an expression but with a few improvements and caveats. For instance, Bash doesn't perform [glob expansion](https://mywiki.wooledge.org/glob) or [word splitting](https://www.gnu.org/software/bash/manual/html_node/Word-Splitting.html) when parsing the command's argument. This makes it a more versatile command. `[[` is also slightly more lenient on syntax and allows you to run more modernized tests and conditions.

For instance, you can compare integers using the `<` and `>` operators. `[[ $n > 10 ]]` tests if the value of the `n`[variable](/blog/bash-variables) is greater (`-gt`) than ten. It will return an exit code based on this test. On the other hand, `[ $n > 10 ]` creates a (empty) file called `10`, and in most cases, it will return an exit status of `0` (barring that nothing stops it from creating the file).

Again, because the `[[` command skips glob expansion and word splitting, it makes testing regular expressions easier. For instance, the arguments of the command `[[ $n =~ [1-10] ]]` will cause the `[` command to fail. For this reason, many use cases require using this command over the test keyword or `[` built-in.

### Bash Test Operators

Now that you, hopefully, understand how Bash's test commands work, you can learn how to form test expressions. The core of the expressions is *test operators*. If you want to take full advantage of conditionals, you need to have a healthy understanding of them.

Bash has a large variety of test operators that apply to different variable types and situations. These operators are just flags passed to the test commands and include the following:

#### Compounding Comparison Operators

Compounding comparison operators allow you to combine test expressions. They return a value based on a test performed on multiple expressions:

- **`-a`:** is the *and* operator. It lets you test multiple conditions and returns true if all conditions are true (*ie* if `[ $n -gt 10 -a $n -lt 15 ]`).
- **`-o`:** is the *or* operator. It lets you test multiple conditions and returns true if one or more conditions are true (*ie* if `[ $n -gt 10 -o $n -lt 15 ]`).

#### Integer Comparison Operators

Integer comparison operators let you build expressions that compare whole numbers in Bash:

- **`-eq`:** tests if two values/variables are equal (`=` or `==`)
- **`-ne`:** checks if two values/variables are not equal (`!=`)
- **`-gt`:** checks if one value is greater than another (`>`)
- **`-ge`:** checks if one value is greater than or equal to another (`>=`)
- **`-lt`:** checks if one value is less than another (`<`)
- **`-le`:** checks if one value is equal or less than another (`<=`)

> You can use the symbols (`<`,`>`,`=`,`!=`, etc.) in place of the above word-based operators when using the `[[` built-in.

#### String Evaluation Operators

String evaluation operators let you compare and evaluate strings of text in Bash:

- **`==` or `=`:** checks if two strings are equal
- **`!=`:** checks if two strings are not equal to each other
- **`<`:** checks if one string is less than another using the ASCII sorting order
- **`>`:** checks if one string is greater than another using the ASCII sorting order
- **`-z`:** returns true if the string is empty or null (has a length of zero)
- **`-n`:** returns true if a string is not null

#### File Evaluating Operators

These advanced operators let you assess and compare files in Bash:

- **`-e`:** validates the existence of a file (returns true if a file exists)
- **`-f`:** validates if the variable is a regular file (not a folder, directory, or device)
- **`-d`:** checks if the variable is a directory
- **`-h` (or `-L`):** validates if the variable is a file that is a symbolic link
- **`-b`:** checks if a variable is a block special file
- **`-c`:** verifies if a variable is a character special file
- **`-p`:** checks if a file is a pipe
- **`-S`:** checks if a file is a socket
- **`-s`:** verifies if the size of the file is above zero (returns true if the file is greater than 0 bytes)
- **`-t`:** validates if the file is associated with a terminal device
- **`-r`:** checks if the file has read permissions
- **`-w`:** verifies if the file has write permissions
- **`-x`:** checks if the file has execute permissions
- **`-g`:** checks if the [SGID](https://www.linux.com/training-tutorials/what-sgid-and-how-set-sgid-linux/) flag is set on a file
- **`-u`:** verifies if the [SUID](https://www.techrepublic.com/article/linux-101-what-is-the-suid-permission/) flag is set on a file
- **`-k`:** checks if the [sticky bit](https://www.thegeekstuff.com/2013/02/sticky-bit/) is set on a file
- **`-O`:** verifies if you're the owner of a file
- **`-G`:** validates if the group ID is the same as yours
- **`-N`:** validates if a file was modified since it was last read
- **`-nt`:** compares the creation dates of two files to see if one file (file 1) is newer than the other (file 2)
- **`-ot`:** compares the creation dates of two files to verify if one file (file 1) is older than the other (file 2)
- **`-ef`:** checks if two variables are hard links to the same file

## Conditional Statements

The first category of conditionals you'll look at is known as conditional statements. Each statement assesses a singular condition (which can be compounded from multiple conditions) and performs an action (or list of actions).

### If Statements

The if statement is the most commonly used conditional in any programming language. The structure of a simple if statement is as follows:

~~~{.bash }
if test
then
perform actions
fi
~~~

The first line assesses a condition (any command). The `fi` indicates the end of the if statement (along with its body). Bash evaluates a command's exit code before performing (or skipping) an action (or set of actions). If a command returns an exit code of `0`, it has run successfully. In that case, the if statement will run the command(s) between the `then` and `fi` keywords.

A status code with any other value (1–255) denotes a failure and will cause the if statement to skip over the statements between the if's body. While Bash doesn't have true built-in conditions, you can co-opt and use its command status codes as a makeshift boolean, where `0` is true and any other value is false. You also have `true` and `false`, which are actual commands that return `0` and `1`, respectively.

Take a look at the following example:

~~~{.bash caption=""}
#!/bin/bash 

n=`ls -1 | wc -l` 
if [ $n -lt 10 ]
then 
printf "There are less than ten files here \n" 
fi
~~~

The code here first assigns the number of files in the current directory to a variable (`n`). It then uses the test operator `-lt` to test if the number count is less than ten. If the test condition is true, the command (`[ $n -lt 10 ]`) will exit with a status of `0`, returning an exit code of `0`. Then it displays a message informing the user that there are less than ten files in this particular directory.

Of course, this sample can be repurposed and used for more practical applications, like deleting files in a folder when they exceed a certain number.

### If-Else Statements

An if-else statement allows you to call an alternative command when an if statement's condition evaluates to false (*ie* when its command returns an error status code). In most cases, the *else* portion of the statement provides you a chance to perform some cleanup. For instance, you can use it to exit the script or inform the user that a condition has not been met. The syntax of the if-else statement is as follows:

~~~{.bash caption=""}
if test
then
perform actions
else
perform some different actions
fi
~~~

You can modify the previous example:

~~~{.bash caption=""}
#!/bin/bash

n=`ls -1 | wc -l`
if [ $n -lt 10 ]
then
printf "There are less than ten files here \n"
else
printf "There are more than ten files here \n";
fi
~~~

This time, the if-else informs the user that there are more than ten files instead of just exiting the script when it doesn't meet the first condition.

### If-Elif-Else Statements

The if-elif-else statement lets you add more functionality to the basic if and if-else statements. You can test multiple conditions and run separate commands when a condition is met.

Because things in the real world aren't always limited to two alternatives, you need conditionals with more nuance to suit complex use cases. The if-elif-else statement provides this subtlety. Its structure is as follows:

~~~{.bash caption=""}
if test
then
perform actions
elif test
then
perform elif action(s)
else
perform else action(s)
fi
~~~

Again, you can modify the last example:

~~~{.bash caption=""}
#!/bin/bash

n=`ls -1 | wc -l`
if [ $n -lt 10 ]
then
printf "There are less than ten files here \n"
elif [ $n -lt 15 ]
then printf "There are less than fifteen files here \n";
else
printf "There are more than fifteen files here \n";
fi
~~~

`elif` is essentially a shorthand of an else-if statement that you may recognize from other fully formed programming languages. In the example above, you check if there are less than ten files. If there are more than ten files, your else-if conditional expression will check if there are less than fifteen files. If both conditions are not met—in this case, the directory has more than fifteen files—then the script will display a message indicating this.

### Nested `If` Statements

If you want to add more refinement to your `if` and `elif` conditionals, you can use a nested or embedded if statement. A nested `if` lets you perform an additional check after a condition is met by an `if` statement. The structure looks like this:

~~~{.bash caption=""}
if test
then
if another_test
     then
     perform actions;
     fi
fi 
~~~

Of course, Bash doesn't require you to indent code. However, it's easier to read the above syntax if you do. Here's how the nested if looks in action:

~~~{.bash caption=""}
#!/bin/bash
n=`ls -1 | wc -l`
if [ $n -lt 10 ]
then
  printf "There are less than ten files here \n";
  if [ $n -gt 5 ]
  then
    printf "There are more than five files here \n";
  else
  printf "There are less than five files here \n";
  fi
fi
~~~

Here, you've added a nested if to your previous example. To start, it checks if the current directory has less than ten files. If the command runs successfully, it performs another check to see if there are more than five files and then displays a message accordingly.

### Case Statements

Case statements are one of the most important control flow tools for advanced programming. They work similarly to if-elif-else statements, but when employed correctly, they can help produce cleaner code. The syntax for a case statement is as follows:

~~~{.bash caption=""}
case <test variable> in
<test pattern1>)  <perform task>;;
<test pattern2>) <perform task>;;
<test pattern3>) <perform task>;;
……………
esac
~~~

Here, rather than using a condition, you test a variable that will be compared against the patterns, and when a match is found, the corresponding action(s) will be performed.

The structure may be a little hard for beginners to understand, but the more you use it, the more comfortable you'll become. Again, you can modify the previous examples with case statements:

~~~{.bash caption=""}
#!/bin/bash

n=`ls -1 | wc -l` 
echo $n

case $n in 
0) printf "There are no files here \n";; 
1) printf "There is one \n";;
2) printf "There are two files here \n";; 
3) printf "There are three files here \n";; 
4) printf "There are four files here \n";; 
5) printf "There are five files here \n";; 
6) printf "There are six files here \n";; 
7) printf "There are seven files here \n";; 
8) printf "There are eight files here \n";; 
9) printf "There are nine files here \n";; 
10) printf "There are ten files here \n";; 
*) printf "There are more than ten files here \n";; 
esac
~~~

This time, the example takes the file count and assesses it against twelve different patterns, which are all simple numbers. It displays a message with every pattern it suits. The pattern `*` acts as a catchall and will match if none of the other patterns match.

You can also combine multiple patterns with `|`:

~~~{.bash caption=""}
#!/bin/bash

n=`ls -1 | wc -l` 
echo $n

case $n in 
0|2|4|6|8|10) printf "There are even number of files here \n";; 
1|3|5|7|9) printf "There are odd number of files here \n";;
*) printf "There are more than ten files here \n";; 
esac
~~~

As you may have noted, the command list associated with each pattern ends in `;;`. However, you can also use `;&` or `;;&`. If you use `;&`, the execution will continue with the next clause even if the next pattern doesn't match (a fall through).

~~~{.bash caption=""}
#!/bin/bash

n=2

case $n in
2) printf "This will match. \n" ;&
3) printf "This will run even though it doesn't match.\n" ;;
esac
~~~

If you use `;;&`, the execution will continue with the next clause, only if the pattern matches:

~~~{.bash caption=""}
#!/bin/bash

a="abcd"

case $a in
a*) printf "This will match.\n" ;;&
b*) printf "This will be tested but won't match.\n" ;;&
*d) printf "This will be tested and will match.\n" ;;
esac
~~~

### Handling Script Failures Using Conditionals

As this guide has discussed, each command returns an exit code. Conditionals use these exit codes to determine which code should be executed next. If a function, command, or script should fail, a well-placed conditional can catch and handle this failure.

Bash has more sophisticated tools for [error handling](https://linuxhint.com/bash_error_handling/); however, if you're performing quick and dirty script failure handling, simple if or case statements should be sufficient.

### Storing Script Output

When troubleshooting or keeping a record of successful and failed scripts, you can output the results to an external file. The above guide has already touched on how you can output the results of a command using the `>` operator. You can also keep a record of script errors by using a combination of exit code tests, conditionals, and this operator. Here's an example:

~~~{.bash caption=""}
n=`ls -1 | wc -l` 

if [ $n -lt 10 ]
then
echo "There are less than ten files" > success.txt
else
echo "There are more than ten files" > fail.txt
fi
~~~

The above snippet will check if the current directory has less than ten files. If it does, it will output a success message to a file named `success.txt`. If it fails, it will redirect the echo command's output and place it in a file named `fail.txt`.

The `>` redirection operator will create a new file and write the output on that new file if the file doesn't exist. However, if the file does exist, the command will overwrite its contents. Thus, you should use the `>>` operator if you want to append contents to an existing file. These are the simplest ways to redirect output from Bash and place it on an external file.

## Conclusion

Learning conditionals could be your final hurdle to truly [understanding Bash](https://earthly.dev/blog/understanding-bash) and mastering it. Up until now, you may have underestimated Bash's true capabilities. You may even find that learning about Bash's various conditional statements, expressions, and operations inspires you to rewrite old scripts and improve them with better flow control.

But if you do, remember to utilize the correct syntax. Bash (especially sh) is case- and space-sensitive. Then you can transfer what you've learned from Bash and use it with [Earthly](https://earthly.dev/). Earthly lets you define and deploy your build using a Git-aware syntax that is strikingly similar to Bash.

Because Earthly's builds are neatly encapsulated and language-independent, they're easier to initiate and manage. If you're trying to build and deploy repeatable multiplatform software, Earthly is a great solution.

{% include_html cta/bottom-cta.html %}