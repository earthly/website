---
title: "Using Loops In Bash"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea

sidebar:
  nav: "bash"
internal-links:
 - bash loops
 - while loop
 - while loops
 - until loop
 - until loops
excerpt: |
    Learn how to use loops in Bash to control the flow of your programs. This article covers the different types of loops in Bash, including `while`, `until`, and `for`, and provides examples of how to use them in practical scenarios.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about looping in bash. If you are looking for to move beyond bash scripts for building and deploying then [check us out](/).**

Like any other programming language, [Bash](https://www.gnu.org/software/bash/) supports loops. The loops are used to repeatedly execute a set of commands based on some condition. Along with [conditionals](https://earthly.dev/blog/bash-conditionals/), they're the most common way to control the flow of a program.

Once you've mastered [variables](https://earthly.dev/blog/bash-variables/) and conditionals, you're ready to learn loops. In this article, you'll learn the different types of loops provided by Bash and see some examples of using them to accomplish various tasks.

## `while` Loop

Bash provides three types of loops: `while`, `until`, and `for`.

The `while` loop is used to execute commands as long as a condition is true. The general syntax for a `while` loop is as follows:

<div class="narrow-code">

~~~{.bash caption=""}
#!/bin/bash
while test-commands
do
    consequent-commands
done
~~~

Or equivalently, it can be a one-liner:

~~~{.bash caption=">_"}
while test-commands; do consequent-commands; done
~~~

</div>

The `test-commands` can be any command that exits with a success or failure status. An exit status of `0` is considered a success, and any non-zero status is considered a failure. Since each Linux command exits with a status code, you can use any command as a condition for the `while` loop.

Before executing the commands in the body of the `while` loop, the condition is checked. The loop is executed if the `test-commands` exits with success. If the `test-commands` exits with a failure, the loop doesn't run. The return code of the `while` loop is the return code of the last command in the body of the `while` loop.

Just like [conditionals](https://earthly.dev/blog/bash-variables/), you can use the `test`, `[`, and `[[` commands in the condition of the `while` loop. For example, the following `while` loop prints off all the numbers from 1 to 10:

~~~{.bash caption=""}
#!/bin/bash
i=1

while [ $i -le 10 ]
do
  echo $i
  ((i++))
done
~~~

The condition above is `[ $i -le 10 ]`. The `[` command evaluates whether `$i` is less than or equal to 10, and if it is, the command exits with a status of `0`. Since `i` is initiated with the value of `1`, the condition is true, so the loop is executed and prints `1`. In the loop's body, `$i` is incremented, and in the next iteration, the condition is rechecked. This goes on until `$i` becomes `11`, at which point, the `[` command exits with a status of `1`, and the loop exits.

Being able to use `[` and `[[` means you can have more complex conditions by combining two or more conditions, or performing tests related to variables and files. You can find a full list of tests in the [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html#Bash-Conditional-Expressions).

You can also use arithmetic expressions to evaluate numerical comparisons in the `while` loop condition. Below is the `while` loop from above, rewritten using the arithmetic expression:

~~~{.bash caption=""}
#!/bin/bash
i=1

while ((i <= 10))
do
  echo $i
  ((i++))
done
~~~

> Note that this only works for arithmetic expressions.

## `until` Loop

The `until` loop is a rarely used cousin of the `while` loop. Its syntax is similar to the `while` loop:

~~~{.bash caption=""}
#!/bin/bash
until test-commands
do
    consequent-commands
done
~~~

The only difference between the `while` loop and the `until` loop is that the `until` loop will run as long as `test-commands` has a non-zero exit status. You can think of it as an inverted `while` loop. Here's a sample:

~~~{.bash caption=">_"}
$ i=1
$ until [ $i -gt 10 ]; do echo $i; ((i++)); done
1
2
3
4
5
6
7
8
9
10
~~~

## `for` Loop

`for` loops in Bash are used to iterate over a list of items. The general syntax of the `for` loop is as follows:

~~~{.bash caption=""}
#!/bin/bash
for variable_name in list_of_items
do
    commands
done
~~~

Or it can be written as a one-liner:

~~~{.bash caption=">_"}
for variable_name in list_of_items; do commands; done
~~~

The `variable_name` is the name of the variable that you can access in the body of the loop that represents the current item from the list as the list is being looped through. The `list_of_items` is a list of space- or newline-separated items, or a command that returns a list of items.

To begin, the list is expanded according to the [expansion rules](https://www.gnu.org/software/bash/manual/bash.html#Shell-Expansions), and for each item in the list, the `commands` will run. At every iteration, the current item can be accessed using the `variable_name`.

Here's an example of a `for` loop:

~~~{.bash caption=""}
#!/bin/bash

for word in hello world
do
    echo $word
done
~~~

The output is as follows:

~~~{.bash caption=">_"}
hello
world
~~~

As you can see, the list contains two items, `hello` and `world`. In the first iteration, `word` is bound to `hello`, and `hello` is printed. In the second iteration, `word` is bound to `world`, so `world` is printed.

It's possible to generate a range of numbers or characters using the [sequence expression](https://www.gnu.org/software/bash/manual/bash.html#Brace-Expansion) syntax. The syntax of the sequence expression is `{start..end}` where `start` and `end` are integers or characters. This expression creates a range of numbers or characters between `start` and `end` that are both inclusive. You can also optionally specify an interval with the syntax `{start..end..interval}`.

The `for` loop can iterate over a range of numbers or characters created using the sequence expression:

~~~{.bash caption=">_"}
$ for i in {1..10..2}; do echo $i; done
1
3
5
7
9
~~~

If you're using the `for` loop in a script, you can omit the `in list_of_items` part. In that case, the loop will iterate over the arguments passed to the scripts. This is the same as running `for variable_name in "$@"`. You can find out more about `$@` in ["Understanding Bash Variables"](https://earthly.dev/blog/bash-variables/).

To test this, create a file named `for_loop.sh` with the following code:

~~~{.bash caption=""}
#!/bin/bash

for i
do
    echo $i
done
~~~

Then make this code executable and run it with some arguments:

~~~{.bash caption=">_"}
$ chmod +x for_loop.sh
$ ./for_loop.sh 1 2 3
1
2
3
~~~

Bash also has an alternate form of the `for` loop that is similar to the `for` loop in languages like C or C++. The syntax is as follows:

~~~{.bash caption=""}
#!/bin/bash

for (( expr1 ; expr2 ; expr3 ))
do 
    commands
done
~~~

Here, `expr1`, `expr2`, and `expr3` are arithmetic expressions. Before the loop starts, `expr1` is evaluated. Then `expr2` is evaluated, and if it evaluates to a non-zero value, the loop runs. After every iteration, `expr3` is evaluated. The loop runs until `expr2` evaluates to zero.

> Note that `expr2` *must* evaluate to a non-zero value for the loop to run, unlike the `while` loop.

Here's an example of this type of `for` loop:

~~~{.bash caption=""}
$ for (( i=1 ; i<=10; i++ )); do echo $i; done
1
2
3
4
5
6
7
8
9
10
~~~

All three expressions are optional, and if any of them are omitted, it will evaluate to `1`. However, semicolons are required.

Here's a sample:

~~~{.bash caption=">_"}
$ i=1
$ for (( ; i<=10; i++ )); do echo $i; done
1
2
3
4
5
6
7
8
9
10
~~~

If you're familiar with `for` loops in Python, you're probably used to using them for iterating over arrays. You can also do the same in Bash, albeit with a bit of a caveat.

Say you are defining an array like the following:

~~~{.bash caption=">_"}
$ WORDS=('Hello' 'World' 'This' 'Is' 'An' 'Array')
~~~

Then you'd want to run a `for` loop like this:

~~~{.bash caption=">_"}
$ for i in ${WORDS}; do  echo $i; done
~~~

This prints only `Hello` and *does not* iterate over the array.

This is because `${WORDS}` is the same as `${WORDS[0]}` (*ie* the first element of the array). To iterate over the array, you need to expand the array using either `${WORDS[@]}` or `${WORDS[*]}`. Both versions are the same unless it's double-quoted. You can learn more about this difference in the [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html#Arrays).

~~~{.bash caption=">_"}
$ for i in ${WORDS[@]}; do  echo $i; done
Hello
World
This
Is
An
Array
~~~

## `break` and `continue` Statements

The `break` and `continue` statements help modify the default flow of the loop. The `break` statement immediately stops the loop, and the `continue` statement skips the rest of the loop and jumps to the next iteration. These statements can be used in the body of the `while`, `for`, and `until` loops.

In the following example, when `i` equals `6`, the `break` statement is encountered, and the loop stops so the output is only up to `6`:

~~~{.bash caption=""}
#!/bin/bash

for (( i=1; i<=10; i++ ))
do
    echo $i
    if [ $i -eq 6 ]
    then
        break
    fi
done

# Output:
# 1
# 2
# 3
# 4
# 5
# 6
~~~

The following example shows the `continue` statement in action. When `i` is equal to `6`, the `continue` statement causes Bash to skip the `echo` command and jump to the next iteration.

~~~{.bash caption=""}
#!/bin/bash

for (( i=1; i<=10; i++ ))
do
    if [ $i -eq 6 ]
    then
        continue
    fi
    echo $i
done

# Output:
# 1
# 2
# 3
# 4
# 5
# 7
# 8
# 9
# 10
~~~

As you can see, `6` is skipped in the output.

## Examples Using Loops

Now that you know the three types of loops, it's time to see them in action. Below are a few practical use cases of the various loops:

### Renaming Files

If you have to rename several files at once, loops can be a valuable resource. By utilizing `for` loops, you can iterate over a list of files and rename them. In the following example, the script renames all `.jpeg` files in a directory to `.jpg`:

~~~{.bash caption=""}
#!/bin/bash

for i in *.jpeg
do
    mv $i ${i//jpeg/jpg}
done
~~~

You can read ["Bash String Manipulation"](https://earthly.dev/blog/bash-string/) to learn more about how `${i//jpeg/jpg}` works.

### Waiting for Successful Execution of a Command

Sometimes, you need to wait for another command to finish executing before you can continue with your script. For instance, if your script needs a running server, you can utilize a `while` loop to wait for the server to start. How exactly you check for the execution of the command depends on the command and how it communicates the status of its execution.

Following is an example where the script waits for some command to finish. It's assumed that this command creates a file named `result.txt` to indicate its execution:

~~~{.bash caption=""}
#!/bin/bash

while [ ! -f result.txt ]
do
    echo "Waiting for result.txt to be created..."
    sleep 1
done
echo "File created. Exiting"
~~~

Save the above code in a file and run it. You'll see that it prints "Waiting for result.txt to be created…" every second. In another terminal, create `result.txt` by running `touch result.txt`, and the script will terminate.

### Counting Files in a Directory

The following example is slightly complex. It counts the number of directories and files with different extensions and presents the number of files corresponding to each extension:

~~~{.bash caption=""}
#!/bin/bash

declare -A counter

for i in *
do
        if [[ -d "$i" ]]
        then
                ((counter["dir"]++))
        elif [[ -f "$i" ]]
        then
                extension=${i##*.}
                ((counter[${extension}]++))
        fi
done

for i in "${!counter[@]}"
do
    echo "$i = ${counter[$i]}"
done
~~~

The script uses `declare- A` to declare an associative array named `counter`. The `for` loop then iterates over all the files in the current directory. The test `[[ -d "$i" ]]` checks if the file is a directory. If it is, the `counter["dir"]` value is incremented. The `"dir"` key will automatically be created, and the value will be set to `0` the first time it is accessed.

Then the `[[ -f "$i" ]]` test checks if it is a file or not. If it is, it extracts the extension using the [shell parameter expansion](https://www.gnu.org/software/bash/manual/bash.html#Shell-Parameter-Expansion) and increments the corresponding counter in the array.

The second `for` loop iterates over the keys of the array. Since `counter` is an associative array, `${counter[@]}` will expand to only the values of the array. Then `${!counter[@]}` is used, which expands to the list of indices. The indices, along with the values, are then printed.

Here's a sample output:

~~~{.bash caption=""}
dir = 54
java = 1
log = 49
pdf = 65
json = 11
out = 1
png = 44
journal = 1
zip = 25
js = 1
txt = 5
jpeg = 7
~~~

### Guessing Game

While the other examples may seem a little boring, this one is a bit more fun: a game. The script will generate a secret random number between 1 and 100, and you have to try and guess it in five tries. Here's the script:

~~~{.bash caption=""}
#!/bin/bash

number=$(($RANDOM % 100 + 1))
count=1

while [ ${count} -le 5 ]
do
    read -r -p "Enter your guess: (${count} / 5): " guess
    if [ ${guess} -eq ${number} ]
    then
            echo "You win"
            break
    elif [ ${guess} -lt ${number} ]
    then
            echo "You're thinking too small."
    else
            echo "You're thinking too large."
    fi
    ((count++))
done
~~~

Here, `$RANDOM` is used to generate a random number. The `$count` variable stores the number of guesses made by the user. A `while` loop is used to run the script as long as `$count` is less than or equal to 5. In the body of the `while` loop, the `read` command is used to get the user's input. If it's equal to the secret number, the user wins, and the loop ends. Otherwise, a hint is given based on whether the user's guess is greater or less than the secret number.

<div class="wide">
![Playing the game and winning using binary search]({{site.images}}{{page.slug}}/zuGh3RF.png)
</div>

## Conclusion

Loops are one of the most fundamental concepts in Bash, or any programming language for that matter. From iterating over items to manipulating files, any fairly advanced script is certain to employ loops. In fact, the Bash shell itself is a big [`while` loop](https://github.com/bminor/bash/blob/master/eval.c#L71).

This article gave you an overview of loops in Bash, using `while`, `until`, and `for` loops. If you want to learn more about loops, you can consult the [Bash manual](https://www.gnu.org/software/bash/manual/bash.html) or if you want to learn more about Bash, you can check out the [next article in this series](link).

If you love building things in Bash, you're sure to love [Earthly](https://earthly.dev). Supercharge your build system with the clean and approachable syntax, and repeatable builds, of Earthly.

{% include_html cta/bottom-cta.html %}
